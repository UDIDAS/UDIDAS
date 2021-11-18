import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
import pickle
#import warnings
#warnings.filterwarnings('ignore')
#from sklearn.metrics import roc_auc_score

class Model():
    def __init__(self,df,sample,scoring='roc_auc',train_set=70,random_state=10,save_to=None,model_pickle=None,cv=5,n_estimators=[250],learning_rate=[.3],max_depth=[6]):
        self.df = df
        self.sample = sample
        self.train_set = train_set
        self.random_state = random_state
        self.scoring = scoring
        self.save_to = save_to
        self.pickle = model_pickle
        self.cv = cv
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth



    def XGB_best(self):
        #Train_test:
        sample = self.df.sample(frac = self.sample/100, random_state=10).sort_index()
        print(f'Size of sample is {sample.shape}')

        x=sample.drop(columns='Target',axis=1)
        y=pd.DataFrame(sample['Target'])
        self.x_tr,self.x_te,self.y_tr,self.y_te=train_test_split(x,y,stratify=y,test_size=(1-(self.train_set/100)),random_state=self.random_state)
        print('x_tr:',self.x_tr.shape,'x_te:',self.x_te.shape,'y_tr:',self.y_tr.shape,'y_te:',self.y_te.shape)
        

        #Grid search:
        xg = XGBClassifier(n_jobs=-1,random_state=10)
        xg.fit(self.x_tr,self.y_tr)

        try:
            pg={'n_estimators':self.n_estimators,'learning_rate':self.learning_rate,'max_depth':self.max_depth}
            self.xg_cv=GridSearchCV(xg,pg,cv=self.cv,scoring=self.scoring,n_jobs=-1)
            self.xg_cv.fit(self.x_tr,self.y_tr)
        except:
            pass
        
        grid_table=pd.DataFrame(data=self.xg_cv.cv_results_).drop(columns=['mean_fit_time','std_fit_time','mean_score_time','std_score_time','params'],axis=1)
        grid_table=grid_table.rename(columns={'param_learning_rate':'learning_rate','param_max_depth':'max_depth','param_n_estimators':'n_estimators'})
        grid_table.sort_values(by='rank_test_score',ascending=True)

        self.xg_best=self.xg_cv.best_estimator_
        
        print(f'Best parameters are {self.xg_cv.best_params_} with best  roc_auc score of {self.xg_cv.best_score_*100:.2f}%')
        
        #Pickle file
        try:
            with open(f'{self.save_to}/{self.pickle}','wb') as pickle_file:
                pickle.dump(self.xg_best,pickle_file)
        except:
            pass

        grid_table.to_csv(f'{self.save_to}/grid_table.csv')
        
        return grid_table


    def pred(self):
        yxg_pred=[]
        for i in self.xg_best.predict(self.x_tr):
            yxg_pred.append(i)
        yxg_prob=[]
        for i in self.xg_best.predict_proba(self.x_tr):
            yxg_prob.append(i)
        
        prob=[]
        for i in yxg_prob:
            prob.append(i[0])
        data_dict = {'Predicted target':yxg_pred,'Prediction probabilities':prob}
        
        df_decile = pd.DataFrame(data=data_dict)
        df_decile['Decile_rank'] = pd.qcut(df_decile['Prediction probabilities'],10,labels=False)

        df_final=self.x_tr.reset_index().join(self.y_tr.reset_index().drop(columns='index',axis=1))
        df_final=df_final.join(df_decile)
        df_final=df_final.sort_values(by='Decile_rank',ascending=False).drop(columns='index',axis=1)
        self.df_final = df_final.reset_index().drop(columns='index',axis=1)
        
        self.df_final.to_csv(f'{self.save_to}/train_set_prediction.csv')
        
        return self.df_final

    
    def lift(self):
        

        top_decile = self.df_final[self.df_final['Decile_rank']==9]
        
        lift = top_decile['Prediction probabilities'].mean()/self.df_final['Prediction probabilities'].mean()

        print(f'Lift = {lift:.2f}')

        #return lift


    
    def profile(self):

        profile_table=self.df_final.groupby('Decile_rank').mean()
        profile_table.to_csv(f'{self.save_to}/train_profile_table.csv')
        
        return profile_table



    def main(self):
        self.XGB_best()
        self.pred()
        self.lift()
        self.profile()

        