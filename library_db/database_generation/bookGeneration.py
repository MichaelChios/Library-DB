import pandas as pd
import random


def processISBN(num):
    isbnList=[]
    
    while len(isbnList)<num:
        randomISBN=random.randint(1000000000000, 9999999999999)
        
        if randomISBN not in isbnList:
            isbnList.append(randomISBN)
        
    return isbnList


def processPublishDate(num,dates):
    date=[]
    
    for i in range(num):
        try:
            if pd.isna(dates[i]):
                date.append("NULL")
            elif len(dates[i])>3:
                try:
                    date.append(int(dates[i][-4:]))
                except:
                    date.append("NULL")
            else:
                date.append("NULL")
        except:
            date.append("NULL")
        
    return date


def processPublishLocation(num, locations):
    location=[]
    
    for i in range(num):
        if pd.isna(locations[i]):
            location.append("NULL")
        else:
            location.append(locations[i][2:-2])
            
            
    return location


def generate():
    df=pd.read_excel("excel_files/bookInfo.xlsx",
                       index_col=None, na_values=['NA'])
    
    
    generationOfISBN=processISBN(len(df))
    title=df.loc[:,"title"]
    publisher=df.loc[:,"publishers"]
    publish_date=processPublishDate(len(df),df.loc[:,"publish_date"])
    publish_location=processPublishLocation(len(df), df.loc[:,"publish_places"])
    subject=df.loc[:,"subjects"]
    description=df.loc[:,"description"]
    numberOfPages=df.loc[:,"number_of_pages"]
    
    bookList=[]
    for i in range(len(df)):
        tempList=[]
        
        tempList.append(generationOfISBN[i])
        tempList.append(title[i])
        
        try:
            tempList.append(publisher[i][2:-2])
        except:
            tempList.append("NULL")
            
        tempList.append(publish_date[i])
        tempList.append(publish_location[i])
        tempList.append(subject[i])
        tempList.append(description[i])
        try:
            tempList.append(int(numberOfPages[i]))
        except:
            tempList.append("NULL")
        
        try:
            #status
            status=["available", "unavailable", "personnel-only"]
            probability=[0.6,0.3,0.1]
            tempList.append(random.choices(status, probability)[0])
        except:
            print(title[i])
        
        
        try:
            #number of copies
            numberOfCopies=random.randint(15,30)
            tempList.append(numberOfCopies)
        except:
            print(title[i])
        
            
        #ISBN
        #title
        #publisher
        #publish_date
        #publish_location
        #subject
        #description
        #number_of_pages
        #status
        #number_of_copies
        
        bookList.append(tempList)
        
    columns=["ISBN","title","publisher","publish_date","publish_location","subject",
             "description","number_of_pages","status","number_of_copies"]
    df=pd.DataFrame(bookList, columns=columns)
    writer = pd.ExcelWriter('excel_files/book.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='book', index=False)
    writer.save()
        
        
        
        
        
        
        
        
        
        