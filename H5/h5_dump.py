import pandas as pd

nrows   = 20
df      = pd.DataFrame()
df['a'] = [i for i in range(nrows)]#[1,2,3,9,4]
df['b'] = [i for i in range(nrows)]#[4,5,6,7,8]

df.to_hdf('tst.h5','table',format='t',append=False)














