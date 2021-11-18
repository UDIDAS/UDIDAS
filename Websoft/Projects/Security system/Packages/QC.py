import pandas as pd
import re

class QC():
    def __init__(self,df):
        self.df = df
    
    def qc(self):

        datetime_lst = []
        for i in self.df.columns.to_list():
            try:
                match1 = re.search(r'\d\d:\d\d:\d\d',self.df[i][0])
                match2 = re.search(r'\d\d-\d\d-\d\d',self.df[i][0])
                match3 = re.search(r'\d\d/\d\d/\d\d',self.df[i][0])
                if match1 or match2 or match3:
                    datetime_lst.append(i)
                else:
                    pass
            except:
                pass       

        for i in datetime_lst:
            try:
                self.df[i] = self.df[i].astype('datetime64')
            except:
                pass
        
        description_dict={i:self.df[i].describe(datetime_is_numeric=True) for i in self.df.columns }
        qc=pd.DataFrame(description_dict)
        try:
            qc_df1=qc.loc[['25%','50%','75%','std']].T
            qc_df1=qc_df1.rename(columns={'25%':'25th percentile','50%':'50th percentile','75%':'75th percentile','std':'Standard deviation'})

        except:
            qc_df1=[] 
                
        def var(df):
            l=[]
            for i in df.columns:
                l.append(i)
            return l

        def ex(df):
            l=[]
            for i in self.df.columns:
                try:
                    l.append(df[i].value_counts().index[0])
                except:
                    l.append('empty column')
            return l

        def tp(df):
            l=[]
            for i in self.df.columns:
                l.append(df[i].dtype)
            return l

        def N(df):
            l=[]
            for i in self.df.columns:
                l.append(len(df[i]))
            return l

        def N_null(df):
            l=[]
            for i in self.df.columns:
                l.append(df[i].count())
            return l

        def unique(df):
            l=[]
            for i in self.df.columns:
                l.append(df[i].nunique())
            return l

        def m_freq(df):
            l=[]
            for i in self.df.columns:
                if df[i].nunique() != len(df[i]):
                    try:
                        l.append(df[i].value_counts().idxmax())
                    except:
                        l.append('NaN')
                else:
                    l.append('All unique values')
            return l
            
        
        def m_freq2(df):
            l=[]
            for i in self.df.columns:
                if df[i].nunique() != len(df[i]):
                    try:
                        df_val=pd.DataFrame(df[i].value_counts())
                        l.append(df_val.index[1])
                    except:
                        l.append('NaN')
                else:
                    l.append('All unique values')
            return l

        def m_freq3(df):
            l=[]
            for i in self.df.columns:
                if df[i].nunique() != len(df[i]):
                    try:
                        df_val=pd.DataFrame(df[i].value_counts())
                        l.append(df_val.index[2])
                    except:
                        l.append('NaN')
                else:
                    l.append('All unique values')
            return l
            
        def min(df):
            l = []
            for i in self.df.columns:
                try:
                    l.append(df[i].min())
                except:
                    l.append('NaN')
            return l
        
        def max(df):
            l = []
            for i in self.df.columns:
                try:
                    l.append(df[i].max())
                except:
                    l.append('NaN')
            return l
        
        dict_qc={'Variables':var(self.df),'Example':ex(self.df),'Type':tp(self.df),'N_rows':N(self.df),'Minimum':min(self.df),'Maximum':max(self.df),
                'Not-null values':N_null(self.df),'Unique values':unique(self.df),'Most frequent':m_freq(self.df),'Second most frequent':m_freq2(self.df),
                'Third most frequent':m_freq3(self.df)}
        qc_df2=pd.DataFrame(dict_qc)
        qc_df2=qc_df2.set_index('Variables')   
        
        if len(qc_df1)> 0:
            df_final=pd.concat([qc_df2,qc_df1],axis=1,sort=True)
        else:
            df_final=qc_df2

        

        return df_final