import random
import pandas as pd

def createFullName():
    firstNameMen=["Georgios", "Mihail", "Nikolaos", "Emmanouil", "Foivos", "Andreas", 
                  "Panagiotis", "Alexandros", "Moris", "Petros", "Konstantinos"]
    lastNameMen=["Paraskevas", "Stefanioros","Nikolopoulos","Papadopoulos","Sotiropoulos",
              "Limnidis", "Konstantellos", "Parthenios", "Mourtzopoylos", "Hahalis"]
    
    firstNameWomen=["Theodora", "Georgia", "Maria", "Emmanouela", "Foivi", "Andrianna",
                   "Panagiota", "Alexandra", "Konstantina", "Eugenia", "Sonia"]
    lastNameWomen=["Paraskeva", "Stefaniorou", "Nikolopoulou", "Hahali", "Papadopoyloy",
                   "Spiroulia", "Mpourika", "Tarabira", "Laggouretou", "Papatsori"]
    gender=["M","F"]


    nameGenderEmailList=[]
    while(len(nameGenderEmailList)<59):
        randomGender=random.choice(gender)
        
        if randomGender=="M":
            randomFirstName=random.choice(firstNameMen)
            randomLastName=random.choice(lastNameMen)
            
            nameGenderEmailList.append([randomFirstName, randomLastName, randomGender, 
                                            str.lower(randomFirstName)+str.lower(randomLastName)+"@gmail.com"])
        else:
            randomFirstName=random.choice(firstNameWomen)
            randomLastName=random.choice(lastNameWomen)
        
            nameGenderEmailList.append([randomFirstName, randomLastName, randomGender, 
                                        str.lower(randomFirstName)+str.lower(randomLastName)+"@gmail.com"])
                
    return nameGenderEmailList
            
def createAFM():
    afmList=[]
    while(len(afmList)<59):
        randomSixDigitNumber=random.randint(100000,999999)
        randomAFM="AM"+str(randomSixDigitNumber)
        
        if randomAFM not in afmList:
            afmList.append(randomAFM)
            
    return afmList

def createPhoneNumber():
    phoneNumberList=[]
    while(len(phoneNumberList)<59):
        randomEightDigitNumber=random.randint(10000000,99999999)
        randomPhoneNumber="69"+str(randomEightDigitNumber)
        
        if randomPhoneNumber not in phoneNumberList:
            phoneNumberList.append(randomPhoneNumber)
            
    return phoneNumberList


def createBirthDate():
    birthDateList=[]
    
    for i in range(59):
        year= random.randint(1960, 2005)
        month=random.randint(1,12)
        if month in [1,3,5,7,8,10,12]:
            day=random.randint(1,31)
        elif month in [4,6,9,11]:
            day=random.randint(1,30)
        elif year%4==0:
            day=random.randint(1,29)
        else:
            day=random.randint(1,28)
            
        if day<10:
            day="0"+str(day)
        if month<10:
            month="0"+str(month)
        
        birthDateList.append(str(year)+"-"+str(month)+"-"+str(day))
    
    return birthDateList


def createTypeOfMembership(born_in):
    typeOfMembershipList=[]
    
    for i in range(59):
        if int(born_in[i][0:4])>1999:
            typeOfMembershipList.append(0) #Undergraduate Student
        elif 1996<=int(born_in[i][0:4])<=1999:
            typeOfMembershipList.append(1) #Postgraduate Student
        elif 1980<=int(born_in[i][0:4])<1996:
            typeOfMembershipList.append(3) #Outside User
        else:
            typeOfMembershipList.append(2) #Professor
    
    return typeOfMembershipList
        
    
def createPenalty():
    penaltyList=[]
    
    penaltyID=[0,1,2,3]
    probability=[0.7,0.15,0.1,0.05]
    
    for i in range(59):
        penaltyList.append(random.choices(penaltyID,probability)[0])
    
    return penaltyList
   
    

def generate():
    afm=createAFM()
    nameGenderEmail=createFullName()
    phoneNumber=createPhoneNumber()
    birthDate=createBirthDate()
    membership=createTypeOfMembership(birthDate)
    penalty=createPenalty()
    
    memberList=[]
    
    
    for i in range(59):
        tempList=[]
        tempList.append(afm[i])
        for j in range(4):
            tempList.append(nameGenderEmail[i][j])
        tempList.append(phoneNumber[i])
        tempList.append(birthDate[i])
        tempList.append(membership[i])
        tempList.append(penalty[i])
        tempList.append(i) #no need for random location_id
        
        memberList.append(tempList)
    
    columns=["AFM","first_name","last_name","gender", "gmail","phone_number","birthdate",
             "type_of_membership","penalty_id","location_id"]
    df=pd.DataFrame(memberList, columns=columns)
    writer = pd.ExcelWriter('excel_files/member.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()


    

