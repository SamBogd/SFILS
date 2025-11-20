from pymongo import MongoClient
import time


#This is imported almost directly from the How to Use Python with MongoDB website linked in the A02 pdf
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


#https://www.w3schools.com/mongodb/mongodb_mongosh_find.php

startTime = time.perf_counter()

#Fetch all patron Types
myPatronType = myCollect.find({}, {"Patron Type Definition": 1, "_id": 0})

#Age Ranges
patronAge = myCollect.find({}, {"Age Range":1,"_id": 0})

#Available Branches
libraryType = myCollect.find({}, {"Home Library Definition":1, "_id": 0})

#Preferred Notification 
notifcationType = myCollect.find({}, {"Notification Code Definition":1, "_id": 0})

#All documents in collection
myPatron = myCollect.find()
print(f"Time Elapsed To Fetch Select Documents and Document values: {(time.perf_counter() - startTime):.3f}s")

#All patrons with more than 100 checkouts
#Since all patrons have exactly one Checkout Total, we can just take the count of documents fitting criteria as our patron total
startTime = time.perf_counter()
patronCountCOHundred = myCollect.count_documents({"Total Checkout": {"$gt": 100}})
print(f"Total Amount of Patrons With More Than One Hundred Renewals: {patronCountCOHundred}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")

##https://www.w3schools.com/mongodb/mongodb_aggregations_count.php
#total # of patrons 
patronCount = 0
for doc in myPatron:
    patronCount += 1
print(f"Total Amount of Patrons: {patronCount}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")



#https://www.mongodb.com/docs/manual/reference/operator/aggregation/sum/
#total # of patron checkouts
startTime = time.perf_counter()
#I had to get help from Copilot with this and patron renewl queries the documentation on aggregation
#Was too light for me
checkoutTotalQuery = list(myCollect.aggregate([{"$group": {"_id": 0, "checkoutTotal": {"$sum": "$Total Checkout"}}}]))
#'CommandCursor' object is not subscriptable
checkoutTotal = checkoutTotalQuery[0]["checkoutTotal"]
print(f"Total Checkout: {checkoutTotal}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")


#total # of patron renewals
startTime = time.perf_counter()
renewalTotalQuery = list(myCollect.aggregate([{"$group": {"_id": 0, "renewalTotal": {"$sum": "$Total Renewal"}}}]))
renewalTotal = renewalTotalQuery[0]["renewalTotal"]
print(f"Total Renewals: {renewalTotal}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")



#Average of renewal and checkout
print(f"\nAverage amount of Checkouts per patron: {(float(checkoutTotal / patronCount)):.3f}")
print(f"Average amount of Renewals per patron: {(float(renewalTotal / patronCount)):.3f}")



#I wanted to keep this as this took me quite a while in the previous assibnemnt, much to my chagrin
#Its a one line command in MongoDB, I can def see the advantages of the two. 
# startTime = time.perf_counter()
# sqlStatement = ("""SELECT patBranch.HomeLibraryCode, libBranch.HomeLibraryDefinition
#                     FROM PATRON as patBranch
#                     INNER JOIN LIBRARYTYPE AS libBranch
#                     ON patBranch.HomeLibraryCode = libBranch.HomeLibraryCode
#                     WHERE libBranch.HomeLibraryDefinition = %s;

# """)
# chosenBranch = ('Main'),
#CMySQLCursor.execute() missing 1 required positional argument: 'operation'
#Could not process parameters: str(Main), it must be of type list, tuple or dict
#This was the most difficult query for me to write, my first attempt at fixing was paramertization 
#That fixed step 1, then it demanded str(Main), it must be of type list, tuple or dict
#I fixed this by turning chosenBranch into a tuple
# myCursor.execute(sqlStatement, chosenBranch)
# patronBranchMain = myCursor.fetchall()

#I only need to count the documents that contain "main" as their home library definiton
patronCountBranchMain = myCollect.count_documents({"Home Library Definition" : "Main"})
print (f"\nPatron whos home library is the main SFILS library: {patronCountBranchMain}  |  Time Elapsed: {(time.perf_counter() - startTime):.3f}s")


