from memberMenuSQLite import *
from datetime import datetime

class MemberMenu():
    def __init__(self, database):
        self.dbmenu = MemberMenuSQLite(database)
        
        afm = input("Your AFM: ")
        
        self.dbmenu.showMemberInfo(afm)

        while (True):
            self.option = self.menuOptions()
            if (self.option == "1"):
                self.dbmenu.showMemberInfo(afm)
            elif (self.option == "2"):
                self.dbmenu.viewMemberships()
            elif (self.option == "3"):
                title = input("Δώσε τίτλο: ")
                self.dbmenu.checkBookAvailability(title)
            elif (self.option == "4"):
                kw = input("Δώσε τίτλο ή λέξη κλειδί: ")
                self.dbmenu.searchBookByTitle(kw)
            elif (self.option == "5"):
                author_name = input("Δώσε όνομα συγγραφέα: ")
                self.dbmenu.searchBookByAuthor(author_name)
            elif (self.option == "6"):
                title = input("Ποιο βιβλίο θες να δανειστείς? (Δώσε ολόκληρο τον τίτλο): ")
                if(self.dbmenu.checkBookAvailabilityMyLibrary(title, afm) == False):
                    choice1 = input("Θες να το παραγγείλεις από άλλη βιβλιοθήκη? (Yes/no) ")
                    if(choice1 == "yes" or choice1 == "Yes"):
                        numberOfLibraries=self.dbmenu.checkBookAvailability(title) 
                        if(numberOfLibraries[0] == False):
                            continue
                        else:
                            library_id_sending = input("Διάλεξε μια από τις παραπάνω βιβλιοθήκες: (1, 2, κλπ) ")
                            library_id_receiving = self.dbmenu.myLibraryID(afm)
                        
                            [book_id, holding_id] = self.dbmenu.returnBookAndHoldingIDWithGivenLibID(title, afm, library_id_sending)
                            choice = input(f"Δανεισμός του βιβλίου '{title}' με ISBN: {book_id} και holding ID: {holding_id}? (Yes/no) ")
                            if(choice == "yes" or choice == "Yes"):
                                self.dbmenu.newShareBorrow(afm, holding_id, book_id, numberOfLibraries[1], library_id_sending, library_id_receiving)
                                print("Ο δανεισμός πραγματοποιήθηκε.")
                    else:
                        continue
                else:
                    [book_id, holding_id] = self.dbmenu.returnBookAndHoldingID(title, afm)
                    choice = input(f"Δανεισμός του βιβλίου '{title}' με ISBN: {book_id} και holding ID: {holding_id}? (Yes/no) ")
                    if(choice == "yes" or choice == "Yes"):
                        self.dbmenu.newBorrow(afm, holding_id, book_id)
                        print("Ο δανεισμός πραγματοποιήθηκε.")
            else:
                break

    def menuOptions(self):
        print("Option 1: Πληροφορίες χρήστη.")
        print("Option 2: Πληροφορίες συνδρομής.")
        print("Option 3: Δες αν το βιβλίο της επιλογής σου είναι διαθέσιμο.")
        print("Option 4: Αναζήτηση βιβλίων με τίτλο ή λέξη κλειδί.")
        print("Option 5: Αναζήτηση βιβλίων με βάση τον συγγραφέα.")
        print("Option 6: Πραγματοποίηση δανεισμού.")
        option = input("Διάλεξε 1-6 ή γράψε exit για να βγεις: ")
        print("\n")
        return option
