import pandas as pd
import numpy  as np
import os

#pth_root    = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_for2d/'
#pth_root    = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/all_in_1/'
pth_root    = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/LLP/allInOne/'
n_jets      = 4
drop_nan    = False#True

pth         = pth_root + 'raw/' 
pth_out     = pth      + str(n_jets) + 'jets' 

mode_str    = '_pfc'#'_hla'

jet_list    = []
for i in range(n_jets):    jet_list.append('jet'+str(i))

qcd_list    = ['100to200','200to300','300to500','500to700','700to1000','1000to1500','1500to2000','2000toInf']
m_list      = [20,30,40,50]
l_list      = [500,1000,2000,5000]
versionN_b  = 'TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'
versionN_s  = 'TuneCUETP8M1_13TeV-powheg-pythia8_Tranche2_PRIVATE-MC'
tail_str    = '_skimed.h5'
sgnt_str    = 'jjjj'

h5_name_list = []
for m_i in m_list:
    for l_i in l_list:
        in_name = 'VBFH_HToSSTobbbb_MH-125_MS-'+str(m_i)+'_ctauS-'+str(l_i)+'_'+versionN_s+sgnt_str+tail_str
        h5_name_list.append(in_name) 
for qcd_i in qcd_list:
    in_name = 'QCD_HT'+qcd_i+'_'+versionN_b+sgnt_str+tail_str
    h5_name_list.append(in_name)

if not os.path.isdir(pth_out):
    os.system('mkdir '+pth_out)


def read_h5(in_str,Name):
    input_filename = pth+in_str+'/'+Name
    return pd.read_hdf(input_filename, 'df')

def stack_df(file_name):
    file_name_out = file_name.replace(sgnt_str,'_'+str(n_jets)+'j')
    print file_name_out
    stb_list      = []
    for jet_i in jet_list:
        fn        = file_name.replace(sgnt_str,'_j'+jet_i[3:]+mode_str) 
        stb_i     = read_h5(jet_i, fn)
        
        stb_i['jetIndex_0'] = int( jet_i[3:] )

        stb_list.append(stb_i)
    stb_stacked   = pd.concat(stb_list, ignore_index=True)
    stb_stacked.to_hdf(pth_out+'/'+file_name_out, key='df', mode='w', dropna=drop_nan)
    #stb_stacked.to_hdf(pth_out+'/'+file_name_out, 'table', append=False, complevel=8)
    #stb_stacked.to_hdf(pth_out+'/'+file_name_out, 'table', append=True, complevel=8)


for i in h5_name_list:    stack_df(i)



