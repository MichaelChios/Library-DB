import pandas as pd
import random
from datetime import datetime, timedelta


def edition(title, revision, copies):
    revisionList=[]
    
    for i in range(len(title)):
        for j in range(copies[i]):
            try:
                revisionList.append(random.randint(1, revision[i]))
            except:
                revisionList.append(random.randint(1, 4))
    
    return revisionList


def generateDate():
    year=random.randint(2011, 2022)
    month=random.randint(1,12)
    if month in [1,3,5,7,8,10,12]:
        day=random.randint(1,31)
    elif month in [4,6,9,11]:
        day=random.randint(1,30)
    elif year%4==0:
        day=random.randint(1,29)
    else:
        day=random.randint(1,28)
        
    if day<10:
        day="0"+str(day)
    if month<10:
        month="0"+str(month)
    
    date=str(year)+"-"+str(month)+"-"+str(day)
    
    return date

def checkout():
    probability=[0.4,0.6]
    booked=["never", "sometime"]
    checkedOut=random.choices(booked,probability)[0]
    
    if checkedOut=="never":
        return ["NULL",0,0]
    elif checkedOut=="sometime":
        date_last_checked=generateDate()
        total_checkouts=random.randint(8, 15)
        total_renewals=random.randint(1,7)
    
    return [date_last_checked, total_checkouts, total_renewals]



def generateBorrow(holdings,numberOfBooks, AFM):
    
    #we will generate a random date between 1 year ago and now
    start_date = datetime.now().date() - timedelta(days=365)
    end_date = datetime.now().date()
    
    numberOfBooksBurrowedLeft={}
    for i in range(len(numberOfBooks)):
        #initialize dictionary
        #every member has # number of books left to borrow
        if numberOfBooks[i]==0:
            numberOfBooksBurrowedLeft[i]=3
        elif numberOfBooks[i]==1:
            numberOfBooksBurrowedLeft[i]=5
        elif numberOfBooks[i]==2:
            numberOfBooksBurrowedLeft[i]=5
        elif numberOfBooks[i]==3:
            numberOfBooksBurrowedLeft[i]=2            
    
    for i in range(300):
        
        if holdings[i][5]=="NULL":
            borrow_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            
            succeed=0
            #we have 59 members
            while(succeed!=1):
                randomMember=random.randint(0, 58)
                if numberOfBooksBurrowedLeft[randomMember]>0:
                    if numberOfBooks[randomMember] in [0,1,2]:
                        return_date = borrow_date + timedelta(days=27)
                    elif numberOfBooks[randomMember]==3:
                        return_date = borrow_date + timedelta(days=7)
                        
                    holdings[i].append(AFM[randomMember])
                    holdings[i].append(borrow_date)
                    holdings[i].append(return_date)
                    
                    succeed=1
                    numberOfBooksBurrowedLeft[randomMember]=numberOfBooksBurrowedLeft[randomMember]-1
                    
        else:
            holdings[i].append("NULL")
            holdings[i].append("NULL")
            holdings[i].append("NULL")
    
    return holdings


def returnBooksToOriginalLibrary(holdingsDate, index):
    probability=[0.33,0.33,0.34]
    courier=["ELTA", "ACS", "DHL"]
    days=[4,5,6]
    
    probability_return=[0.2,0.15,0.15,0.10,0.10,0.10,0.10,0.05,0.05]
    days_return=[1,2,3,4,5,6,7,15,30]
    
    library_id_returning=random.randint(0,4)
    library_id_receiving=random.randint(0,4)
    
    while library_id_returning==library_id_receiving:
        library_id_receiving=random.randint(0,4)
    
    
    return [library_id_returning, library_id_receiving, random.choices(courier,probability)[0], 
            holdingsDate+timedelta(days=random.choices(days_return,probability_return)[0]), holdingsDate+timedelta(days=random.choices(days,probability)[0]), index]


def assignBooksToLibraries(holdings):
    
    for i in range(len(holdings)):
        # print(i)
        if holdings[i][12]!="NULL":
            holdings[i].append(holdings[i][12])
        else:
            holdings[i].append(random.randint(0, 4))
    
    return holdings


def returnOfBook(holding):
    for i in range(150):
        try:
            if holding[i][12]!="NULL":
                holding[i].append(holding[i][8])
                holding[i].append(holding[i][11])
                holding[i].append(holding[i][14])
            else:
                holding[i].append("NULL")
                holding[i].append("NULL")
                holding[i].append("NULL")
        except:
                holding[i].append("NULL")
                holding[i].append("NULL")
                holding[i].append("NULL")
        
    
    return holding


def generate():
    book_df = pd.read_excel("excel_files/book.xlsx",
                            index_col=None, na_values=['NA'])
    bookInfo_df=pd.read_excel("excel_files/bookInfo.xlsx",
                            index_col=None, na_values=['NA'])
    member_df=pd.read_excel("excel_files/member.xlsx",
                            index_col=None, na_values=['NA'])
    
    
    #book_df
    ISBN=book_df.loc[:,"ISBN"]
    numberOfCopies=book_df.loc[:,"number_of_copies"]
    status=book_df.loc[:,"status"]
    titles_book=book_df.loc[:,"title"]
    
    
    #bookInfo_df
    revision=bookInfo_df.loc[:,"revision"]
   
    #member_df
    AFM=member_df.loc[:,"AFM"]
   
    
   
    available_unavailable=["available", "unavailable"]
    
    holdingList=[]
    #Generation of all book copies with holding_id, ISBN and status
    autoIncrement=0
    for i in range(len(book_df)):
        for j in range(numberOfCopies[i]):
            autoIncrement=autoIncrement+1
            
            if status[i]=="available":
                probability=[0.65,0.35]
                statusHolding=(random.choices(available_unavailable, probability)[0])
            elif status[i]=="unavailable":
                statusHolding=available_unavailable[1] #unavailable
            elif status[i]=="personnel-only":
                probability=[0.4, 0.6]
                statusHolding=(random.choices(available_unavailable, probability)[0])
            
            holdingList.append([autoIncrement, ISBN[i], statusHolding])
    
    #revision
    revisionList=edition(titles_book, revision, numberOfCopies)
    for i in range(len(holdingList)):
        holdingList[i].append(revisionList[i])
    
    #language
    language=["Greek", "English", "Spanish", "Italian"]
    for i in range(len(holdingList)):
        probability=[0.75, 0.15, 0.05, 0.05]
        holdingList[i].append(random.choices(language, probability)[0])
    
    
    #check-outs
    checkOutList=[]
    for i in range(len(holdingList)):
        checkOutList.append(checkout())
        for j in range(3):
            holdingList[i].append(checkOutList[i][j])
            
    #borrowing
    holdingList=generateBorrow(holdingList,member_df.loc[:,"type_of_membership"], AFM)
    
    #let's say only 10 books need to be returned to original library
    count=0
    i=0
    returningBooks=[]
    while count<10:
        if holdingList[i][10]!="NULL":
            returningBooks.append(returnBooksToOriginalLibrary(holdingList[i][10],i))
            count=count+1
        i=i+1
    
    count=0
    for i in range(len(holdingList)):
        try:
            if i==returningBooks[count][5]:
                for j in range(5):
                    holdingList[i].append(returningBooks[count][j])
                count=count+1
            else:
                for j in range(5):
                    holdingList[i].append("NULL")
        except:
            for j in range(5):
                holdingList[i].append("NULL")
        
        
    for i in range(300,len(holdingList)):
        for j in range(3):
            holdingList[i].append("NULL")
    
    
    #assign all books to libraries
    holdingList=assignBooksToLibraries(holdingList)
            
    
    #return of books that got borrowed
    holdingList=returnOfBook(holdingList)
    for i in range(150,len(holdingList)):
        for j in range(3):
            holdingList[i].append("NULL")
    
    columns=["holding_id", "book_id", "status_of_holding", "edition_of_holding", "language_written", "date_last_checked_out",
             "total_checkouts", "total_renewals", "AFM", "date_of_borrowing", "date_of_return",
             "library_id_returning", "library_id_receiving", "courier", "date_sent", "date_received",
             "library_id", "member_id", "library_id_returned", "date_of_holding_return"]
    df=pd.DataFrame(holdingList, columns=columns)
    writer = pd.ExcelWriter('excel_files/holding.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='holding', index=False)
    writer.save()
        
    