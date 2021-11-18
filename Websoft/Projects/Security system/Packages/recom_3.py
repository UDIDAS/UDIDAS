from Packages.recom_2 import Recommend

class Recommend_all():
    
    def __init__(self, table_dict = {}, missing_threshold = 90.0, ex = True):
        self.table_dict = table_dict
        self.missing_threshold = missing_threshold
        self.ex = ex

    def main(self):
        rec = {}
        for key in self.table_dict:
            rec[key] = Recommend(self.table_dict[key],self.missing_threshold,self.ex).main()

        tab_tp = {}
        for i in rec.keys():
            tab_tp[i] = {Recommend(self.table_dict[i],self.missing_threshold,self.ex).main()[j]['column_name']:
                        Recommend(self.table_dict[i],self.missing_threshold,self.ex).main()[j]['variable_type'] 
                        for j in range(len(self.table_dict[i].columns))}
            
        return tab_tp, rec