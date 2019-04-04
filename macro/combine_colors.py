import pandas as pd
import numpy  as np
import os

pth_root      = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/all_in_1/nn_format/'
#pth_root     = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_for2d/'
#pth          = pth_root + 'pfc_400/raw/output/train/test_from_50_5000/2d/'
#pth          = pth_root + 'pfc_400/raw/2jets/output/test/50_5000/test_from_1j/2d/'

#pth          = pth_root + 'pfc_400/raw/2jets/output/train/test_from_50_5000/2d/'
#pth          = pth_root + '2jets/playground/lola/train40_5000val40_2000test50_5000/2d/'
pth           = pth_root + '2jets/DPG/lola/train50_500val30_2000test50_5000/2d/'


compress_level  = 8#5
h5_name_list = ['vbf_qcd-train-v0_40cs.h5','vbf_qcd-val-v0_40cs.h5','vbf_qcd-test-v0_40cs.h5']
#color_list   = ['E','CE']
color_list   = ['E','CE','HE']
#color_list   = ['E','HE']
color_list   = ['E','CHE']
#color_list   = ['CE','HE']
color_list   = ['E','CHE','CE']
#color_list   = ['E','CHE','HE']
#color_list   = ['CE','CHE','HE']
#color_list   = ['E','E','E']



pth_out      = pth + '_'.join(color_list) 


if not os.path.isdir(pth_out):
    os.system('mkdir '+pth_out)

pre_fix = 'img_'

def read_h5(col_str,Name):
    input_filename = pth+col_str+'/'+Name
    store          = pd.HDFStore(input_filename)
    tb             = store.select('table')#              ,
    #	                           start = i_start      ,
    #	                           stop  = i_start + batch_size)
    col_list    = list(tb.columns.values)
    #print col_list

    count       = 0
    for i in col_list:
        if pre_fix in i:
            count += 1
    #print count
    n_rest = len(col_list) - count
    #print n_rest
    stb         = tb.iloc[:, :-n_rest]
    stb_labels  = tb.iloc[:, -n_rest:] 
    #stb = np.array(stb)
    return stb, stb_labels, col_list, n_rest


def column_name_gen(n_pix, counter):
    col_list = []
    n_pixs   = n_pix*n_pix
    for i in range(n_pixs):
        str_i = pre_fix+str(i+n_pixs*counter)
        col_list.append(str_i)
    return col_list


def combine_df(file_name):
    stb_list = []
    cc       = 0
    for color_i in color_list:
        stb_i, _, cl, n_r = read_h5(color_i, file_name)
        n_pix             = int( np.sqrt(len(cl)-n_r) )
        print n_pix
        stb_i.columns     = column_name_gen(n_pix,cc)
        stb_list.append(stb_i)
        cc += 1

    _, stb_labels, _, _   = read_h5(color_list[0], file_name)
    stb_list.append(stb_labels)
        
    stb_comb       = pd.concat(stb_list, axis=1)
    #stb_comb.to_hdf(pth_out+'/'+file_name, 'table', append=True, complevel=compress_level)
    print stb_comb.shape[1]

    df_out_t            = pd.DataFrame()
    df_out_t['tuple']   = stb_comb.apply(lambda r: tuple(r), axis=1).apply(np.array)
    print df_out_t.astype(list) 

    print len(df_out_t['tuple'][0])
    print len(df_out_t.astype(list))
    #exit()
    (df_out_t.astype(list)).to_hdf(pth_out+'/'+file_name, 'df', mode='w', format='fixed', append=False, complevel=compress_level, complib='blosc')
    #df_out_t.to_hdf(pth_out+'/'+file_name, 'fixed', append=True, complevel=compress_level)



for i in h5_name_list:
    combine_df(i)




