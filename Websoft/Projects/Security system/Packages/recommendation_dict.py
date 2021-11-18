from Packages.QC import QC
import pandas as pd


class Recommend():
    
    def __init__(self,df,missing_threshold=90.0):
        self.df = df
        self.missing_threshold = missing_threshold

    def main(self):
        data_qc = QC(self.df).qc()

        def missing(i):
            missing_pct = ((data_qc['N_rows'][i] - data_qc['Not-null values'][i])/data_qc['N_rows'][i])*100
            return missing_pct

        def fill(i):
            if data_qc['Type'][i] != 'object':
                if missing(i) >= self.missing_threshold:
                    return 0
                elif 0 < missing(i) < self.missing_threshold and data_qc['Unique values'][i] >= data_qc['Not-null values'][i]*.70:
                    return 'Mean'
                elif 0 < missing(i) < self.missing_threshold and data_qc['Unique values'][i] <= data_qc['Not-null values'][i]*.30:
                    return 'Median'
                if missing(i) == 0:
                    return 'No fill required'
            else:
                return 'Dummies will fill missing values'

        def logic(i):
            if fill(i) == 0:
                return 'Missing percentage > Missing threshold value'
            elif fill(i) == 'Mean':
                return '0 < Missing percentage < Missing threshold value and Lots of unique values'
            elif fill(i) == 'Median':
                return '0 < Missing percentage < Missing threshold value and very few unique values'
            elif fill(i) == 'No fill required':
                return 'There are no missing values in this column'
            else:
                return fill(i)

        def fill_value(i):
            if fill(i) == 0:
                return 0
            elif fill(i) == 'Mean':
                return self.df[i].mean()
            elif fill(i) == 'Median':
                return self.df[i].median()
            else:
                return None
        
        
        rec_dict = []
        for i in data_qc.index.to_list():
            rec_dict.append({'Variable':i, 'Example':data_qc['Example'][i], 'Type':data_qc['Type'][i],
            'N_rows':data_qc['N_rows'][i], 'Missing percentage':missing(i), 'Recommended fill':fill(i), 'Recommended values':fill_value(i),
            'Logic':logic(i) })

        return rec_dict