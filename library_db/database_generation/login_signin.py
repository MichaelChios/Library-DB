import sqlite3
import hashlib
import pandas as pd


def generate():
    with sqlite3.connect("login_signin.db") as connection:
        with open("login_signin.sql", "r") as file:
            sql=""
            for row in file:
                sql+=row
            sql=sql.split(";")
        for query in sql:
            cur=connection.cursor()
            cur.execute(query)


def loadAdmins():
    
    conn=sqlite3.connect("login_signin.db")
    cur=conn.cursor()
    
    
    fparask_password="12345"
    fparask_password_hashed=hashlib.sha256(fparask_password.encode()).hexdigest()
    
    cur.execute(
        f"""INSERT INTO login_signin
        VALUES (?, ?, ?)""", ("Fparask", fparask_password_hashed, 1)
    )
    
    mstef_password="67890"
    mstef_password_hashed=hashlib.sha256(mstef_password.encode()).hexdigest()
    
    cur.execute(
        f"""INSERT INTO login_signin
        VALUES (?, ?, ?)""", ("Mstef", mstef_password_hashed, 1)
    )

    conn.commit()
    conn.close()
    
    return
    
    
def loadMembers():
    member_df=pd.read_excel("excel_files/member.xlsx")
    
    usernameList=["Fparask", "Mstef"]
    with sqlite3.connect("login_signin.db") as connection:
        cursor = connection.cursor()
        
        for _, row in member_df.iterrows():
            first_name = row["first_name"]
            last_name=row["last_name"]
            
            succeed=0
            count=0
            while(succeed!=1):
                username=first_name[count]+last_name[0:4]
                if username not in usernameList:
                    usernameList.append(username)
                    succeed=1
                count=count+1
            
            password_hashed=hashlib.sha256(username.encode()).hexdigest()
            
            cursor.execute(
                f"""INSERT INTO login_signin
                VALUES (?,?,?);""", (username,password_hashed,0)
            )

        connection.commit()
        connection.close
    
