import sqlite3

class adminMenu():
    def __init__(self, database):
        self.con = sqlite3.connect(database)
        while(True):
            self.choice = self.query_choice()
            if (self.choice == "1"):
                self.numBooksHoldings()
            elif (self.choice == "2"):
                print("Αριθμός αντίτυπων: ")
                num=input()
                print("\n")
                self.findTitles("available", num)
            elif (self.choice == "3"):
                self.findMaxBor()
            elif (self.choice == "4"):
                self.findMemberID()
            elif (self.choice == "5"):
                print("Διάστημα ημερομηνιών (YYYY-MM-DD YYYY-MM-DD): ")
                self.answer=input()
                while len(self.answer)!=21:
                    print("Λάθος εκχώρηση ημερομηνιών!")
                    print("YYYY-MM-DD YYYY-MM-DD")
                    self.answer=input()
                self.findShares("Βιβλιοθήκη και Κέντρο Πληροφορίας Πανεπιστήμιο Πατρών", self.answer[0:10], self.answer[11:])
            elif (self.choice == "6"):
                print("Write your query: ")
                self.answer=input()
                print("\n")
                self.specialQuery(self.answer)
            else:
                break

    def query_choice(self):
        print("Query 1: Πόσα βιβλία και αντίτυπα αποθηκεύονται στη ΒΔ.")
        print("Query 2: Βρείτε τους τίτλους και τον αριθμό των πρώτων 5 αντιτύπων των διαθέσιμων\
 βιβλίων που έχουν ακριβώς # αντίτυπα. Να ταξινομηθούν σε αλφαβητική σειρά.")
        print("Query 3: Βρείτε από ποια βιβλιοθήκη γίνονται οι περισσότεροι δανεισμοί και πόσοι είναι αυτοί.")
        print("Query 4: Εμφανίστε τους κωδικούς των μελών που έχουν δανειστεί βιβλία,\
              τα οποία αυτή τη στιγμή δεν είναι ακόμη υποχρεωμένοι να επιστρέψουν.")
        print("Query 5: Βρείτε τους τίτλους των βιβλίων τα οποία μοιράστηκε η βιβλιοθήκη\
 του Πανεπιστημίου Πατρών κάποια περίοδο.")
        print("Query 6: Αξιοποίηση άλλου query.")
        print("Type 1-6 to choose a query or type 'exit' to end the program.")
        c = input()
        print("\n")
        return c

    def numBooksHoldings(self):
        cursor = self.con.cursor()
        query = """SELECT COUNT(*), SUM(number_of_copies) FROM book;"""
        results = cursor.execute(query).fetchall()
        for row in results:
            print(f"Number5 of books: {row[0]}")
            print(f"Number of holdings: {row[1]}\n")
    
    def findTitles(self, st, noc):
        cursor = self.con.cursor()
        query = f"""SELECT title, number_of_copies FROM book
WHERE status_of_book = '{st}'
AND number_of_copies == {noc}
ORDER BY title ASC
LIMIT 5;"""
        results = cursor.execute(query).fetchall()
        for row in results:
            print(f"Title: {row[0]}")
            print(f"Number of copies: {row[1]}\n")

    def findMemberID(self):
        cursor = self.con.cursor()
        query = f"""SELECT DISTINCT(afm) FROM holding
WHERE DATE(date_of_return) > CURRENT_DATE;"""
        results = cursor.execute(query).fetchall()
        for i in range (len(results)):
            print(results[i][0])
        print("\n")
        
    def findMaxBor(self):
        cursor = self.con.cursor()
        query = f"""SELECT library_name, COUNT(holding.date_of_borrowing) AS num_of_borrowings
FROM library
INNER JOIN holding
ON library.library_id = holding.library_id
WHERE holding.date_of_borrowing NOT NULL
GROUP BY library_name
ORDER BY COUNT(holding.date_of_borrowing) DESC
LIMIT 1;"""
        results = cursor.execute(query).fetchall()
        for row in results:
            print(f"Library: {row[0]}")
            print(f"Number of borrowings: {row[1]}\n")
    
    def findPunishment(self):
        cursor = self.con.cursor()
        query=f"""SELECT 
        """
    
            
    def findShares(self, library_name, start_date, end_date):
        cursor = self.con.cursor()
        query = f"""SELECT title FROM book
WHERE ISBN IN
(SELECT holding.book_id
FROM holding
INNER JOIN share
ON share.holding_id = holding.holding_id
WHERE share.library_id_sharing = (SELECT library_id
FROM library
WHERE library_name = 'Βιβλιοθήκη και Κέντρο Πληροφορίας Πανεπιστήμιο Πατρών')
AND share.date_sent BETWEEN '{start_date}' AND '{end_date}')
ORDER BY title;"""
        results = cursor.execute(query).fetchall()
        print("Shared books:")
        for row in results:
            print(f"Title: {row[0]}")
        
    def specialQuery(self,query):
        cursor = self.con.cursor()
        results=cursor.execute(query).fetchall()
        
        for row in results:
            for element in row:
                print(element)
        print("\n")


if __name__ == "__main__":
    queriesObj = adminMenu("database_generation/library.db")
