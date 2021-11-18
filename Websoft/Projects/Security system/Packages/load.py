import pandas as pd

class Load:
    def __init__(self, path, dtype):
        self.path = path
        self.dtype = dtype

    def load(self):
        if self.dtype == 'csv':
            self.df=pd.read_csv(self.path)
        elif self.dtype == 'xls':
            self.df=pd.read_excel(self.path)
        elif self.dtype == 'json':
            self.df = pd.read_json(self.path)
        
        for i in self.df.columns:
            if i == 'Unnamed: 0':
                self.df = self.df.drop(columns=i,axis=1)
        
        
        return self.df


            
