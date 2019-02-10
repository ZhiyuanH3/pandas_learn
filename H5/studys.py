import pandas as pd

#nsize = 500

def datagen_batch_h5(brs, store, batch_siz):
    size = store.get_storer('table').nrows
    #size = nsize
    i_start = 0
    while True:
        print 'i_start: ', i_start
        if size >= i_start+batch_siz:
            foo = store.select('table',
                               columns = brs,
                               start = i_start,
                               stop  = i_start + batch_siz)

            yield foo
            i_start += batch_siz
        else:
            i_start = 0


batch_size        = 5#512#3


st = pd.HDFStore('tst.h5')
print st.get_storer('table')
a  = datagen_batch_h5(['a'], st, batch_size)

nrows             = st.get_storer('table').nrows
print 'nrows: ', nrows
samples_per_epoch = int(nrows/batch_size) * batch_size

print samples_per_epoch

#for i in range(10):
#    print next(a)
#    print '------------------'


nbatches = int(samples_per_epoch/batch_size - 1) 
print 'nbatches: ', nbatches

for i_batch in range(nbatches):
    df = next(a) 
    print df

print '#############################'

b = a
#next(b)
for i_batch in range(nbatches):
    df = next(b)
    print df

print '!!!!!!!!!!!!!!!!!!!!!!!'
for i_batch in range(nbatches):
    df = next(b)
    print df







