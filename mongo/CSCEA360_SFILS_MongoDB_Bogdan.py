from pymongo import MongoClient



#Prompts user to see what tables that they want
def showTables():
    mybool = 1
    while (mybool):
        print("\n\nWhat table would you like to see?")
        print("1: Patron Types")
        print("2: Patron Ages")
        print("3: Library Branch")
        print("4: Preferred Notifcation")
        print("5: View Patrons (Note one sample entry) ")
        print("6: Exit View Tables")
        print("\n")
        try:
            myinput = int(input("Enter value (1-6): "))
        except:
            print("Please enter a valid integer")
            continue
        if myinput <= 6  and myinput >= 1:
                
            if (myinput == 1):
                print(patronType) 

            if (myinput == 2):
                print(patronAge)
                
            if (myinput == 3):
                print(libType)
                
            if (myinput == 4):
                print(notifType)
                
            if(myinput == 5):
                print("NOTE: There is over 440 thousand patrons of the San Francisco Library, this is a sample")
                print("If you would like to view a specified portion, enter the \"Make a Query subbranch\"")
                print(sampleEntry)
            if(myinput == 6):
                mybool = 0
                print("Thank You for viewing the tables!")

        else:
            print("\nPlease enter a number between 1 and 6, Thank you!")


def makeQuery():
    print("Hello, this option is for those with some experience in MongoDB: I trust you to not do anything malicious")
    print("This is raw acess to the SFILS collection.")
    
    while True:
        myinput = input(("\nWould you like to continue (y/n): "))
        if (myinput == 'y'):
            mybool = 1
        if (myinput == 'n'):
            mybool = 0
            break
        else:
            print("Please enter a valid char (y/n)")
            continue
    
    ##https://www.mongodb.com/resources/languages/python#querying-in-python
    #   
    while mybool == 1:
        myinput = input("Please enter your MongoDB query:")
        try:
            #try to turn it into python dict 
            #https://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval
            query = ast.literal_eval(myinput)

            if not isinstance(query,dict):
                print("Enter a valid MongoDB query")
                continue
            userQuery = myCollect.find(query)
            print("Results: \n")
            for doc in userQuery:
                print(doc)
                

            while True:
                myinput = input(("\nWould you like to continue (y/n): "))
                if (myinput == 'y'):
                    mybool = 1
                if (myinput == 'n'):
                    mybool = 0
                    break
                else:
                    print("Please enter a valid char (y/n)")
                    continue

        except Exception as error:
            print("\nPlease enter a valid MongoDB command")
            print("Error: ", error)



#This is a more controlled version of an insertion
#Prompts user to fulfill each column of patron in order to insert element
def insertEle():

    # ObjectId  #Generated automatically upon insertion
    
    

    #Same logic as SQl implementatio, creat a key-value pair of these associated elements for querying  
    #I had a nice idea of building a key-value pairing for the elements
    #I store branch names as key, all associated codes to that pranch is value in list
    #When user selects branch, I prompt them to select code 
    #https://www.w3schools.com/python/python_dictionaries_add.asp
    # PatronTypeCode 
    while True:
        #https://www.w3schools.com/mongodb/mongodb_mongosh_find.php
        #https://stackoverflow.com/questions/28034845/how-to-correctly-iterate-through-a-search-result-in-mongodb-shell

        myCursor = myCollect.find({}, {"_id": 0, "Patron Type Code": 1, "Patron Type Definition": 1})

        #Key-Value Pair 
        myPatron = {}
        for doc in myCursor:
            key = doc.get("Patron Type Definition")
            value = doc.get("Patron Type Code")
            myPatron[key] = value

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



    while True:
        #mycursor.execute("SELECT HomeLibraryCode, HomeLibraryDefinition FROM LIBRARYTYPE")
        myCursor = myCollect.find({}, {"_id": 0, "Home Library Code": 1, "Home Library Definition": 1})
        
        myLibrary = { }
        #This is reversed in the fetchall, code comes before branch, so when building our Key-Value, we need to grab 2nd value first
        for doc in myCursor:
            key = doc.get("Home Library Definition")
            value = doc.get("Home Library Code")
            #Key is our branch, the value is a list of all possible codes for that branch 
            myLibrary[key] = value
    

        print("Available Library Branches: ")
        for branch in myLibrary:
            print(branch)
        HomeLibrary = input("\nWhat Branch is the Patron: ")

        if HomeLibrary in myLibrary:
            #https://flexiple.com/python/python-print-variable
            print(f"Available Codes for Branch: {myLibrary[HomeLibrary]}")
            code = input("What code would you like to use? ")
        else:
            print("Error: Enter valid library branch")
            continue
        
        if code in myLibrary[HomeLibrary]:
            print("\nBranch selected sucessfully!!")
            HomeLibraryCode = code
            break
        else:
            print("Invalid Code: Code not in library branch")
            continue




        

    # Notification Preference Code
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
                NotificationCodeDefinition = "None"
                break
            if NotificationMediumCode == 2:
                NotificationMediumCode = 'a'
                NotificationCodeDefinition = "Print"
                break

            if NotificationMediumCode == 3:
                NotificationMediumCode = 'p'
                NotificationCodeDefinition = "Phone"
                break
            if NotificationMediumCode == 4:
                NotificationMediumCode = 'z'
                NotificationCodeDefinition = "Email"
                break
        else:
            print("Please enter a valid number")
            continue


    #Age of patron 
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
                    PatronAge = "0-9 Years"
                    break                    
                if PatronAgeID == 2:
                    PatronAge = "10-14 Years"
                    break
                if PatronAgeID == 3:
                    PatronAge = "20-24 Years"
                    break
                if PatronAgeID == 4:
                    PatronAge = "25-34 Years"
                    break
                if PatronAgeID == 5:
                    PatronAge = "35-44 Years"
                    break
                if PatronAgeID == 6:
                    PatronAge = "45-54 Years"
                    break
                if PatronAgeID == 7:
                    PatronAge = "55-59 Years"
                    break
                if PatronAgeID == 8:
                    PatronAge = "60-64 Years"
                    break
                if PatronAgeID == 9:
                    PatronAge = "65-74 Years"
                    break
                if PatronAgeID == 10:
                    PatronAge = "75+ Years"
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
                if ProvidedEmailAddress == 1:
                    ProvidedEmailAddress = True
                else:
                    ProvidedEmailAddress = False
                break
            else:
                print("Please enter a valid input")
        except:
            print("Enter Number 1 or 0 Thank You.")


    while True:
        try:
            WithinSFCounty = int(input("Does Patron live within SF County (1-yes, 0-no): "))
            if (WithinSFCounty == 1 or WithinSFCounty == 0):
                if WithinSFCounty == 1:
                    WithinSFCounty = True
                else:
                    WithinSFCounty = False
                break
            else:
                print("Please enter a valid input")
        except:
            print("Enter Number 1 or 0 Thank You.")

    #Due to what I assume are data privacy reasons, we auto set this to NULL for the time being
    #All of these are blanks when I view the list in excelt
    CirculationActiveMonth  = ""
    CirculationActiveYear  = -1
    
    try:
        #These few lines truly took a long time to write
        #https://pynative.com/python-mysql-insert-data-into-database-table/

        mongoDBPatron = {
            "Patron Type Code": PatronTypeCode,
            "Patron Type Definition": patType,
            "Total Checkout": CheckoutTotal,
            "Total Renewal": RenewalTotal,
            "Age Range": PatronAge,
            "Home Library Code": HomeLibraryCode,
            "Home Library Definition": HomeLibrary,
            "Circulation Active Month": CirculationActiveMonth,
            "Circulation Active Year": CirculationActiveYear,
            "Notification Preference Code": NotificationMediumCode,
            "Notification Code Definition": NotificationCodeDefinition,
            "Provided Email Address": ProvidedEmailAddress,
            "Within San Francisco County": WithinSFCounty,
            "Year Patron Registered": YearRegistered
                       
        }

        #https://www.w3schools.com/mongodb/mongodb_mongosh_insert.php
        insertDoc = myCollect.insert_one(mongoDBPatron)

        print("Record added successfully! ID: ", insertDoc.inserted_id)

    except Exception as err:
        print("Error Encountered With Adding Patron: ", err)
        print("Try Again y/n")
        myinput = input()
        if(myinput == 'y'):
            insertEle()



#This is imported almost directly from the How to Use Python wiht MongoDB website linked in the A02 pdf
# https://www.mongodb.com/resources/languages/python
CONNECTION_STRING = "mongodb://localhost:27017/"
client = MongoClient(CONNECTION_STRING)
#Admittedly I probably could of named my Datbase and collection something Diff 
db = client["SFILS"]
myCollect = db["SFILS"]
# Retrieve a collection named "user_1_items" from database

#Testing connection and CSV import  
#myDoc = myCollect.find_one()
#print(myDoc)

#Distinct values, no need to query the server every time
patronType = myCollect.distinct("Patron Type Definition")
patronAge = myCollect.distinct("Age Range")
libType = myCollect.distinct("Home Library Definition")
notifType = myCollect.distinct("Notification Code Definition")
sampleEntry = myCollect.find_one()


print("\nHello World! Welcome to Samuel's SFILS: San Francisco Integrated Library System Database")
print("This is a pretty simplistic database, implemented in MongoDB this time, how exciting!")
print("We can insert elements, either through a question and ask, or by giving all values at once. I hope you enjoy")


mybool = 1
while (mybool):
    print("\n\nWhat would you like to see?")
    print("1: See The Tables of the Database?")
    print("2: Make a Query? NOTE: Must understand MongoDB")
    print("3: Add a new library patron! (Insert a document)")
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
