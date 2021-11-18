import pandas as pd
import pickle

#from sklearn.metrics import roc_auc_score

class Prediction():
    def __init__(self,df,loc,model):
        self.df = df
        self.loc = loc
        self.model = model
        
        #self.Target_present = Target_present
        #self.save_to = save_to

    def predict(self):
        with open(f'{self.loc}/{self.model}','rb') as model:
            model_p=pickle.load(model)


        try:
            self.df=self.df.drop(columns='Target',axis=1)
            self.df
        except:
            pass

        
        y_pred=[]
        for i in model_p.predict(self.df):
            y_pred.append(i)

        y_prob=[]
        for i in model_p.predict_proba(self.df):
            y_prob.append(i)

        prob=[]
        for i in y_prob:
            prob.append(i[0])

        data_dict = {'Predicted target':y_pred,'Prediction probabilities':prob}
        
        df_decile = pd.DataFrame(data=data_dict)
        df_decile['Decile_rank'] = pd.qcut(df_decile['Prediction probabilities'],10,labels=False)

        df_final=self.df.join(df_decile)
        df_final=df_final.sort_values(by='Decile_rank',ascending=False)
        self.df_final = df_final.reset_index().drop(columns='index',axis=1)
        
        self.df_final.to_csv(f'{self.loc}/test_set_prediction.csv')
        
        return self.df_final

    
    def lift(self):
        try:
            self.df_final['Target']=self.df_final['Target'].astype('category')
            self.df_final['Target']=self.df_final['Target'].cat.codes
        except:
            pass

        self.df_final['Predicted target']=self.df_final['Predicted target'].astype('category')
        self.df_final['Predicted target']=self.df_final['Predicted target'].cat.codes

        top_decile = self.df_final[self.df_final['Decile_rank']==9]
        
        lift = top_decile['Prediction probabilities'].mean()/self.df_final['Prediction probabilities'].mean()

        print(f'Lift = {lift:.2f}')


    
    def profile(self):

        profile_table=self.df_final.groupby('Decile_rank').mean()
        try:
            profile_table.to_csv(f'{self.loc}/test_profile_table.csv')
        except:
            pass

        return profile_table



    def main(self):
        self.predict()
        self.lift()
        self.profile()