import numpy  as np
import h5py
import pandas as pd


tvt            = 'train'#'test'#'val'
#pth            = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_for2d/bugged/pfc_40/lola/c/'
#pth            = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/all_in_1/nn_format/2jets/playground/lola/train40_5000val40_2000test50_5000/2d/' + 'E_CE_HE/'
pth            = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/all_in_1/nn_format/2jets/playground/lola/train40_5000val40_2000test50_5000/'

Name           = 'vbf_qcd-'+tvt+'-v0_40cs.h5'
input_filename = pth+Name


if_2d = 0#1

if not if_2d:
    store = pd.HDFStore(input_filename)
    # Read the first 10 events
    store.select("table",stop=10)
    #print store['table'][:16][['img_800','img_888']]
    print store['table'].iloc[:20,400:900]
    print len(store['table'])
    print store['table'].iloc[:20,0:]

    df = store['table']
    
    print df.shape
    print '#sgn: ', df[df['is_signal_new']==1].shape
    print '#bkg: ', df[df['is_signal_new']==0].shape


else:
    df = pd.read_hdf(input_filename, 'df')
    
    print df
    print df['tuple']
    tmp = df[0:8]
    print tmp
    
    print '>>>>>>>>>>>>>>>>> debug:'
    lst = tmp['tuple'][0]
    print len(lst)
    print len(tmp['tuple'][1])
    print pd.DataFrame(tmp.tuple.values.tolist(),index=tmp.index)

