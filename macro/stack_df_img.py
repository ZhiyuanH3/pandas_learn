import pandas as pd
import numpy  as np
import os


#pth_root     = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_forLola/h5/'
pth_root     = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_for2d/'
pth          = pth_root + '2d/' + 'augmented/' + 'e/'
pth_out      = pth      + 'stacked'#'augmented'#'multi_cols/'

h5_name_list = ['vbf_qcd-train-v0_40cs.h5','vbf_qcd-val-v0_40cs.h5','vbf_qcd-test-v0_40cs.h5']
#color_list   = ['pt','ce'] # 'c'
#rot_list     = ['rot0flp1','rot1flp1']

rot_list     = []
n_rot        = 4
ele_angle    = int(360/n_rot)
for i in range(n_rot):
    str_i = 'rot_' + str(ele_angle*i)
    rot_list.append(str_i)

#rot_list = ['rot_0']


if not os.path.isdir(pth_out):
    os.system('mkdir '+pth_out)

pre_fix = 'img_'

def read_h5(col_str,Name):
    input_filename = pth+col_str+'/'+Name
    store          = pd.HDFStore(input_filename)
    tb             = store.select('table')#              ,
    #	                           start = i_start      ,
    #	                           stop  = i_start + batch_size)
    """
    col_list    = list(tb.columns.values)
    count       = 0
    for i in col_list:
        if pre_fix in i:
            count += 1
    #print count
    n_rest = len(col_list) - count
    #print n_rest
    """ 
    #stb         = tb.iloc[:, :-n_rest]
    #stb_labels  = tb.iloc[:, -n_rest:] 
    #stb = np.array(stb)
    stb = tb.iloc[:,:]
    return stb# stb_labels, col_list, n_rest

"""
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
    stb_comb.to_hdf(pth_out+'/'+file_name, 'table', append=True, complevel=5)
"""

def stack_df(file_name):
    stb_list = []
    for rot_i in rot_list:
        stb_i = read_h5(rot_i, file_name)
        stb_list.append(stb_i)

    #_, stb_labels, _, _   = read_h5(color_list[0], file_name)
    #stb_list.append(stb_labels)

    stb_stacked = pd.concat(stb_list, ignore_index=True)
    
    stb_stacked.to_hdf(pth_out+'/'+file_name, 'table', append=True, complevel=5)

for i in h5_name_list:
    #combine_df(i)
    stack_df(i)



