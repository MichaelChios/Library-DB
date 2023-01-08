from memberMenuSQLite import *
from datetime import datetime

class MemberMenuSignIn():
    def __init__(self, database):
        self.dbmenu = MemberMenuSQLite(database)
        
        self.insertUserInfo()

    def insertUserInfo(self):
        afm = input("Your AFM: ")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        username = input("Username: ")
        while(self.dbmenu.checkIfUsernameExists(username) == False):
            username = input("Username already exists: ")
        print("Give password: ")
        password = hashlib.sha256(input().encode()).hexdigest()
        self.dbmenu.signUp(username, password)
        gender = input("'M' for male or 'F' for female: ")
        email = input("Email address: ")
        phone_number = input("Phone number: ")
        birthdate = input("Birth date (YYYY-MM-DD): ")
        print("Διάλεξε membership: ")
        print("1) Φοιτητής")
        print("2) Μεταπτυχιακός")
        print("3) Μέλος ΔΕΠ")
        print("4) Εξωτερικός χρήστης")
        tom = input("Επέλεξε (1-4): ")
        print("0) Βιβλιοθήκη και Κέντρο Πληροφορίας Πανεπιστήμιο Πατρών")
        print("1) Βιβλιοθήκη και Κέντρο Πληροφορίας Πανεπιστήμιο Αγρινίου")
        print("2) Βιβλιοθήκη και Κέντρο Πληροφορίας Πανεπιστήμιο Κουκουλίου")
        print("3) Βιβλιοθήκη και Κέντρο Πληροφορίας Πανεπιστήμιο Μεσολογγίου")
        print("4) Βιβλιοθήκη και Κέντρο Πληροφορίας Πανεπιστήμιο Πύργου")
        libraryID = input("Διάλεξε σε ποια βιβλιοθήκη θες να κάνεις εγγραφή: ")
        self.dbmenu.insertLibraryMember(afm, libraryID)
        print("Τώρα θα χρειαστούμε πληροφορίες σχετικά με την τοποθεσία σου.")
        country = input("Country: ")
        city = input("City: ")
        street = input("Street: ")
        streetNum = input("Street number: ")
        pk = input("Postal code: ")
        if(self.dbmenu.checkIfLocationExists(country, city, street, streetNum, pk) == False):
            self.dbmenu.newLocation(country, city, street, streetNum, pk)
        locID = self.dbmenu.returnLocationId(country, city, street, streetNum, pk)
        self.dbmenu.newMember(afm, first_name, last_name, gender, email, phone_number, birthdate, tom, locID)


