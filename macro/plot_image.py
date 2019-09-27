from keras.layers import Dense
import pandas
import numpy as np
#from preprocess_shihnew import *
from matplotlib import pyplot


title    = 'Energy'
#title    = 'Energy*If_Charged'

#pth_root = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_for2d/2d/no_pType/'
pth_root = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_for2d/pfc_400/large_sgn/'
#pth = pth_root + 'dR_test/C/'
#pth = pth_root + 'dR_test/E/'
#pth = pth_root + '2d/E/'
#pth = pth_root + '2d/C/'
pth = pth_root + '2d/pixels_40/no_preprocess/E/'

#pth = pth_root + '2d/pixels_40/no_preprocess/C/'

pth = '/beegfs/desy/user/hezhiyua/MA/TVT/'


def plot_gen_img(i_start, batch_size, n_pixel):

    import h5py
    import pandas
    
    Name           = 'vbf_qcd-train-v0_40cs.h5'
    Name = 'train.h5'
    input_filename = pth+'/'+Name

    folder_name    = 'png'
    store          = pandas.HDFStore(input_filename)
    #print store['table'][:16][['img_800','img_888']]
    #print store['table'].iloc[:20,400:900]
    tb = store.select('df',#'table'              ,
                       start = i_start      ,
                       stop  = i_start + batch_size)
    

    #tb = tb[tb['is_signal_new']==1]
    #print tb
    #stb = tb.iloc[:, :-3]
    stb = tb.iloc[:, 2:]
    
    stb = np.array(stb)
    
    for i in range(batch_size):   
        foo    = stb[i]
        #print foo  
        im_arr = np.reshape(foo, (n_pixel, -1) )
        im_arr = np.array(im_arr)
        print im_arr
   
        
        fig    = pyplot.imshow(im_arr)
        pyplot.colorbar()
        pyplot.title(title)
        #pyplot.savefig(pth+folder_name+'/'+str(i)+'.png')

        pyplot.savefig(pth+'/'+'_1event_'+str(i)+'.png')
        pyplot.close()



def overlay(i_start, batch_size, n_pixel):

    from matplotlib.colors import LogNorm

    Name           = 'vbf_qcd-train-v0_40cs.h5'
    Name = 'train.h5'
    input_filename = pth+'/'+Name
    folder_name    = 'png'
    store          = pandas.HDFStore(input_filename)
    tb = store.select('df',#'table'              ,
                       start = i_start      ,
                       stop  = i_start + batch_size)
    

    #print tb
    #exit()

    tb_sgn_orig = tb[tb['is_signal_new']==1].copy()
    tb_bkg_orig = tb[tb['is_signal_new']==0].copy()
    #tb_bkg_orig = tb_bkg_orig[tb_bkg_orig['weight']>0.01].copy()
    #tb_bkg_orig = tb_bkg_orig[tb_bkg_orig['weight']<0.01].copy()

    #tb_bkg_orig = tb_bkg_orig[tb_bkg_orig['weight']<0.0001].copy()


    #print tb_bkg

    tb_sgn = tb_sgn_orig 
    tb_sgn = tb_sgn_orig.apply(lambda x: x * x['weight'] * 1, axis=1)  
    tb_bkg = tb_bkg_orig.apply(lambda x: x * x['weight'] * 1, axis=1) 
    #tb_bkg = tb_bkg_orig.apply(lambda x: x * 1, axis=1)    

    #print tb_bkg
    #print tb_bkg_orig
    #exit() 


    def plt_in(tb, out_names):
        print tb.shape
        #print tb
        stb        = tb.iloc[:, 2:]

        #stb        = tb.iloc[:, :-3]
        stb        = np.array(stb)
        tot_im_arr = np.zeros((n_pixel,n_pixel))
     
        if batch_size > len(stb):
            batch_size_in = len(stb)
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> batch_size_in: ', batch_size_in     
        else: batch_size_in = batch_size
        for i in range(batch_size_in):   
            foo         = stb[i]
            im_arr      = np.reshape(foo, (n_pixel, -1) )
            im_arr      = np.array(im_arr)
            tot_im_arr += im_arr 
    
        # Plotting:
        fig    = pyplot.imshow(tot_im_arr, norm=LogNorm())
        #fig    = pyplot.imshow(tot_im_arr) 
        pyplot.colorbar()
        pyplot.title(title)
        #pyplot.savefig(pth+folder_name+'/'+out_names+'_overlay_'+str(batch_size_in)+'.png')
        pyplot.savefig(pth+'/'+out_names+'_overlay_'+str(batch_size_in)+'.png')
        pyplot.close()

    #plt_in(tb,'all')    
    #plt_in(tb_sgn,'sgn')
    plt_in(tb_bkg,'bkg')



n_pics    = 1
n_overlay = 1#165#400#200#165#180#199#150#100#1#200#40000#10000#9580

plot_gen_img(1, n_pics, 25)

overlay(1, n_overlay, 25)


