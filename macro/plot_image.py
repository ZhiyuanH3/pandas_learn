import pandas
import numpy as np
#from preprocess_shihnew import *
from matplotlib import pyplot



pth_root = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_for2d/2d/no_pType/'

pth = pth_root + 'dR_test/C/'
#pth = pth_root + 'dR_test/E/'


def plot_gen_img(i_start, batch_size, n_pixel):

    import h5py
    import pandas
    
    Name           = 'vbf_qcd-train-v0_40cs.h5'
    input_filename = pth+'/'+Name

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
        print im_arr
   
        fig    = pyplot.imshow(im_arr)
        pyplot.colorbar()
        pyplot.title('pt')
        pyplot.savefig(pth+folder_name+'/'+str(i)+'.png')
        pyplot.close()



def overlay(i_start, batch_size, n_pixel):

    from matplotlib.colors import LogNorm

    Name           = 'vbf_qcd-train-v0_40cs.h5'
    input_filename = pth+'/'+Name
    folder_name    = 'png'
    store          = pandas.HDFStore(input_filename)
    tb = store.select('table'              ,
                       start = i_start      ,
                       stop  = i_start + batch_size)
    


    tb_sgn = tb[tb['is_signal_new']==1]
    tb_bkg = tb[tb['is_signal_new']==0]


    def plt_in(tb, out_names):
        stb = tb.iloc[:, :-3]
        stb = np.array(stb)
        tot_im_arr     = np.zeros((40,40))
     
        if batch_size > len(stb):
            batch_size_in = len(stb)
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> batch_size_in: ', batch_size_in     
        for i in range(batch_size_in):   
            foo    = stb[i]
            im_arr = np.reshape(foo, (n_pixel, -1) )
            im_arr = np.array(im_arr)
            tot_im_arr += im_arr 
    
    
        fig    = pyplot.imshow(tot_im_arr, norm=LogNorm())
        pyplot.colorbar()
        pyplot.title('pt')
        pyplot.savefig(pth+folder_name+'/'+out_names+'_overlay_'+str(batch_size_in)+'.png')
        pyplot.close()

    #plt_in(tb,'all')    
    plt_in(tb_sgn,'sgn')
    plt_in(tb_bkg,'bkg')



n_pics    = 1
n_overlay = 9580

plot_gen_img(1, n_pics, 40)

overlay(1, n_overlay, 40)


