'''
Created on 2011-3-28

@author: ibm
'''
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured

class mysqlDB(object):
    '''
    store data using mysqlDB
    '''


    def __init__(self):
        '''
        get the configuration from settings
        '''
        
        db_url = settings.get("DB_URL")
        table_name = settings.get("DB_TABLE")
        if not db_url or not table_name:
            raise NotConfigured
        
        '''
        ???
        how to connect DB
        '''        
    def store(self,items):
        '''
        ???
        how to open the DB, then save the items
        ''' 
        