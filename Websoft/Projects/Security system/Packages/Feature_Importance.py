import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#import warnings
#warnings.filterwarnings('ignore')

class FI():
    def __init__(self,df,op=None,keep=100,test_size=30,n_estimators=10,random_state=10):
        self.df = df
        self.op=op
        self.keep = keep
        self.test_size = test_size
        self.n_estimators = n_estimators
        self.random_state = random_state
    
    def fi_rf(self):     

        #Train-Test split:
        x=self.df.drop(columns='Target',axis=1)
        y=self.df['Target']

        x_tr,x_te,y_tr,y_te=train_test_split(x,y,stratify=y,test_size=self.test_size/100)
        print('x_tr:',x_tr.shape,'x_te:',x_te.shape,'y_tr:',y_tr.shape,'y_te:',y_te.shape)
        
        #Random_forest:
        rf=RandomForestClassifier(n_estimators=self.n_estimators, n_jobs=-1, random_state=self.random_state)
        rf.fit(x_tr,y_tr)


        #Importance table:
        l_col=[]
        for i in x:
            l_col.append(i)
        
        fi_col=[]
        for i in rf.feature_importances_:
            fi_col.append(i)
        
        data={'Variables':l_col, 'Importance': fi_col}
        
        fi_table=pd.DataFrame(data).sort_values(by='Importance',ascending=False).reset_index().drop(columns='index',axis=1)[:int((self.keep/100)*len(l_col))]

        print(fi_table)

        Var_list = []
        for i in fi_table['Variables']:
            Var_list.append(i)
        final_df = pd.DataFrame(data=self.df,columns=Var_list)
        final_df['Target'] = self.df['Target']
        final_df['Target'] = final_df['Target'].replace({self.df['Target'].value_counts().idxmax():1,self.df['Target'].value_counts()[1:2].idxmax():0})
        

        if self.op != None:
            final_df.to_csv(f'{self.op}')
        else:
            pass

        return final_df