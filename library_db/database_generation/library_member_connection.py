import pandas as pd
import random


def generate():
    member_df=pd.read_excel("excel_files/member.xlsx",
                       index_col=None, na_values=['NA'], usecols="A")
    library_df=pd.read_excel("excel_files/library.xlsx",
                       index_col=None, na_values=['NA'], usecols="A")
    
    memberAFM=member_df.loc[:,"AFM"]
    
    libraryMemberList=[]
    
    for i in range(59):
        libraryMemberList.append([memberAFM[i], random.choice(library_df.loc[:,"library_id"])])
    
    columns_of_library_member=["member_id", "library_id"]
    
    df=pd.DataFrame(libraryMemberList, columns=columns_of_library_member)
    writer = pd.ExcelWriter('excel_files/library_member.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='library_member', index=False)
    writer.save()