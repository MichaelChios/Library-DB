import sqlite3
import random
import hashlib

class MemberMenuSQLite():
    def __init__(self, database):
        self.con = sqlite3.connect(database)

    def checkIfAFMExists(self, afm):
        cursor = self.con.cursor()
        query = f"""SELECT * FROM member
WHERE AFM = '{afm}';"""
        if (len(cursor.execute(query).fetchall()) == 0):
            return False
        else:
            return True

    def checkIfLocationExists(self, country, city, street, streetNum, pk):
        cursor = self.con.cursor()
        query = f"""SELECT location_id FROM location
WHERE country = '{country}'
AND city = '{city}'
AND street = '{street}'
AND street_number = {streetNum}
AND postal_code = {pk};"""
        if (len(cursor.execute(query).fetchall()) == 0):
            return False
        else:
            return True       
    
    def newMember(self, afm, fname, lname, gender, email, phnumber, bdate, tom, locID):
        cursor = self.con.cursor()
        sql = """INSERT INTO member(AFM, first_name, last_name, gender, email, phone_number, birthdate, type_of_membership, location_id)
VALUES(?,?,?,?,?,?,?,?,?)"""
        cursor.execute(sql, (afm, fname, lname, gender, email, phnumber, bdate, tom, locID))
        self.con.commit()

    def signUp(self, username, password):
        con2 = sqlite3.connect("database_generation/login_signin.db")
        cursor = con2.cursor()
        sql = """INSERT INTO login_signin(username, password_hashed, member_admin)
VALUES(?,?,?)"""
        cursor.execute(sql, (username, password, 0))
        con2.commit()

    def checkIfUsernameExists(self, username):
        con2 = sqlite3.connect("database_generation/login_signin.db")
        cursor = con2.cursor()
        query = f"""SELECT username FROM login_signin
WHERE username = '{username}';"""
        if (len(cursor.execute(query).fetchall()) == 0):
            return True
        else:
            return False           

    def newLocation(self, country, city, street, streetnum, pk):
        cursor = self.con.cursor()
        sql = """INSERT INTO location(country, city, street, street_number, postal_code)
VALUES(?, ?, ?, ?, ?)"""
        cursor.execute(sql, (country, city, street, streetnum, pk))
        self.con.commit()

    def returnLocationId(self, country, city, street, streetnum, pk):
        cursor = self.con.cursor()
        query = f"""SELECT location_id FROM location
WHERE country = '{country}'
AND city = '{city}'
AND street = '{street}'
AND street_number = {streetnum}
AND postal_code = {pk};"""
        results = cursor.execute(query).fetchall()
        for row in results:
            return row[0]

    def showMemberInfo(self, afm):
        cursor = self.con.cursor()
        query = f"""SELECT AFM, first_name||' '||last_name, email, type_of_membership, library_member.library_id FROM member
INNER JOIN library_member
ON AFM = member_id
WHERE AFM = '{afm}';"""
        results = cursor.execute(query).fetchall()
        for row in results:
            print("AFM: ", row[0])
            print("Full name: ", row[1])
            print("Email address: ", row[2])
            print("Membership ID: ", row[3])
            print("Library ID: ", row[4])
        print("\n")

        
#Show book's availability
    def checkBookAvailability(self, title):
        cursor = self.con.cursor()
        query = f"""SELECT book.title, library.library_name, library.library_id, COUNT(holding_id) FROM holding, library
INNER JOIN book
ON book.ISBN = holding.book_id
WHERE book_id IN
(SELECT ISBN FROM book
WHERE title LIKE '%{title}%')
AND status_of_holding = 'available'
AND library.library_id = holding.library_id
GROUP BY book.title, library.library_name;"""
        results = cursor.execute(query).fetchall()
        if (len(results) == 0):
            print(f"There are no available books with the word '{title}' in their title.\n")
            return False, None
        else:
            count=0
            for row in results:
                count+=1
                print(f"\n{row[0]}: {row[3]} available holdings in {row[1]} (Library ID: {row[2]}). ")
            print("\n")
            return True, count

    def checkBookAvailabilityMyLibrary(self, title, afm):
        cursor = self.con.cursor()
        query = f"""SELECT book.title, library.library_name, COUNT(holding_id) FROM holding
INNER JOIN book
ON book.ISBN = holding.book_id
INNER JOIN library
ON holding.library_id = library.library_id
WHERE book_id IN
(SELECT ISBN FROM book
WHERE title LIKE '%{title}%')
AND status_of_holding = 'available'
AND holding.library_id = (SELECT library_id FROM library_member
WHERE member_id = '{afm}')
GROUP BY book.title, library.library_name;"""
        results = cursor.execute(query).fetchall()
        if (len(results) == 0):
            print(f"Αυτό το βιβλίο δεν είναι διαθέσιμο στην βιβλιοθήκη σου.\n")
            return False
        else:
            for row in results:
                print(f"\n{row[0]}: {row[2]} διαθέσιμα αντίτυπα στην {row[1]}. ")
            print("\n")
            return True   

    def returnBookAndHoldingIDWithGivenLibID(self, title, afm, lib_send):
        cursor = self.con.cursor()
        query = f"""SELECT book_id, holding_id FROM holding
WHERE book_id IN
(SELECT ISBN FROM book
WHERE title LIKE '%{title}%')
AND status_of_holding = 'available'
AND library_id = {lib_send}
LIMIT 1;"""
        results = cursor.execute(query).fetchall()
        for row in results:
            return row[0], row[1]

    def returnBookAndHoldingID(self, title, afm):
        cursor = self.con.cursor()
        query = f"""SELECT book_id, holding_id FROM holding
WHERE book_id IN
(SELECT ISBN FROM book
WHERE title LIKE '%{title}%')
AND status_of_holding = 'available'
AND library_id IN
(SELECT library_id FROM library_member
WHERE member_id = '{afm}')
LIMIT 1;"""
        results = cursor.execute(query).fetchall()
        for row in results:
            return row[0], row[1]

    def newBorrow(self, afm, holdingID, bookID):
        cursor = self.con.cursor()
        sql = f"""UPDATE holding
SET AFM = '{afm}', date_of_borrowing = CURRENT_DATE, status_of_holding = 'unavailable'
WHERE holding_id = {holdingID}
AND book_id = {bookID};"""
        cursor.execute(sql)
        self.con.commit()
                
    def newShareBorrow(self, afm, holdingID, bookID, num, lib_share, lib_receive):

        #courier
        prob_courier=[0.33,0.33,0.34]
        courier=["ELTA", "ACS", "DHL"]
        prob_days=[]
        days=[]
        for i in range(num):
            prob_days.append(1/num)
            days.append(random.randint(4,7))

        courier=random.choices(courier, prob_courier)[0]
        shipment_time=random.choices(days, prob_days)[0]
        
        cursor = self.con.cursor()
        sql = f"""UPDATE holding
SET AFM = '{afm}', date_of_borrowing = CURRENT_DATE, status_of_holding = 'unavailable', courier = '{courier}', date_sent = CURRENT_DATE,
date_received = date('now', '+{shipment_time} day')
WHERE holding_id = {holdingID}
AND book_id = {bookID};"""
        cursor.execute(sql)
        self.con.commit()
        sql2 = f"""INSERT INTO share (library_id_sharing, holding_id, library_id_receiving, courier, date_sent, date_received, shipment_time)
VALUES({lib_share}, {holdingID}, {lib_receive}, '{courier}', CURRENT_DATE,
date('now', '+{shipment_time} day'), {shipment_time});"""
        cursor.execute(sql2)
        self.con.commit()
        print(f"Το βιβλίο θα είναι διαθέσιμο στην βιβλιοθήκη σου σε {shipment_time} μέρες. ")
        
#Show book's info using a keyword for the title
    def searchBookByTitle(self, key_word):
        cursor = self.con.cursor()
        query = f"""SELECT title, author.first_name||' '||author.last_name AS Author, number_of_copies, status_of_book FROM book
INNER JOIN book_author
ON book.isbn = book_author.book_id
INNER JOIN author
ON book_author.author_id = author.author_id
WHERE title LIKE '%{key_word}%';"""
        results = cursor.execute(query).fetchall()
        for row in results:
            print("Title: ", row[0])
            print("Author: ", row[1])
            print("Holdings: ", row[2])
            print("Status: ", row[3])
        print("\n")
            
#Show book's info using an author's name
    def searchBookByAuthor(self, author):
        cursor = self.con.cursor()
        query = f"""SELECT book.title, author.first_name||' '||author.last_name AS Author, COUNT(holding_id), status_of_holding FROM holding
INNER JOIN book
ON book.isbn = holding.book_id
INNER JOIN book_author
ON book.isbn = book_author.book_id
INNER JOIN author
ON book_author.author_id = author.author_id
WHERE author.first_name||' '||author.last_name LIKE '%{author}%'
GROUP BY book.title, status_of_holding, author.first_name||' '||author.last_name;"""
        results = cursor.execute(query).fetchall()
        for row in results:
            print("Title: ", row[0])
            print("Author: ", row[1])
            print("Holdings: ", row[2])
            print("Status: ", row[3])
        print("\n")

    def updateMembership(self, afm, membershipID):
        cursor = self.con.cursor()
        sql = f"""UPDATE member
SET type_of_membership = {membershipID}
WHERE AFM = '{afm}';"""
        cursor.execute(sql)
        self.con.commit()

    def viewMemberships(self):
        cursor = self.con.cursor()
        query = """SELECT * FROM membership;"""
        results = cursor.execute(query).fetchall()
        for row in results:
            print("Membership ID: ", row[0])
            print("Number of books: ", row[1])
            print("Number of renewals: ", row[2])
            print("Cost: ", row[3])
            print("Eudoxus: ", row[4])
            print("Renting dates: ", row[5])
            print("Number of bookings: ", row[6])
        print("\n")

    def insertLibraryMember(self, member_id, library_id):
        cursor = self.con.cursor()
        sql = """INSERT INTO library_member(member_id, library_id)
VALUES(?, ?)"""
        cursor.execute(sql, (member_id, library_id))
        self.con.commit()

    def myLibraryID(self, afm):
        cursor = self.con.cursor()
        query = f"""SELECT library_id FROM library_member
WHERE member_id = '{afm}';"""
        results = cursor.execute(query).fetchall()
        for row in results:
            return row[0]
