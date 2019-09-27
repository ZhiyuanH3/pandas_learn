import pandas as pd
import numpy  as np

pre_fix                               = 'img_'

def read_h5(TB_dic, col_str):
    tb          = TB_dic[col_str]
    col_list    = list(tb.columns.values)
    #print col_list
    count       = 0
    for i in col_list:
        if pre_fix in i:    count += 1
    #print count
    n_rest = len(col_list) - count
    #print n_rest
    ## implies all non-image columns stay on right hand side of dataframe:
    stb         = tb.iloc[:, :-n_rest]
    stb_labels  = tb.iloc[:, -n_rest:] 
    #stb = np.array(stb)
    return stb, stb_labels, col_list, n_rest


def column_name_gen(n_pix, counter):
    col_list = []
    ## total num of pixels (x^2):
    n_pixs   = n_pix*n_pix
    for i in range(n_pixs):
        ## n_pixs*counter: num of pixels from previously occupied color blocks:
        str_i = pre_fix+str(i+n_pixs*counter)
        col_list.append(str_i)
    return col_list


def CombineDF_online(df_dic, color_list):
    stb_list = []
    cc       = 0
    ## loop over all colors:
    for color_i in color_list:
        ## stb_i: pd.dataframe; cl: list of column keys; n_r: number of non-image columns: 
        stb_i, _, cl, n_r = read_h5(df_dic, color_i)
        ## total number of color pixels(side width):
        n_pix             = int( np.sqrt(len(cl)-n_r) )
        print 'num of pixels for ', color_i, ': ', n_pix
        ## assign column names to dataframe:
        stb_i.columns     = column_name_gen(n_pix, cc)
        stb_list.append(stb_i)
        cc += 1
    ## stb_labels: non-image column of the dataframe:
    _, stb_labels, _, _   = read_h5(df_dic, color_list[0])
    stb_list.append(stb_labels)
        
    stb_comb       = pd.concat(stb_list, axis=1)
    #stb_comb.to_hdf(pth_out+'/'+file_name, 'table', append=True, complevel=compress_level)
    print stb_comb.shape[1]

    ## pack all columns into one tuple in a column of a dataframe(otherwise too many columns for pd.dataframe):
    ## ___________________________________________ This can be optimized!!
    df_out_t            = pd.DataFrame()
    df_out_t['tuple']   = stb_comb.apply(lambda r: tuple(r), axis=1).apply(np.array)
    #print df_out_t.astype(list) 
    print len(df_out_t['tuple'][0])
    #print len(df_out_t.astype(list))
    #(df_out_t.astype(list)).to_hdf(pth_out+'/'+file_name, 'df', mode='w', format='fixed', append=False, complevel=compress_level, complib='blosc')
    
    return df_out_t



