
import mysql.connector
import time

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

# mydb = mysql.connector.connect(
#     host="",
#     user="",
#     password="", #Enter whatever your password is here
#     database = "SFILS"  #Locks us to this Database
#     )

mydb = dbConnect()
myCursor = mydb.cursor()

#Wasn't sure how to time events in python
#https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
#https://www.geeksforgeeks.org/python/precision-handling-python/
#startTime = time.time()

print("\nHello World! Welcome to Samuel's SFILS: San Francisco Integrated Library System Testing Chambers")


#Fetches tables
startTime = time.perf_counter()
myCursor.execute("SELECT * FROM PATRONTYPE")
patronType = myCursor.fetchall()
myCursor.execute("SELECT * FROM PATRONAGE")
patronAge = myCursor.fetchall()
myCursor.execute("SELECT * FROM LIBRARYTYPE")
libraryType = myCursor.fetchall()
myCursor.execute("SELECT * FROM NOTFICATIONTYPE")
notifcationType = myCursor.fetchall()
myCursor.execute("SELECT * FROM PATRON")
myPatron = myCursor.fetchall()
print(f"Time Elapsed To Iterate Through All Tables: {(time.perf_counter() - startTime):.3f}s")

#All patrons with more than 100 checkouts
startTime = time.perf_counter()
myCursor.execute("SELECT COUNT(*) as patronCountGTHundred FROM PATRON WHERE CheckoutTotal > 100")
patronCountGTHundred = myCursor.fetchone()[0]
print(f"Total Amount of Patrons With More Than One Hundred Renewals: {patronCountGTHundred}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")


#total # of patrons 
startTime = time.perf_counter()
myCursor.execute("SELECT COUNT(*) as patronCount FROM PATRON")
patronCount = myCursor.fetchone()[0] #Count sum 
print(f"Total Amount of Patrons: {patronCount}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")



#https://stackoverflow.com/questions/49371423/sum-of-results-python-sql-query
#total # of patron checkouts
startTime = time.perf_counter()
myCursor.execute("SELECT SUM(CheckoutTotal) as checkoutTotal FROM PATRON")
checkoutTotal = myCursor.fetchone()[0] #Result of sum
print(f"Total Checkout: {checkoutTotal}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")


#total # of patron renewals
startTime = time.perf_counter()
myCursor.execute("SELECT SUM(RenewalTotal) as renewalTotal FROM PATRON")
renewalTotal = myCursor.fetchone()[0] #Result of sum
print(f"Total Renewals: {renewalTotal}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")



#Average of renewal and checkout
print(f"\nAverage amount of Checkouts per patron: {(float(checkoutTotal / patronCount)):.3f}")
print(f"Average amount of Renewals per patron: {(float(renewalTotal / patronCount)):.3f}")

startTime = time.perf_counter()
sqlStatement = ("""SELECT patBranch.HomeLibraryCode, libBranch.HomeLibraryDefinition
                    FROM PATRON as patBranch
                    INNER JOIN LIBRARYTYPE AS libBranch
                    ON patBranch.HomeLibraryCode = libBranch.HomeLibraryCode
                    WHERE libBranch.HomeLibraryDefinition = %s;

""")
chosenBranch = ('Main'),

#CMySQLCursor.execute() missing 1 required positional argument: 'operation'
#Could not process parameters: str(Main), it must be of type list, tuple or dict
#This was the most difficult query for me to write, my first attempt at fixing was paramertization 
#That fixed step 1, then it demanded str(Main), it must be of type list, tuple or dict
#I fixed this by turning chosenBranch into a tuple
myCursor.execute(sqlStatement, chosenBranch)
patronBranchMain = myCursor.fetchall()
myCount = 0
for (branchCode, branchLocation) in patronBranchMain:
    myCount += 1

print (f"\nPatron whos home library is the main SFILS library: {myCount}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")



