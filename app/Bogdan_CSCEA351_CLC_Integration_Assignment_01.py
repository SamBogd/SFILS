
#I'm not the most familiar with Python, but the library functions and ease of development seem best for this short CLC integration  
#Of our project





import mysql.connector
 

#Prompts user to see what tables that they want
def showTables():
    mycursor.execute("SHOW TABLES")
    myTable = mycursor.fetchall()
    rows = mycursor


    mybool = 1
    while (mybool):
        print("\n\nWhat table would you like to see?")
        print("1: Patron Types")
        print("2: Patron Ages")
        print("3: Library Branch")
        print("4: Preferred Notifcation")
        print("5: View Patrons")
        print("6: Exit View Tables")
        try:
            myinput = int(input("Enter value (1-6): "))
        except:
            print("Please enter a valid integer")
            continue
        if myinput <= 6  and myinput >= 1:
                
            if (myinput == 1):
                mycursor.execute("SELECT * FROM PATRONTYPE")

            if (myinput == 2):
                mycursor.execute("SELECT * FROM PATRONAGE")
            if (myinput == 3):
                mycursor.execute("SELECT * FROM LIBRARYTYPE")
            if (myinput == 4):
                mycursor.execute("SELECT * FROM NOTFICATIONTYPE")
            if(myinput == 5):
                mycursor.execute("SELECT * FROM NOTFICATIONTYPE")
                print("NOTE: There is over 440 thousand patrons of the San Francisco Library, this is a small subset")
                print("If you would like to view a specified portion, enter the \"Make a Query subbranch\"")
            if(myinput == 6):
                mybool = 0
                print("Thank You for viewing the tables!")

            #I originally had the to print all of these statemeants
            #since the logic is practically identical I can just make sure user isn't exiting table
            #then print based of their coice, the execute is already stored in cursor
            #https://www.geeksforgeeks.org/python/how-to-print-out-all-rows-of-a-mysql-table-in-python/
            print("\n")
            if(myinput != 6):
                rows = mycursor.fetchall()
                for row in rows:
                    print(row)
            print("\n")

        else:
            print("\nPlease enter a number between 1 and 6, Thank you!")


def makeQuery():
    #Looking at the SQL Injection assignment I figured it would be a good option to let this "flaw" be allowed in this code
    #That way I can fix it for the assignment    
    #https://www.dbvis.com/thetable/parameterized-queries-in-sql-a-guide/\
    #https://jupysql.ploomber.io/en/latest/user-guide/template.html
    #What we can do here is paramertize the inputs, make sure our users isn't writing something malicious, or limit an actions that they can do
    #Say you can delete 1, 5, 10 rows, but you are limited, this can also circle around to permissions granted by user.
    #I wanted some option so that user can write SQL while in the CLC   
    print("Hello, this option is for those with some experience in SQL: I trust you to not drop my database")
    print("This is raw acess to the database.")
    
    while True:
        myinput = input(("\nWould you like to continue (y/n): "))
        if (myinput == 'y'):
            mybool = 1
        if (myinput == 'n'):
            return
        else:
            print("Please enter a valid char (y/n)")
            continue
    
    while mybool == 1:
        myinput = input("Please enter your SQL command:")
        try:
            mycursor.execute(myinput)

            #https://mimo.org/glossary/python/string-find
            if (mycursor.strip().tolower().find("select")):
                rows = mycursor.fetchall()
                for row in rows:
                    print(row)

        except:
            print("\nPlease enter a valid sql command")




#This is a more controlled version of an insertion
#Prompts user to fulfill each column of patron in order to insert element
def insertEle():

    # PatronID  #Generated automatically upon insertion (auto increment surrogate key)  
    
    

    # PatronTypeCode  #FK of PATRONTYPE
    #Most of this code was adopted from HomeLibraryCode selection
    while True:
        mycursor.execute("SELECT PatronTypeCode, PatronTypeDefinition FROM PATRONTYPE")
        rows = mycursor.fetchall()

        #Key-Value Pair 
        myPatron = {}
        for code, patType in rows:
            myPatron.setdefault(patType, code) 

        print("Available Patron Types:")
        for code in myPatron:
            print(code)

        patType = input("\nWhich Patron Type is this patron: ")
        if patType in myPatron:
            PatronTypeCode = myPatron[patType]
            break
        else:
            print("Error: Enter valid patron type")
            continue


    # HomeLibraryCode  #FK of LIBRARYTYPE
    #I had a nice idea of building a key-value pairing for the elements
    #I store branch names as key, all associated codes to that pranch is value in list
    #When user selects branch, I prompt them to select code 
    #https://www.w3schools.com/python/python_dictionaries_add.asp
    while True:
        mycursor.execute("SELECT HomeLibraryCode, HomeLibraryDefinition FROM LIBRARYTYPE")
        columns =  mycursor.fetchall()


        myLibrary = { }
        #This is reversed in the fetchall, code comes before branch, so when building our Key-Value, we need to grab 2nd value first
        for code, branch in columns:
            #Key is our branch, the value is a list of all possible codes for that branch 
            myLibrary.setdefault(branch, []).append(code)
    

        print("Available Library Branches: ")
        for branch in myLibrary:
            print(branch)
        HomeLibraryCode = input("\nWhat Branch is the Patron: ")

        if HomeLibraryCode in myLibrary:
            #https://flexiple.com/python/python-print-variable
            print(f"Available Codes for Branch: {myLibrary[HomeLibraryCode]}")
            code = input("What code would you like to use? ")
        else:
            print("Error: Enter valid library branch")
            continue
            
             

        if code in myLibrary[HomeLibraryCode]:
            print("\nBranch selected sucessfully!!")
            HomeLibraryCode = code
            break
        else:
            print("Invalid Code: Code not in library branch")
            continue




        

    # NotificationMediumCode  #FK of NOTIFCATION TYPE
    print("\nWhat type of Notification does Patron Prefer?\n")
    while True:
        print("1: Patron Prefers No Notifcation")
        print("2: Patron Prefers Printed Statement")
        print("3: Patron Prefers Phone")
        print("4: Patron Prefers Email")
        try:
            NotificationMediumCode = int(input())
        except:
            print("Please enter an integer")
        if NotificationMediumCode >= 1 and NotificationMediumCode <= 4:
            if NotificationMediumCode == 1:
                NotificationMediumCode = '-'
                break
            if NotificationMediumCode == 2:
                NotificationMediumCode = 'a'
                break

            if NotificationMediumCode == 3:
                NotificationMediumCode = 'p'
                break
            if NotificationMediumCode == 4:
                NotificationMediumCode = 'z'
                break
        else:
            print("Please enter a valid number")
            continue


    #This is probably the silliest code I've writted, due to how PatronAgeID works
    #The ID isn't stored linearly by year, rather by when encountered in DB generation
    #So we need to clean input to the correct associated ID
    #E.G. user select 3, is actually PatronAgeID = 35 - 44 years 
    print("\nHow old is our patron?")
    print("1:  0-9   Years")
    print("2:  10-19 Years")
    print("3:  20-24 Years")
    print("4:  25-34 Years")
    print("5:  35-44 Years")
    print("6:  45-54 Years")
    print("7:  55-59 Years")
    print("8:  60-64 Years")
    print("9:  65-74 Years")
    print("10: 75+   Years")
    while True:
        try:
            PatronAgeID = int(input()) #FK of PATRONAGE
            if (PatronAgeID >= 1 and PatronAgeID <= 10):
                if PatronAgeID == 1:
                    break                    
                if PatronAgeID == 2:
                    break
                if PatronAgeID == 3:
                    PatronAgeID = 7
                    break
                if PatronAgeID == 4:
                    break
                if PatronAgeID == 5:
                    PatronAgeID = 3
                    break
                if PatronAgeID == 6:
                    break
                if PatronAgeID == 7:
                    PatronAgeID = 8
                    break
                if PatronAgeID == 8:
                    PatronAgeID = 9
                    break
                if PatronAgeID == 9:
                    PatronAgeID = 5
                    break
                if PatronAgeID == 10:
                    break
            else:
                print("Please enter a number between 1 and 10")
        except:
            print("Please enter a valid integer")


    #ALl of these are dependent on if our patron exists
    #You can make a case that if a new patron is being inserted, they would have 0 renews and insertions
    #Same with date registered being default set to 2025  
    #I had some weird bugs with trying to determine checkout total  
    while True:
        try:
            CheckoutTotal = int(input("How many times has user checked a book out: "))
        except:
            print("Please enter a number")


        if (CheckoutTotal < 0):
            print("Please enter a valid number (Patron's cannot checkout negative books)")
            continue
        else:
            break

    #This could probably cleaned slightly
    while True:
        try:
            RenewalTotal = int(input("How many times has patron renewed book: "))
        except:
            print("Please enter a number")
        
        if (RenewalTotal < 0):
            print("Please enter a valid number (Patron's cannot have negative renewels)")
            continue
        else:
            break

    while True:
        try:
            YearRegistered = int(input("Year patron registered: "))
              
        except:
            print("Please enter a number")

        #We can have 125 year old patrons in this library, They say learning keeps you young!
        #that or maybe they inherit their grandpa's card?
        #This would be something that would need more rigorous bound checking if this was suppose to be a "production" DB
        #We can compare it with AgeRange in order to generate a "acceptable" range of dates that way we dont have patrons with 
        #registration older than their age but for simple CLC integration I find this acceptable   
        if ( YearRegistered >= 1900 and YearRegistered <= 2025):
            break
        else:
            print("Please enter realistic age of registration (1900-2025)")
            continue
            

    #Boolean values
    while True:
        try:
            ProvidedEmailAddress = int(input("Has patron provded email adress (1-yes, 0-no): "))
            if (ProvidedEmailAddress == 1 or ProvidedEmailAddress == 0):
                break
            else:
                print("Please enter a valid input")
        except:
            print("Enter Number 1 or 0 Thank You.")


    while True:
        try:
            WithinSFCounty = int(input("Does Patron live within SF County (1-yes, 0-no): "))
            if (WithinSFCounty == 1 or WithinSFCounty == 0):
                break
            else:
                print("Please enter a valid input")
        except:
            print("Enter Number 1 or 0 Thank You.")

    #Due to what I assume are data privacy reasons, we auto set this to NULL for the time being
    #All of these are blanks when I view the list in excelt
    CirculationActiveMonth  = ""
    CirculationActiveYear  = ""

    try:
        #These few lines truly took a long time to write
        #https://pynative.com/python-mysql-insert-data-into-database-table/

        sqlInsert = """INSERT INTO PATRON(PatronTypeCode, HomeLibraryCode, NotificationMediumCode, PatronAgeID, CheckoutTotal, RenewalTotal, YearRegistered,
                       ProvidedEmailAddress, WithinSFCounty, CirculationActiveMonth, CirculationActiveYear)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       """




        #Insert failed: MySQLInterfaceError('Python type list cannot be converted')
        #Trying to get this insertion to work took a long time.  
        patronEle = (PatronTypeCode, HomeLibraryCode, NotificationMediumCode, PatronAgeID, CheckoutTotal, RenewalTotal, YearRegistered,
                       ProvidedEmailAddress, WithinSFCounty, CirculationActiveMonth, CirculationActiveYear)

        #print(patronEle)
        #print([type(x) for x in patronEle])

        mycursor.execute(sqlInsert, patronEle)
        mydb.commit()
        print("Inserted Row Successfully! PatronID = ", mycursor.lastrowid)
    except:
        print("Error Encountered With Adding Patron")
        print("Try Again y/n")
        myinput = input()
        if(myinput == 'y'):
            insertEle()



#Leftover from testing, saves me from typing in my connection evry run through 
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="{Insert Password}", #Enter whatever your password is here
#     database = "SFILS"  #Locks us to this Database
#     )



#https://k21academy.com/datascience-blog/step-by-step-guide-to-setup-sql-with-python/
def dbConnect():
    print("Hello, first please connect to the server)")
    while True:
        print("\n")
        host= input("Host Name (e.g. localhost): ")
        user= input("Username (e.g. root): ")
        password= input("Password: ") #Enter whatever your password is here
        try:
            #This connects us to our local mysql server
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,            
                database = "SFILS"  #Locks us to this Database
            )
            if (mydb.is_connected()):
                print("Connection Succesful")
                return mydb
            
        except:
            print("Connection unsuccessful please try again")
            continue

#This certifies that we sucessfully connected
#print(mydb)

#TESTING Making sure we connected sucessfully, and were using the right database (multiple test schema on mySQL instance)
# mycursor = mydb.cursor()
# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#     print(x)

mydb = dbConnect()
print("\nHello World! Welcome to Samuel's SFILS: San Francisco Integrated Library System Database")
print("This is a pretty simplistic database, from my understanding it is 3NF, and is really just to collect and hold user information")
print("We can insert elements, either through a question and ask, or by giving all values at once. I hope you enjoy")

mycursor = mydb.cursor()
mybool = 1
while (mybool):
    print("\n\nWhat would you like to see?")
    print("1: See The Tables of the Database?")
    print("2: Make a Query? NOTE: Must understand SQL")
    print("3: Insert an additional row (A new library patron!)")
    print("4: Exit Program")
    
    try:
        myinput = int(input("Enter value (1-4): "))
    except:
        print("Please enter a valid integer")
        continue
    if myinput <= 4  and myinput >= 1:
        if (myinput == 1):
            showTables()
        if (myinput == 2):
            makeQuery()
        if (myinput == 3):
            insertEle()
        if (myinput == 4):
            print("Have a wonderful day!")
            mybool = 0
    else:
        print("Please enter a number between 1 and 4, Thank you!")

#Make sure we close our connection
mycursor.close()
mydb.close()

