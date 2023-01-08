from memberMenuSQLite import *
import login_UI
from memberMenuSignIn import *

def main():
    while(True):
        print("1) Log in")
        print("2) Sign in")
        c = input("Choose: 1 or 2: ")
        if(c == "1"):
            login_UI.main()
        elif(c=="2"):
            signinmenu = MemberMenuSignIn("database_generation/library.db")
        else:
            return   

if __name__=='__main__':
    main()
