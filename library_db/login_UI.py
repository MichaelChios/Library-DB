import sqlite3
import hashlib
import adminMenu as am
import memberMenu as mm


def main():
    conn = sqlite3.connect("database_generation/login_signin.db")
    cursor = conn.cursor()
    
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("SELECT password_hashed, member_admin FROM login_signin WHERE username=?", (username,))
    row = cursor.fetchone()
    
    
    if row is None:
        print("Invalid username or password")
    else:
        if row[0] == password_hash:
            if row[1]==1:
                queriesObj = am.adminMenu("database_generation/library.db")
                
            elif row[1]==0:
                menu = mm.MemberMenu("database_generation/library.db")
        else:
            print("Invalid username or password")
    
    # Close the connection
    conn.close()
