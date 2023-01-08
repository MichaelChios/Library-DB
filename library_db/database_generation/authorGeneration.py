import pandas as pd

def processAuthorName(authorName):
    authorName=authorName.replace("'","")
    authorName=authorName.replace("[","")
    authorName=authorName.replace("]","")
    # authorName=authorName.replace(" ","")
    authorName=authorName.split(" ")
    
    
    lastName=""
    i=0
    for name in authorName:
        i=i+1
        if i==1:
            firstName=name
        elif i==2:
            lastName=name
        else:
            lastName=lastName+" "+name
    
    return [firstName, lastName]
    


def generate():
    author_df = pd.read_excel("excel_files/bookInfo.xlsx",
                       index_col=None, na_values=['NA'], usecols="C")
    
    book_df = pd.read_excel("excel_files/book.xlsx",
                            index_col=None, na_values=['NA'], usecols="A")
    book_df=book_df.loc[:,"ISBN"]
    
    author_df["authors"]=author_df["authors"].str.split(',')
    
    authors=author_df.loc[:,"authors"]
    
    processedNames=[]
    book_author_indexes=[]
    authorIndex=0
    for i in range(len(authors)):
        try:
            if pd.isna(authors[i]).all():
                authorIndex=authorIndex+1
                processedNames.append(["NULL", "NULL"])
                book_author_indexes.append([authorIndex,book_df[i]])
        except:
            continue
            
        if len(authors[i])!=1:
            for j in range(len(authors[i])-1):
                authors[i][j+1]=authors[i][j+1].replace(" ","",1)
            for author in authors[i]:
                authorIndex=authorIndex+1
                # print(i)
                [first_name, last_name]=processAuthorName(author)
                processedNames.append([first_name, last_name])
                book_author_indexes.append([authorIndex,book_df[i]])
        else:
            # print(i)
            authorIndex=authorIndex+1
            [first_name, last_name]=processAuthorName(authors[i][0])
            processedNames.append([first_name, last_name])
            book_author_indexes.append([authorIndex,book_df[i]])
        
    columns_of_author=["first_name", "last_name"]
    columns_of_book_author=["author_index", "book_index"]
    
    df=pd.DataFrame(processedNames, columns=columns_of_author)
    writer = pd.ExcelWriter('excel_files/author.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='author', index=False)
    writer.save()
    
    df=pd.DataFrame(book_author_indexes, columns=columns_of_book_author)
    writer = pd.ExcelWriter('excel_files/book_author.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='book_author', index=False)
    writer.save()
    
    
    
    
    
