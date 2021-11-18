from Packages.QC import QC
import pandas as pd


class Recommend():
    
    def __init__(self,df,missing_threshold,ex=True):
        self.df = df
        self.missing_threshold = missing_threshold
        self.ex = ex
        

    def main(self):
        data_qc = QC(self.df).qc()
        
        def ex(i):
            data_qc['Example'] = data_qc['Example'].astype(str)
            return data_qc['Example'][i]
        
        def dtype(i):
            
            if data_qc['Type'][i] == 'int64' or data_qc['Type'][i] == 'int32' or data_qc['Type'][i] == 'int':
                return 'integer'
            elif data_qc['Type'][i] == 'float64' or data_qc['Type'][i] == 'float32' or data_qc['Type'][i] == 'float':
                return 'float'
            elif data_qc['Type'][i] == 'object':
                return 'string'
            elif data_qc['Type'][i] == 'datetime64[ns]' or data_qc['Type'][i] == 'datetime64' or data_qc['Type'][i] == 'datetime32' or data_qc['Type'][i] == 'datetime32[ns]' or data_qc['Type'][i] == 'datetime':
                return 'datetime'
           
        def missing(i):
            missing_amt = data_qc['N_rows'][i] - data_qc['Not-null values'][i]
            if missing_amt > 0:
                return 'missing'
            else:
                return 'filled'

        def missing_pct(i):
            missing_pct = ((data_qc['N_rows'][i] - data_qc['Not-null values'][i])/data_qc['N_rows'][i])*100
            return f'{missing_pct}'
        
        def fill_opt(i):
            missing_pct = ((data_qc['N_rows'][i] - data_qc['Not-null values'][i])/data_qc['N_rows'][i])*100
            if data_qc['Type'][i] != 'object' and dtype(i) != 'datetime':
                if missing_pct >= self.missing_threshold:
                    return ['0','drop']
                elif 0 < missing_pct < self.missing_threshold:
                    return ['median','mean']
                if missing_pct == 0:
                    return None         
            elif data_qc['Type'][i] == 'object':
                if missing_pct == 0:
                    return None
                else:
                    return ['drop']

        def fill_val(i):
            if missing(i) == 'filled':
                return 'np.nan'
            else:
                if fill_opt(i) == 0 or fill_opt(i) == ['0','drop']:
                    return ["0"]
                elif fill_opt(i) ==['median','mean']:
                    return [f"{self.df[i].median()}", f"{self.df[i].mean()}"]
        
        rec = []
        for i in data_qc.index.to_list():
            if missing(i) == 'missing':
                if self.ex == True:
                    rec.append({'column_name':i, 'example':f'{ex(i)}', 'variable_type':dtype(i), 'percentage_missing':missing_pct(i), 
                    'recommended_fill':[{'condition':missing(i), 'recommended_fill_option':fill_opt(i),
                                        'recommended_fill_value':fill_val(i)}]})
                else:
                    rec.append({'column_name':i, 'variable_type':dtype(i), 'percentage_missing':missing_pct(i),
                    'recommended_fill':[{'condition':missing(i), 'recommended_fill_option':fill_opt(i),
                                        'recommended_fill_value':fill_val(i)}]})
            else:
                if self.ex == True:    
                    rec.append({'column_name':i, 'example':f'{ex(i)}', 'variable_type':dtype(i), 'percentage_missing':missing_pct(i),
                    'recommended_fill':[]})
                else:
                    rec.append({'column_name':i, 'variable_type':dtype(i), 'percentage_missing':missing_pct(i),
                    'recommended_fill':[]})


        return rec