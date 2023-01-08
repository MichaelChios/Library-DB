import libraryDBGenerator
import login_signin

import bookScrapper
import bookGeneration
import authorGeneration
import memberGeneration
import library_member_connection
import holdingGeneration
import positionGeneration
import shareGeneration



if __name__=='__main__':
    libraryDBGenerator.generate()
    login_signin.generate()
    # bookScrapper.generate()
    bookGeneration.generate()
    authorGeneration.generate()
    memberGeneration.generate()
    library_member_connection.generate()
    holdingGeneration.generate()
    positionGeneration.generate()
    shareGeneration.generate()
    libraryDBGenerator.loadData()
    login_signin.loadAdmins()
    login_signin.loadMembers()
    




    print(1)
