import numpy  as np
import h5py
import pandas

#pth            = '../'
#pth            = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_forLola/h5/2d/multi_cols/'
pth            = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_for2d/pfc_400/large_sgn/with_chf/output/train/'
Name           = 'vbf_qcd-train-v0_40cs.h5'
#input_filename = pth+"vbf_qcd-test-v0_40cs.h5"
#input_filename = pth+'vbf_qcd-val-v0_40cs.h5'
#input_filename = pth+'vbf_qcd-train-v0_40cs.h5'
#input_filename = pth+'2d/'+Name
input_filename = pth+Name


store = pandas.HDFStore(input_filename)

# Read the first 10 events
store.select("table",stop=10)

#print store['table'][:16][['img_800','img_888']]
print store['table'].iloc[:20,400:900]
print len(store['table'])

print store['table'].iloc[:20,0:]
