import pandas as pd
import numpy as np

class DP():
    def __init__(self,df,target,fillna_mean=[],fillna_median=[],fillna_0=[],drop=[],DROP_PCTNULL=0.9,TOP_BIN_FLAGS=5):
        
        #MEAN_MEDIAN_FILLNA=10,binaryFlagsAgg
        
        self.df = df
        self.target = target
        self.fillna_mean = fillna_mean
        self.fillna_median = fillna_median
        self.fillna_0 = fillna_0
        self.drop = drop
        self.DROP_PCTNULL = DROP_PCTNULL
        self.TOP_BIN_FLAGS = TOP_BIN_FLAGS

        #self.MEAN_MEDIAN_FILLNA = MEAN_MEDIAN_FILLNA
        #self.binaryFlagsAgg = binaryFlagsAgg
        
   
    
    def process(self):

        #Target variable
        print(f'Target column is {self.target}')

        #Drop columns
        for i in self.df.columns:
            if self.df[i].count()/len(self.df[i]) < self.DROP_PCTNULL and i not in (self.fillna_0 or self.fillna_mean or self.fillna_median):
                if i != self.target:
                    self.df=self.df.drop(columns=i,axis=1)
                    self.df
            else:
                pass
        
        for i in self.drop:
            if i != self.target:
                self.df = self.df.drop(columns=i,axis=1)
                self.df

        #Fill nas    
        for i in self.fillna_mean:
            try:
                if i!=self.target:
                    self.df[i].fillna(self.df[i].mean(),inplace=True)
            except:
                pass    
        for i in self.fillna_median:
            if i not in (self.fillna_mean or self.fillna_0) and i!=self.target:           
                try:
                    self.df[i].fillna(self.df[i].median(),inplace=True)
                except:
                    pass

        for i in self.fillna_0:
            if i not in (self.fillna_mean or self.fillna_median) and i != self.target:
                self.df[i].fillna(0,inplace=True)        

        #Dummy
        
        binaryFlags = []
        
        for i in self.df.columns:
            if i not in self.target and self.df[i].dtype == 'object':
                binaryFlags.append(i)

        
        for i in binaryFlags:
            try:    
                if self.df[i].dtype == object and i not in self.target:
                    if self.df[i].value_counts().count() <= self.TOP_BIN_FLAGS:
                        self.df=pd.get_dummies(self.df,columns=[i])
                    if self.df[i].value_counts().count() > self.TOP_BIN_FLAGS:
                        top_vals=self.df.sort_index(ascending=False).groupby(i).count().reset_index()[:(self.TOP_BIN_FLAGS-1)][i]
                        pd.get_dummies(self.df[self.df[i].isin(top_vals)][i])
                        for j in top_vals:
                            self.df[i+f'_{j}']=np.where(self.df[i]==j,1,0)
                            self.df[i+'_other']=np.where(self.df[i].isin(top_vals),1,0)
                    self.df=self.df.drop(columns=i,axis=1)
                    self.df
            except:     
                    pass
        
        self.df = self.df.rename(columns={self.target:'Target'})


        return self.df
