import pandas as pd
import random
from datetime import datetime, timedelta


def generateShare(index,library_id):
    library_id_receiving=library_id[index]
    library_ids=[0,1,2,3,4]
    library_ids.remove(library_id_receiving)
    library_id_sharing=random.choice(library_ids)
    
    #we started sharing the last 2 years
    start_date = datetime.now().date() - timedelta(days=730)
    end_date = datetime.now().date()
    
    #courier
    probability=[0.33,0.33,0.34]
    courier=["ELTA", "ACS", "DHL"]
    days=[4,5,6]
    
    courier=random.choices(courier,probability)[0]
    shipment_time=random.choices(days,probability)[0]
    
    date_sent = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    date_received = date_sent + timedelta(days=shipment_time)
    
    return [library_id_sharing, index, library_id_receiving, courier, 
            date_sent, date_received, shipment_time]



def generate():
    position_df = pd.read_excel("excel_files/position.xlsx",
                            index_col=None, na_values=['NA'])
    holding_df = pd.read_excel("excel_files/holding.xlsx",
                            index_col=None, na_values=['NA'])
    
    library_id=position_df.loc[:,"library_id"]
    holding_id=position_df.loc[:,"holding_id"]
    
    shareList=[]
    indexList=[]
    #lets say only 1000 books were shared between libraries
    for i in range(1000):
        succeed=0
        while(succeed!=1):
            index=random.randint(1,len(holding_df))
            if holding_id[index]!="empty" and index not in indexList:
                succeed=1
                shareList.append(generateShare(index,library_id))
            indexList.append(index)
        
    
    columns=["library_id_sharing", "holding_id", "library_id_receiving",
             "courier", "date_sent", "date_received", "shipment_time"]
    df=pd.DataFrame(shareList, columns=columns)
    writer = pd.ExcelWriter('excel_files/share.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='share', index=False)
    writer.save()
        
        
