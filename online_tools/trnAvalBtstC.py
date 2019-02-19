import pandas as pd
import numpy  as np
import sys, os
sys.path.append('/home/hezhiyua/desktop/BDT_study/')
sys.path.append('/home/hezhiyua/desktop/pandas_learn/online_tools/')
sys.path.append('/home/hezhiyua/desktop/CNN_Preprocessing/Classes/')
from set_weight       import *
from DataTypes        import pkl_df

#====settings==================================================================================================
tvt_l         = ['train','val','test']
phpt          = {}
phpt['train'] = '40_5000'
phpt['val']   = '40_2000'
phpt['test']  = '50_5000'
ABC_str       = ''
for i in tvt_l:    ABC_str += i+phpt[i]

pth_root    = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/all_in_1/nn_format/leading_jet/'
pth         = pth_root + 'playground/' 
pth_dic     = {}
for i in tvt_l:    pth_dic[i] = pth_root + '/test/'+phpt[i]+'/'

pth_out_lola = pth + 'lola/'
os.system('mkdir '+pth_out_lola)
pth_out     = pth_out_lola + ABC_str +'/'
os.system('mkdir '+pth_out)
#k_fold            = 10
#nan_replacement   = 0 
xs  = { '100to200': 28060000 , '200to300': 1710000 , '300to500': 351300 , '500to700': 31630 , '700to1000': 6802 , '1000to1500': 1206 , '1500to2000': 120.4 , '2000toInf': 25.25 }
#====settings==================================================================================================

qcd_inst = pkl_df(pth_root, 'qcd_all_400pfc'+'.h5')
sgn_inst = {}
for i in tvt_l:    sgn_inst[i] = pkl_df(pth_dic[i], 'vbf_'+phpt[i]+'_all_400pfc'+'.h5')
_, df_qcd_dic = qcd_inst.splitN(3)
tvt_dic          = {}
tvt_dic['train'] = pd.concat( [df_qcd_dic[0], sgn_inst['train'].df] )
tvt_dic['val']   = pd.concat( [df_qcd_dic[1], sgn_inst['val'].df] )
tvt_dic['test']  = pd.concat( [df_qcd_dic[2], sgn_inst['test'].df] )

tb_dict          = {}
for key in tvt_l:
    tmp_inst     = onlineDF(tvt_dic[key], xs)
    tmp_inst.set_weights()
    tmp_inst.shuffle()
    #tb_dict[key] =tmp_inst.df
    #print tb_dict[key][:8] 

    (tmp_inst.df).to_hdf( pth_out + 'vbf_qcd-'+key+'-'+'v0_40cs'+'.h5','table',append=True)




















exit()
###################################################################################################################
################################ For Debugging~~~~
###################################################################################################################
from main_bdt         import bdt_train, bdt_val, bdt_test
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree     import DecisionTreeClassifier
from sklearn          import metrics
from keras.callbacks  import EarlyStopping, ModelCheckpoint, Callback
from keras.models     import Sequential
from keras.layers     import Dense
from keras            import utils




test_output_dir             = 'test_out/'
os.system('mkdir '+pth+test_output_dir)
test_early_stop_weights_dir = 'test_early_stop_weights/'
pth_out                     = pth + test_output_dir + test_early_stop_weights_dir
os.system('mkdir '+pth_out)
pth_checkpoint              = pth_out + "/weights-latest.hdf5"


in_tpl            = ['CHF']#['cHadEFrac']#['CHF']#['cHadEFrac']
train_nn          = True#False
train_bdt         = True#False#True
val_aug           = False#True#False
train_weight      = False#True
guess_test        = False#True

#-------------------------------------- FCN
train_str    = 'train'#'val'#'train'#'test'
val_str      = 'val'#'test'#'val'
test_str     = 'test'#'train'#'test'#'val'#'test'

es_patience  = 4#4#8#5
n_nodes      = 4#2#8#4#30
in_shape     = (1,)#(2,)#(1,)#(2,)
#Optimizer    = 'rmsprop'
#loss_f       = 'mean_squared_error'
Optimizer    = 'adam'
loss_f       = 'categorical_crossentropy'

n_batch_size = 32#64    #16-1024#512#128
n_epochs     = 44#22#2#88

#-------------------------------------- BDT
pss = {
      'calcROCon': 0,
      'path_result': './out/',
      'descr': 'testt',

      'max_depth': 4,
      'algorithm': 'SAMME',
      'n_estimators': 140,
      'learning_rate': 0.1,
      }







arr_dict = {}
X_dict   = {}
y_dict   = {}
w_dict   = {}
#in_tpl = [0]#(0,1)#[0]#[1]


#for key, item in tb_dict.iteritems():    arr_dict[key] = np.asarray(item)

for key, item in tb_dict.iteritems():
    X_dict[key] = np.asarray(item[in_tpl])
    y_dict[key] = np.asarray(item['is_signal_new'])
    w_dict[key] = np.asarray(item['weight'])


#for key, item in arr_dict.iteritems():    X_dict[key], w_dict[key], y_dict[key] = item[:,in_tpl], item[:,2], item[:,3]
#for key, item in arr_dict.iteritems():
#    w_dict[key] = np.ones( X_dict[key].shape )


if not train_weight:
    w_dict[train_str] = np.ones(len(w_dict[train_str]))
    print w_dict[train_str]


#"""
#\\\\\\\\\\\\\\\\\\\\\\\fcnn\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Y_dict = {}
for key, item in y_dict.iteritems():
    Y_dict[key] = utils.to_categorical(item)
    #print Y_dict[key]

model = Sequential()
model.add(Dense(n_nodes, activation='relu', input_shape=in_shape))
model.add(Dense(n_nodes, activation='relu'))
model.add(Dense(n_nodes, activation='relu'))
model.add(Dense(2      , activation='softmax'))
model.summary()

model.compile(
    optimizer = Optimizer,
    loss      = loss_f,
    #metrics   =['accuracy']
)

#################################################
early_stop = EarlyStopping( monitor='val_loss',
		            patience=es_patience,
		            verbose=0,
		            mode='auto')
checkpoint = ModelCheckpoint(pth_checkpoint, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
#################################################

if train_nn:
    history = model.fit(
                          X_dict[train_str],
                          Y_dict[train_str],
                          batch_size      = n_batch_size, 
                          epochs          = n_epochs,
                          #verbose         = 2,     
                          validation_data = (X_dict[val_str], Y_dict[val_str], w_dict[val_str]), 
                          shuffle         = True,
                          sample_weight   = w_dict[train_str],
                          #initial_epoch   = 0,
                          callbacks       = [checkpoint, early_stop]
                       )
    print history


    if guess_test:    X_dict[test_str] = np.array(  [[np.random.uniform()] for i in range( len(X_dict[test_str]) )]  )


    y_pred_nn = model.predict_proba(X_dict[test_str])

    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    print 'AUC_no_weight(fcn)', metrics.roc_auc_score(Y_dict[test_str], y_pred_nn)


    auc_nn    = metrics.roc_auc_score(Y_dict[test_str], y_pred_nn, sample_weight=w_dict[test_str])
    print 'AUC(fcn):', auc_nn
#\\\\\\\\\\\\\\\\\\\\\\\fcnn\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#"""










#print X_dict[train_str]
#print y_dict[train_str]
#print w_dict[train_str]
##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BDT:
if val_aug:
    print X_dict[train_str].shape
    print y_dict[train_str].shape
    print w_dict[train_str].shape
    axs = 0
    X_dict[train_str] = np.concatenate( (X_dict[train_str], X_dict[val_str]), axis=axs )
    y_dict[train_str] = np.concatenate( (y_dict[train_str], y_dict[val_str]), axis=axs ) 
    w_dict[train_str] = np.concatenate( (w_dict[train_str], w_dict[val_str]), axis=axs )
    print X_dict[train_str].shape
    print y_dict[train_str].shape
    print w_dict[train_str].shape

##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> calling packages:
for key, item in X_dict.iteritems():    X_dict[key] = item.reshape(-1,1)
if train_bdt:
    bdt_val(
                 X_Train      = X_dict[train_str],\
                 y_Train      = y_dict[train_str],\
                 W_train      = w_dict[train_str],\
                 df_Train     = tb_dict[train_str],\
                 X_Test       = X_dict[test_str],\
                 y_Test       = y_dict[test_str],\
                 W_test       = w_dict[test_str],\
                 df_Test_orig = tb_dict[test_str],\
                 ps           = pss
           )































exit()
#||||||||||||||||||||||bdt||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
clf = DecisionTreeClassifier( 
                              max_depth                = pss['max_depth'], 
                              min_weight_fraction_leaf = pss['min_weight_fraction_leaf'],
                            )
bdt = AdaBoostClassifier( 
                          clf,
                          algorithm     = pss['algorithm'],
                          n_estimators  = pss['n_estimators'],
                          learning_rate = pss['learning_rate'],
                        )
print '>>>>>>>>>>>>>>> fitting...'
bdt.fit(X_dict[train_str], y_dict[train_str], sample_weight=w_dict[train_str])
clf.fit(X_dict[train_str], y_dict[train_str], sample_weight=w_dict[train_str])
print '<<<<<<<<<<<<<<< fit completed'
y_pred_proba_bdt           = bdt.predict_proba(X_dict[test_str])[:,1]
auc_bdt                    = metrics.roc_auc_score(y_dict[test_str], y_pred_proba_bdt, sample_weight=w_dict[test_str])
print 'AUC(BDT): ', auc_bdt
#||||||||||||||||||||||bdt||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||



















