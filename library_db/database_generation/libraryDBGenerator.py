import sqlite3
import pandas as pd

# A functions that reads the contents of an 
# sql file and creates the database file
def generate():
    with sqlite3.connect("library.db") as connection:
        with open("sqlite.sql", "r") as file:
            sql = ""
            for row in file:
                sql += row
            sql = sql.split(";")
        for query in sql:
            cur = connection.cursor()
            cur.execute(query)


def loadBook():
    book_df=pd.read_excel("excel_files/book.xlsx")
    
    with sqlite3.connect("library.db") as connection:
        cursor = connection.cursor()
        
        for _, row in book_df.iterrows():
            ISBN = row["ISBN"]
            title=row["title"]
            publisher=row["publisher"]
            publish_date=row["publish_date"]
            publish_location=row["publish_location"]
            subject=row["subject"]
            description=row["description"]
            number_of_pages=row["number_of_pages"]
            status=row["status"]
            number_of_copies=row["number_of_copies"]
            cursor.execute(
                f"""INSERT INTO book
            VALUES (?,?,?,?,?,?,?,?,?,?);""", (ISBN,title,publisher,publish_date,
            publish_location, subject, description,
            number_of_pages,status,number_of_copies)
            )

        connection.commit()
    return


def loadAuthor():
    author_df=pd.read_excel("excel_files/author.xlsx")
    
    with sqlite3.connect("library.db") as connection:
        cursor = connection.cursor()
        author_id=0
        for _, row in author_df.iterrows():
            author_id=author_id+1
            author_fname = row["first_name"]
            author_lname = row["last_name"]
            
            cursor.execute(
                f"""INSERT INTO author
            VALUES (?,?,?);""", (author_id,author_fname,author_lname)
            )

        connection.commit()
    return


def loadBookAuthor():
    book_author_df=pd.read_excel("excel_files/book_author.xlsx")
    
    with sqlite3.connect("library.db") as connection:
        cursor = connection.cursor()
        
        for _, row in book_author_df.iterrows():
            author_index = row["author_index"]
            book_index = row["book_index"]
            cursor.execute(
                f"""INSERT INTO book_author
            VALUES (?,?)""", (int(author_index),int(book_index))
            )

        connection.commit()
    return
    
def loadMembership():
    membership_df=pd.read_excel("excel_files/membership.xlsx")
    
    with sqlite3.connect("library.db") as connection:

        cursor = connection.cursor()

        for _, row in membership_df.iterrows():
            membership_id=row["membership_id"]
            number_of_books=row["number_of_books"]
            number_of_renewals=row["number_of_renewals"]
            cost=row["cost"]
            eudoxus=row["eudoxus"]
            renting_dates=row["renting_dates"]
            number_of_bookings=row["number_of_bookings"]
            cursor.execute(
                f"""INSERT INTO membership
            VALUES (?,?,?,?,?,?,?);""", (membership_id, number_of_books,
            number_of_renewals, cost,eudoxus,renting_dates,number_of_bookings)
            )

        connection.commit()
    return
    

def loadLibrary():
    library_df=pd.read_excel("excel_files/library.xlsx")
    
    with sqlite3.connect("library.db") as connection:
        
        cursor=connection.cursor()
        
        for _,row in library_df.iterrows():
            library_id=row["library_id"]
            name=row["name"]
            
            cursor.execute(
                f"""INSERT INTO library
                VALUES (?,?);""", (library_id, name)
                )
        connection.commit()
    return

def loadLocation():
    location_df=pd.read_excel("excel_files/location.xlsx")
    
    with sqlite3.connect("library.db") as connection:
        
        cursor=connection.cursor()
        
        for _,row in location_df.iterrows():
            location_id=row["location_id"]
            country=row["country"]
            city=row["city"]
            street=row["street"]
            street_number=row["street_number"]
            postal_code=row["postal_code"]
            
            cursor.execute(
                f"""INSERT INTO location
                VALUES (?,?,?,?,?,?);""", (location_id, country, city,
                street, street_number, postal_code)
                )
        connection.commit()
    return


def loadPenalty():
    penalty_df=pd.read_excel("excel_files/penalty.xlsx")
    
    with sqlite3.connect("library.db") as connection:
        
        cursor=connection.cursor()
        
        for _,row in penalty_df.iterrows():
            penalty_id=row["penalty_id"]
            penalty=row["penalty"]
            
            cursor.execute(
                f"""INSERT INTO penalty
                VALUES (?,?);""", (penalty_id, penalty)
                )
        connection.commit()
    return


def loadMember():
    member_df=pd.read_excel("excel_files/member.xlsx")
    
    with sqlite3.connect("library.db") as connection:
        
        cursor=connection.cursor()
        
        for _,row in member_df.iterrows():
            AFM=row["AFM"]
            first_name=row["first_name"]
            last_name=row["last_name"]
            gender=row["gender"]
            gmail=row["gmail"]
            phone_number=row["phone_number"]
            birthdate=row["birthdate"]
            type_of_membership=row["type_of_membership"]
            penalty_id=row["penalty_id"]
            location_id=row["location_id"]
            
            cursor.execute(
                f"""INSERT INTO member
                VALUES (?,?,?,?,?,?,?,?,?,?);""", (AFM, first_name, last_name, 
                gender, gmail, phone_number, birthdate, type_of_membership,
                penalty_id, location_id)
                )
        connection.commit()
    return
    

def loadLibraryMember():
    library_member_df=pd.read_excel("excel_files/library_member.xlsx")
    
    with sqlite3.connect("library.db") as connection:
        
        cursor=connection.cursor()
        
        for _,row in library_member_df.iterrows():
            member_id=row["member_id"]
            library_id=row["library_id"]
            
            cursor.execute(
                f"""INSERT INTO library_member
                VALUES (?,?);""", (member_id, library_id)
                )
        connection.commit()
    return
    

def loadHolding():
    holding_df=pd.read_excel("excel_files/holding.xlsx")

    conn = sqlite3.connect('library.db')
    holding_df.to_sql('holding', conn, if_exists='append', index=False)
    

def loadPosition():
    position_df=pd.read_excel("excel_files/position.xlsx")
    
    conn=sqlite3.connect('library.db')
    position_df.to_sql('position', conn, if_exists='append', index=False)


def loadShare():
    share_df=pd.read_excel("excel_files/share.xlsx")
    
    conn=sqlite3.connect('library.db')
    share_df.to_sql('share', conn, if_exists='append', index=False)

def loadData():
    loadBook()
    loadAuthor()
    loadBookAuthor()
    loadMembership()
    loadLibrary()
    loadLocation()
    loadPenalty()
    loadMember()
    loadLibraryMember()
    loadHolding()
    loadPosition()
    loadShare()
    
