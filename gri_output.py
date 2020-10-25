import pandas as pd
import sqlite3

class gri_output():
    '''
    for data save
    Attributes:
        dbpath (str): the database path
    '''
    def __init__(self, dbpath=None):
        '''
        Args:
            dbpath (str): the database path, default to None
        '''
        self.dbpath = dbpath
        self.conn = sqlite3.connect(dbpath)
    def output_base(self,data_dict,table_name='gri_base'):
        '''
        for save page to database
        Args:
            data_dict (dict): the data
            table_name (str): the table name to store the data
        '''
        df = pd.DataFrame(data_dict)
        df = df[['ORG_name','ORG_url','size','sector','country', 'region']]
        df.to_sql(name=table_name,con=self.conn,if_exists='append',index=False)
        return df
    def output_reports(self,data_dict,table_name='gri_reports'):
        tmp_dict = {'ORG_url':[],'report_url':[],'report_year':[],'report_label':[]}
        for u,rs in zip(data_dict['ORG_url'],data_dict['reports']):
            if not rs:
                continue
            for r in rs:
                tmp_dict['ORG_url'].append(u)
                for k in list(tmp_dict.keys())[1:]:
                    tmp_dict[k].append(r.get(k))
        df = pd.DataFrame(tmp_dict)
        df.to_sql(name=table_name,con=self.conn,if_exists='append',index=False)
        return df
