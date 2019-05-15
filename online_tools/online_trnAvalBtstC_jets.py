import pandas as pd
import numpy  as np
import sys, os
sys.path.append('/home/hezhiyua/desktop/BDT_study/')
sys.path.append('/home/hezhiyua/desktop/pandas_learn/online_tools/')
sys.path.append('/home/hezhiyua/desktop/CNN_Preprocessing/Classes/')
from set_weight       import *
from DataTypes        import pkl_df


def TVTgen(
            n_pfc    = 40,
            trn_p    = '30_500',
            val_p    = '30_2000',
            tst_p    = '50_5000',
            pth_root = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/allInOne/nn_format/',
          ):
    #====settings==================================================================================================

    drop_nan      = True#False#True 
    sgn_genMatch  = False#True

    v_production  = 'v6'
    n_jets        = 4#2

    tvt_l         = ['train','val','test']
    phpt          = {}
    phpt['train'] = trn_p#'30_500'
    phpt['val']   = val_p#'30_2000'
    phpt['test']  = tst_p#'50_5000'
    ABC_str       = ''
    for i in tvt_l:    ABC_str += i+phpt[i]
    #pth_root      = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/allInOne/nn_format/'
    pth_jets      = pth_root + str(n_jets) + 'jets/'
    #pth_test_sgn  = pth_jets + '/test/'+phpt['test']+'/'
    pth           = pth_jets + v_production + '/'
    pth_dic       = {}
    for i in tvt_l:    pth_dic[i] = pth_jets + '/test/'+phpt[i]+'/'
    
    drop_lst  = ['pt']#['pt','jetIndex','PID']

    #xs  = { '50to100': 246300000, '100to200': 28060000 , '200to300': 1710000 , '300to500': 351300 , '500to700': 31630 , '700to1000': 6802 , '1000to1500': 1206 , '1500to2000': 120.4 , '2000toInf': 25.25 }
    xs  = { '100to200': 28060000 , '200to300': 1710000 , '300to500': 351300 , '500to700': 31630 , '700to1000': 6802 , '1000to1500': 1206 , '1500to2000': 120.4 , '2000toInf': 25.25 }
    #xs  = { '200to300': 1710000 , '300to500': 351300 , '500to700': 31630 , '700to1000': 6802 , '1000to1500': 1206 , '1500to2000': 120.4 , '2000toInf': 25.25 }

    xs_tot = sum(xs.values())

    file_tail = '_all_'+str(n_pfc)+'pfc'
    #====settings==================================================================================================
    
    print 'online_data running...'

    qcd_inst = pkl_df(pth_jets, 'qcd'+file_tail+'.h5')
    sgn_inst = {}
    
    for i in tvt_l:
        sgn_inst[i]  = pkl_df(pth_dic[i], 'vbf_'+phpt[i]+file_tail+'.h5')
        sgn_inst[i].gen_matching(sgn_genMatch)     
        ## gen-match in later step ... 


    #sgn_inst['test']                = pkl_df(pth_test_sgn, 'vbf_'+phpt['test']+file_tail+'.h5')
    upperLimitPerXs = None#100000

    #df_dic     = qcd_inst.splitTV(6, upperLimitPerXs, n_jets)
    """
    tvt_dic          = {}
    tvt_dic['train'] = pd.concat( [df_dic['bkg'][3], df_dic['bkg'][4], df_dic['bkg'][5], sgn_inst['train'].df] )
    tvt_dic['val']   = pd.concat( [df_dic['bkg'][1], df_dic['bkg'][2], sgn_inst['val'].df] )
    tvt_dic['test']  = pd.concat( [df_dic['bkg'][0], sgn_inst['test'].df] )
    """
    """ 
    df_sgn_dic = sgn_inst['test'].splitTV_sgn(6, upperLimitPerXs, n_jets)
    tvt_dic          = {}
    #tvt_dic['train'] = pd.concat( [df_dic['bkg'][3], df_sgn_dic['sgn'][3]] )
    tvt_dic['train'] = pd.concat( [df_dic['bkg'][3], df_dic['bkg'][4], df_dic['bkg'][5], df_sgn_dic['sgn'][3], df_sgn_dic['sgn'][4], df_sgn_dic['sgn'][5]] )
    tvt_dic['val']   = pd.concat( [df_dic['bkg'][1], df_dic['bkg'][2], df_sgn_dic['sgn'][1], df_sgn_dic['sgn'][2]] )
    tvt_dic['test']  = pd.concat( [df_dic['bkg'][0], df_sgn_dic['sgn'][0]] )
    """
    """
    #_, df_qcd_dic_j0, df_qcd_dic_j1 = qcd_inst.splitTV_1(3, upperLimitPerXs)
    _, df_qcd_dic_j0, df_qcd_dic_j1, df_qcd_dic_j2, df_qcd_dic_j3 = qcd_inst.splitTV_4(3, upperLimitPerXs)
    tvt_dic          = {}
    #tvt_dic['train'] = pd.concat( [df_qcd_dic_j0[0], df_qcd_dic_j1[0], df_qcd_dic_j1[2], sgn_inst['train'].df] )
    tvt_dic['train'] = pd.concat( [df_qcd_dic_j1[0], df_qcd_dic_j1[2], sgn_inst['train'].df] )
    tvt_dic['val']   = pd.concat( [df_qcd_dic_j0[1], df_qcd_dic_j1[1], sgn_inst['val'].df] )
    #tvt_dic['test']  = pd.concat( [df_qcd_dic_j0[2], sgn_inst['test'].df] )
    tvt_dic['test']  = pd.concat( [df_qcd_dic_j1[1], sgn_inst['test'].df] )
    """

    #df_dic = qcd_inst.splitTV_4(4, upperLimitPerXs)
    df_dic = qcd_inst.splitTV_4(4, upperLimitPerXs)
    S      = df_dic['sgn']
    B      = df_dic['bkg']
    tvt_dic          = {}
    # all 4 jets combined:
    #tvt_dic['train'] = pd.concat( [B[0][0], B[1][0], B[2][0], B[3][0], B[0][3], B[1][3], B[2][3], B[3][3], sgn_inst['train'].df] )
    #tvt_dic['val']   = pd.concat( [B[0][1], B[1][1], B[2][1], B[3][1], sgn_inst['val'].df] )
    #tvt_dic['test']  = pd.concat( [B[0][2], B[1][2], B[2][2], B[3][2], sgn_inst['test'].df] )


    ################### bdt & lola   
    # problematic 
    #tvt_dic['train'] = pd.concat( [ B[1][0], B[1][2], sgn_inst['train'].df] )
    #tvt_dic['val']   = pd.concat( [ B[0][1], B[1][1], sgn_inst['val'].df] )
    #tvt_dic['test']  = pd.concat( [ B[1][1], sgn_inst['test'].df] )

    # bdt & lola (_0)
    #tvt_dic['train'] = pd.concat( [ B[1][0], B[1][2], sgn_inst['train'].df] )
    #tvt_dic['val']   = pd.concat( [ B[0][1], sgn_inst['val'].df] )
    #tvt_dic['test']  = pd.concat( [ B[1][1], sgn_inst['test'].df] )

    # bdt & lola (_1) best so far (problematic)
    #tvt_dic['train'] = pd.concat( [ B[1][0], B[1][2], sgn_inst['train'].jets.get_group(0)] )
    #tvt_dic['val']   = pd.concat( [ B[0][0], sgn_inst['val'].jets.get_group(0)] )
    #tvt_dic['test']  = pd.concat( [ B[1][1], sgn_inst['test'].jets.get_group(0)] )

    # bdt no lola ok (_2)
    #tvt_dic['train'] = pd.concat( [ B[1][0], B[1][2], sgn_inst['train'].jets.get_group(1)] )
    #tvt_dic['val']   = pd.concat( [ B[0][0], sgn_inst['val'].jets.get_group(1)] )
    #tvt_dic['test']  = pd.concat( [ B[1][1], B[1][3], sgn_inst['test'].jets.get_group(1)] )

    ################################################ bdt no lola good (_3)
    """
    tvt_dic['train'] = pd.concat( [ B[1][0], B[1][2], sgn_inst['train'].jets.get_group(1)] )
    tvt_dic['val']   = pd.concat( [ B[1][3], sgn_inst['val'].jets.get_group(1)] )
    tvt_dic['test']  = pd.concat( [ B[1][1], sgn_inst['test'].jets.get_group(1)] )
    """

    # bdt no lola no  (_4)
    """
    tvt_dic['train'] = pd.concat( [ B[0][0], B[0][2], sgn_inst['train'].jets.get_group(0)] )
    tvt_dic['val']   = pd.concat( [ B[0][3], sgn_inst['val'].jets.get_group(0)] )
    tvt_dic['test']  = pd.concat( [ B[0][1], sgn_inst['test'].jets.get_group(0)] )
    """

    # bdt strange lola not working 0 values (_5)
    #tvt_dic['train'] = pd.concat( [ B[3][0], B[3][2], sgn_inst['train'].jets.get_group(3)] )
    #tvt_dic['val']   = pd.concat( [ B[3][3], sgn_inst['val'].jets.get_group(3)] )
    #tvt_dic['test']  = pd.concat( [ B[3][1], sgn_inst['test'].jets.get_group(3)] )
 
    """
    # bdt ok lola good not as good as 3
    tvt_dic['train'] = pd.concat( [ B[0][0], B[0][2], B[1][0], B[1][2], sgn_inst['train'].jets.get_group(0), sgn_inst['train'].jets.get_group(1)] )
    tvt_dic['val']   = pd.concat( [ B[0][3], B[1][3], sgn_inst['val'].jets.get_group(0), sgn_inst['val'].jets.get_group(1)] )
    tvt_dic['test']  = pd.concat( [ B[0][1], B[1][1], sgn_inst['test'].jets.get_group(0), sgn_inst['test'].jets.get_group(1)] )
    """


    """
    tvt_dic['train'] = pd.concat( [ B[0][0], B[1][0], B[2][0], B[3][0], B[0][2], B[1][2], B[2][2], B[3][2], sgn_inst['train'].jets.get_group(0), sgn_inst['train'].jets.get_group(1), sgn_inst['train'].jets.get_group(2), sgn_inst['train'].jets.get_group(3)] )
    tvt_dic['val']   = pd.concat( [ B[0][3], B[1][3], B[2][3], B[3][3], sgn_inst['val'].jets.get_group(0), sgn_inst['val'].jets.get_group(1), sgn_inst['val'].jets.get_group(2), sgn_inst['val'].jets.get_group(3)] )
    tvt_dic['test']  = pd.concat( [ B[0][1], B[1][1], B[2][1], B[3][1], sgn_inst['test'].jets.get_group(0), sgn_inst['test'].jets.get_group(1), sgn_inst['test'].jets.get_group(2), sgn_inst['test'].jets.get_group(3)] )
    """


    """ 
    # jet 0123
    tvt_dic['train'] = pd.concat( [ B[0][0], B[1][0], B[2][0], B[3][0], B[0][2], B[1][2], B[2][2], B[3][2], sgn_inst['train'].jets.get_group(0), sgn_inst['train'].jets.get_group(1), sgn_inst['train'].jets.get_group(2), sgn_inst['train'].jets.get_group(3)] )
    tvt_dic['val']   = pd.concat( [ B[0][3], B[1][3], B[2][3], B[3][3], sgn_inst['val'].jets.get_group(0), sgn_inst['val'].jets.get_group(1), sgn_inst['val'].jets.get_group(2), sgn_inst['val'].jets.get_group(3)] )
    tvt_dic['test']  = pd.concat( [ B[0][1], B[1][1], B[2][1], B[3][1], sgn_inst['test'].jets.get_group(0), sgn_inst['test'].jets.get_group(1), sgn_inst['test'].jets.get_group(2), sgn_inst['test'].jets.get_group(3)] )
    """


 
    """
    # jet 123
    tvt_dic['train'] = pd.concat( [ B[1][0], B[2][0], B[3][0], B[1][2], B[2][2], B[3][2], sgn_inst['train'].jets.get_group(1), sgn_inst['train'].jets.get_group(2), sgn_inst['train'].jets.get_group(3)] )
    tvt_dic['val']   = pd.concat( [ B[1][3], B[2][3], B[3][3], sgn_inst['val'].jets.get_group(1), sgn_inst['val'].jets.get_group(2), sgn_inst['val'].jets.get_group(3)] )
    tvt_dic['test']  = pd.concat( [ B[1][1], B[2][1], B[3][1], sgn_inst['test'].jets.get_group(1), sgn_inst['test'].jets.get_group(2), sgn_inst['test'].jets.get_group(3)] )
    """

    """
    # jet 01
    tvt_dic['train'] = pd.concat( [ B[0][0], B[1][0], B[0][2], B[1][2], sgn_inst['train'].jets.get_group(0), sgn_inst['train'].jets.get_group(1)] )
    tvt_dic['val']   = pd.concat( [ B[0][3], B[1][3], sgn_inst['val'].jets.get_group(0), sgn_inst['val'].jets.get_group(1)] )
    tvt_dic['test']  = pd.concat( [ B[0][1], B[1][1], sgn_inst['test'].jets.get_group(0), sgn_inst['test'].jets.get_group(1)] )
    """



    #"""
    ######################################################################### 
    B_trn_lst = []
    B_val_lst = []
    B_tst_lst = []
    S_trn_lst = []
    S_val_lst = []
    S_tst_lst = []

    ## jet 0123
    for jet_i  in range(n_jets): 
        ## training sample:
        B_trn_lst.append(B[jet_i][0])
        B_trn_lst.append(B[jet_i][2])
        ## signal for training should be gen-matched:
        sgn_trn_jet_i_tmp     = sgn_inst['train'].jets.get_group(jet_i)
        msk_match_trn         = sgn_trn_jet_i_tmp['isGenMatched'] == 1
        sgn_trn_jet_i_matched = sgn_trn_jet_i_tmp[ msk_match_trn ] 
        S_trn_lst.append(sgn_trn_jet_i_matched)
 
        ## validation sample:
        B_val_lst.append(B[jet_i][3])
        ## signal for validation should be gen-matched:
        sgn_val_jet_i_tmp     = sgn_inst['val'].jets.get_group(jet_i)
        msk_match_val         = sgn_val_jet_i_tmp['isGenMatched'] == 1
        sgn_val_jet_i_matched = sgn_val_jet_i_tmp[ msk_match_val ]
        S_val_lst.append(sgn_val_jet_i_matched)
        #S_val_lst.append(sgn_inst['val'].jets.get_group(jet_i))

        ## testing sample: 
        B_tst_lst.append(B[jet_i][1])
        S_tst_lst.append(sgn_inst['test'].jets.get_group(jet_i))

    tvt_dic['train'] = pd.concat( B_trn_lst + S_trn_lst )
    tvt_dic['val']   = pd.concat( B_val_lst + S_val_lst )
    #tvt_dic['test']  = pd.concat( B_tst_lst + S_tst_lst )
    tvt_dic['test']  = pd.concat( B_tst_lst + S_tst_lst + B_trn_lst + S_trn_lst + B_val_lst + S_val_lst )
    #########################################################################
    #"""










    #if trn_p == tst_p:
    #    tvt_dic['test']  = pd.concat( [ B[1][0], B[1][2], sgn_inst['test'].jets.get_group(1)] )

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

    if drop_nan:
         #for key in tvt_l:
         #    DF_dic[key] = DF_dic[key][ DF_dic[key]['isNaN']==False ]   
         for key in tvt_l:
             #DF_dic[key] = DF_dic[key].dropna()   
             print '--------------------------------------------------------------'
             print len(DF_dic[key])
             #print DF_dic[key].isnull().any(1).sum()   

             #print (DF_dic[key]['PX_0']>88888888).sum()   
             #print (DF_dic[key]['PX_39']>88888888).sum()
             print 'number of empty entries: ', (DF_dic[key]['E_0']==0).sum()
             print (DF_dic[key]['E_39']==0).sum()
             #print DF_dic[key] 
             #DF_dic[key] = DF_dic[key][ DF_dic[key].notnull().any(1) ]
             

    #if sgn_genMatch:
    #     for key in tvt_l:
    #         DF_dic[key] = DF_dic[key][ DF_dic[key]['isNaN']==False ]

    return DF_dic['train'], DF_dic['val'], DF_dic['test']           





if __name__ == '__main__':

    out_trn, out_val, out_tst = TVTgen(
                                        n_pfc    = 40,
                                        trn_p    = '30_500',
                                        val_p    = '40_1000',
                                        tst_p    = '30_500',
                                        pth_root = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/allInOne/nn_format/',
                                      )
 
    print '^^'
    print len(out_trn)
    print len(out_tst)










