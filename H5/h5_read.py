import pandas as pd

i_start    = 0
batch_size = 10 

store = pd.HDFStore('tst.h5')
#table = store.get_storer('table')
df    = store.select(
                      'table',
                      #columns = brs,
                      start = i_start,
                      stop  = i_start + batch_size
                    )

print df
















