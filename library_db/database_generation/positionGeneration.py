import pandas as pd
import math

def generatePositionList(idNumber, num):
    position=[]

    count=1
    for i in range(1,math.ceil(len(idNumber)/100)+1):
        for j in range(1,101):
            if count<=len(idNumber):
                position.append([i,j,idNumber[count-1],num])
                count=count+1
            else:
                position.append([i,j,"empty", num])
                
    return position


def generate():
    holding_df=pd.read_excel("excel_files/holding.xlsx",
                       index_col=None, na_values=['NA'], usecols="A,Q")
    
    # sorted_df=holding_df.sort_values(by="library_id", inplace=False)
    # counts=holding_df["library_id"].value_counts()
    
    # sorted_df=sorted_df.loc[:,"library_id"]
    
    library_id=holding_df.loc[:,"library_id"]
    
    id0=[]
    id1=[]
    id2=[]
    id3=[]
    id4=[]
    
    for i in range(len(holding_df)):
        if library_id[i]==0:
            id0.append(i+1)
        elif library_id[i]==1:
            id1.append(i+1)
        elif library_id[i]==2:
            id2.append(i+1)
        elif library_id[i]==3:
            id3.append(i+1)
        elif library_id[i]==4:
            id4.append(i+1)
            
    position0=generatePositionList(id0,0)
    position1=generatePositionList(id1,1)
    position2=generatePositionList(id2,2)
    position3=generatePositionList(id3,3)
    position4=generatePositionList(id4,4)
    
    position=position0+position1+position2+position3+position4
    
    positionList=[]
    for i in range(len(position)):
        positionList.append([i+1, position[i][3], position[i][2],position[i][0], position[i][1]])

    columnsPosition=["position_id","library_id","holding_id","corridor","shelf"]
    df=pd.DataFrame(positionList, columns=columnsPosition)
    writer = pd.ExcelWriter('excel_files/position.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='position', index=False)
    writer.save()
    
    
    
    