import pandas as pd


class Process():
    def __init__(self, df, start_date, end_date, sort_col, group_by, file_name = None, return_grouped = True, to_date_lst = []):
        self.df = df
        self.to_date_lst = to_date_lst
        self.start_date = start_date
        self.end_date = end_date
        self.sort_col = sort_col
        self.file_name = file_name
        self.group_by = group_by
        self.return_grouped = return_grouped

    def main(self):
        
        try:
            self.df = self.df.sort_values(by=self.sort_col)
        except:
            pass

        try:
            for i in self.to_date_lst:
                self.df[i] = pd.to_datetime(self.df[i].str.slice(0,10))
                self.df
        except:
            pass


        dt = []
        for i in pd.date_range(self.start_date, self.end_date):
            dt.append(str(i)[:10])
        
        calander_df = pd.DataFrame(dt, columns=['calander_dates'])
        calander_df['calander_dates'] = pd.to_datetime(calander_df['calander_dates'])
        
        self.merged = pd.merge(left=calander_df, right=self.df, left_on='calander_dates', 
                      right_on='subscription_start_date', how='outer')

        #Groupby methods
        if self.group_by == 'count':
            merged_byDT = self.merged.groupby('calander_dates').count()
        elif self.group_by == 'sum':
            merged_byDT = self.merged.groupby('calander_dates').sum()
        elif self.group_by == 'min':
            merged_byDT = self.merged.groupby('calander_dates').min()
        elif self.group_by == 'max':
            merged_byDT = self.merged.groupby('calander_dates').max()


        for i in merged_byDT.columns:
            try:
                merged_byDT[f'{i}_index'] = (merged_byDT[i]/merged_byDT[i].mean()) - 1
            except:
                pass

        merged_byDT

        if self.file_name != None:
            merged_byDT.to_csv(f'Data/{self.file_name}.csv')
        else:
            pass

        if self.return_grouped == True:
            return merged_byDT
        else:
            return self.merged
