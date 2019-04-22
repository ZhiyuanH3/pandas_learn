import pandas as pd
import numpy  as np
import sys, os
sys.path.append('/home/hezhiyua/desktop/BDT_study/')
sys.path.append('/home/hezhiyua/desktop/pandas_learn/online_tools/')
sys.path.append('/home/hezhiyua/desktop/CNN_Preprocessing/Classes/')
from set_weight       import *
from DataTypes        import pkl_df


def TVTgen(n_pfc=40,
            trn_p='30_500',
            val_p='30_2000',
            tst_p='50_5000',
            pth_root='/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/allInOne/nn_format/',
            ):
    #====settings==================================================================================================
    #n_pfc         = 40
    tvt_l         = ['train','val','test']
    phpt          = {}
    phpt['train'] = trn_p#'30_500'
    phpt['val']   = val_p#'30_2000'
    phpt['test']  = tst_p#'50_5000'
    ABC_str       = ''
    for i in tvt_l:    ABC_str += i+phpt[i]
    #pth_root      = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/allInOne/nn_format/'
    pth_test_sgn  = pth_root + '2jets/' + '/test/'+phpt['test']+'/'
    pth           = pth_root + '2jets/' + 'DPG/'
    pth_dic       = {}
    for i in tvt_l:    pth_dic[i] = pth_root + '2jets/' + '/test/'+phpt[i]+'/'
    
    drop_lst  = ['pt']#['pt','jetIndex','PID']

    xs  = { '100to200': 28060000 , '200to300': 1710000 , '300to500': 351300 , '500to700': 31630 , '700to1000': 6802 , '1000to1500': 1206 , '1500to2000': 120.4 , '2000toInf': 25.25 }
    xs_tot = sum(xs.values())

    file_tail = '_all_'+str(400)+'pfc'
    #====settings==================================================================================================
    
    print 'online_data running...'

    qcd_inst = pkl_df(pth_root+'2jets/', 'qcd'+file_tail+'.h5')
    sgn_inst = {}
    for i in tvt_l:    sgn_inst[i]  = pkl_df(pth_dic[i], 'vbf_'+phpt[i]+file_tail+'.h5')
    sgn_inst['test']                = pkl_df(pth_test_sgn, 'vbf_'+phpt['test']+file_tail+'.h5')
    #_, df_qcd_dic_j0, df_qcd_dic_j1 = qcd_inst.splitTV(3)
    upperLimitPerXs = 100000
    _, df_qcd_dic_j0, df_qcd_dic_j1 = qcd_inst.splitTV(3, upperLimitPerXs)

   
    #"""
    tvt_dic          = {}
    tvt_dic['train'] = pd.concat( [df_qcd_dic_j0[0], df_qcd_dic_j1[0], df_qcd_dic_j1[2], sgn_inst['train'].df] )
    tvt_dic['val']   = pd.concat( [df_qcd_dic_j0[1], df_qcd_dic_j1[1], sgn_inst['val'].df] )
    tvt_dic['test']  = pd.concat( [df_qcd_dic_j0[2], sgn_inst['test'].df] )
    """
    tvt_dic          = {}
    tvt_dic['train'] = pd.concat( [df_qcd_dic_j0[0], sgn_inst['train'].df] )
    tvt_dic['val']   = pd.concat( [df_qcd_dic_j0[1], sgn_inst['val'].df] )
    tvt_dic['test']  = pd.concat( [df_qcd_dic_j0[2], sgn_inst['test'].df] )
    """

    
    DF_dic           = {}
    for key in tvt_l:
        tmp_inst     = onlineDF(tvt_dic[key], xs_tot)
        print tmp_inst.set_weights()
        tmp_inst.shuffle()
    
        orig_cols = list((tmp_inst.df).columns)
        col2drop  = []
        for j in drop_lst:    col2drop += [j+'_'+str(i) for i in range(n_pfc)]
        col2keep  = orig_cols
        #for i in col2drop:    col2keep.remove(i)  
       
        DF_dic[key] = ((tmp_inst.df)[ col2keep ])

    return DF_dic['train'], DF_dic['val'], DF_dic['test']           

















