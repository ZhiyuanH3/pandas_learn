import pandas
import numpy as np
#from preprocess_shihnew import *
from matplotlib import pyplot


def plot_gen_img(i_start, batch_size, n_pixel):

    import h5py
    import pandas
    
    pth            = '../'
    Name           = 'vbf_qcd-train-v0_40cs.h5'
    #input_filename = pth+"vbf_qcd-test-v0_40cs.h5"
    #input_filename = pth+'vbf_qcd-val-v0_40cs.h5'
    #input_filename = pth+'vbf_qcd-train-v0_40cs.h5'
    #input_filename = pth+'2d/'+Name
    #input_filename = pth+'2d/'+'color_C/pT_sorted/'+Name    
    #input_filename = pth+'2d/'+'c/'+Name     
    input_filename = pth+'2d/'+'pt/'+Name    

    folder_name    = 'png'
    store          = pandas.HDFStore(input_filename)
    #print store['table'][:16][['img_800','img_888']]
    #print store['table'].iloc[:20,400:900]
    tb = store.select('table'              ,
                       start = i_start      ,
                       stop  = i_start + batch_size)
    
    stb = tb.iloc[:, :-3]
    stb = np.array(stb)
    
    for i in range(batch_size):   
        foo    = stb[i]
          
        im_arr = np.reshape(foo, (n_pixel, -1) )
        im_arr = np.array(im_arr)
    
        fig    = pyplot.imshow(im_arr)
        pyplot.savefig(pth+folder_name+'/'+str(i)+'.png')



plot_gen_img(1, 10, 40)
