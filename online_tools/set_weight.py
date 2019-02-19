import pandas as pd
import numpy  as np

from sklearn.utils import shuffle


#def calc_weights(row,n_sgn,xs_tot,cat_n_dic):
#    xs = row['xs']
#    if   row['is_signal_new'] == 1:    return 1./float(n_sgn)
#    elif row['is_signal_new'] == 0:    return xs/float(xs_tot * cat_n_dic[xs])





class onlineDF:

    def __init__(self,df,xs_tot):#,xs_dic):
        self.sgn_str   = 'is_signal_new' 
        #self.xs_dic    = xs_dic
        #self.xs_tot    = sum( xs_dic.values() ) 
 
        self.xs_tot    = xs_tot

        self.df        = df
        self.n_events  = df.shape[0]
        self.n_sgn     = df[ df[self.sgn_str]==1 ].count()[self.sgn_str] 
        self.n_bkg     = df[ df[self.sgn_str]==0 ].count()[self.sgn_str]
        self.cat_n_dic = dict(df.groupby('xs').size() )
 
        # Testing~~~~  
        #self.xs_tot    = sum(self.cat_n_dic)    
        self.w_dic     = {i:  i/float(self.xs_tot * self.cat_n_dic[i])  for i in self.cat_n_dic}          


    def set_weights(self):
        def calc_weights(row):
            xs = row['xs']
            if   row['is_signal_new'] == 1:    return 1./float(self.n_sgn)
            elif row['is_signal_new'] == 0:    return xs/float(self.xs_tot * self.cat_n_dic[xs])
        (self.df)['weight'] = (self.df).apply( lambda row: calc_weights(row), axis=1 )
        return (self.df)['weight']

    def shuffle(self,seed=0):    self.df = shuffle(self.df, random_state=seed)


    def set_weights_q(self):
        df  = self.df 

        if self.n_sgn != 0     :    df.loc[  df['is_signal_new'] == 1, 'weight'  ] = 1./float(self.n_sgn)  
        for i in self.cat_n_dic:    df.loc[  df['xs'] == i, 'weight'  ]            = self.w_dic[i]
            
        return (self.df)['weight']









if __name__ == '__main__':
  
    dff                  = pd.DataFrame()
    dff['a']             = [1,2,3,4]
    dff['xs']            = [2,3,4,5]
    dff['is_signal_new'] = [1,1,0,0]

    xss = {1:2,2:4,3:6,4:5,5:10}

    oli = onlineDF(dff,xss) 

    print oli.n_events
    print oli.n_sgn
    

    print oli.set_weights()






















