# Sanfrancisco Integrated Libary System


CREATE database SFILS; 
use SFILS;

#General table, this holds all values before normalization process
#NOTE: doesn't contain any of the structure, this contains all our data from the SFILS excel file
CREATE TABLE SFILSMASTER (
    PatronTypeCode int, # Patron Type determines a patron’s borrowing limits
    PatronTypeDefinition VARCHAR(25), #Patron Type Definition
    CheckoutTotal INT, #items the patron borrowed since they registered for a library card
    RenewalTotal INT, #renewals the patron had on their borrowed items since they registered 
    AgeRange VARCHAR(100),
    HomeLibraryCode VARCHAR(10), #preferred location for patron usage of library services such as pickup for holds
    HomeLibraryDefinition VARCHAR(100),
    CirculationActiveMonth VARCHAR(25) NULL, #last date (month) of Patron activity on account 
    CirculationActiveYear VARCHAR(25) NUll,  #Date Year of patron activity on account
    NotificationMediumCode VARCHAR(5), #This could be renamed to NotifcationPreference but in excel its labeled notification_medium_code
    NotificationCodeDefinition VARCHAR(100),
    ProvidedEmailAddress VARCHAR(10), #Boolean, if they provided email adress True or False, we will change this to 1 and 0
    WithinSFCounty VARCHAR(10), # If Physical adress is located within SF City/County will convert to boolean 1's 0's  as well
    YearRegistered INT #Year when a patron registers for a library card
);




#https://nanonets.com/blog/import-excel-into-mysql/#load-data-infile
#https://stackoverflow.com/questions/1618355/load-data-local-how-do-i-skip-the-first-line
#I was unable to use the MYSQL import so I used this. 
#Encoutnered error --secure-file-priv option and could not execute
#To bypass this we put this in out Program Data upload 
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/SFPL_DataSF_library-usage_Jan_2023 - Sheet1.csv'
INTO TABLE SFILSMASTER
FIELDS TERMINATED BY ','
ENCLOSED by '"'
LINES terminated by '\n'
IGNORE 12 LINES #when I opned the csv file in notepad++ the first 12 lines are dedicated to the first row of the tableset.
(PatronTypeCode, PatronTypeDefinition, CheckoutTotal, RenewalTotal, AgeRange, HomeLibraryCode, 
HomeLibraryDefinition, CirculationActiveMonth,CirculationActiveYear,NotificationMediumCode, NotificationCodeDefinition,
ProvidedEmailAddress, WithinSFCounty, YearRegistered); 

#I want to alter some of these columns, so rather than  ProvidedEmailAddress being True or False, it is just a boolean 
#https://stackoverflow.com/questions/14175036/change-attributes-data-type-in-database-table-when-it-is-already-filled-with-rec
ALTER TABLE SFILSMASTER 
	ADD COLUMN WithinSFBool BOOLEAN,
    ADD COLUMN ProvidedEmailBool BOOLEAN;


#https://stackoverflow.com/questions/11448068/mysql-error-code-1175-during-update-in-mysql-workbench
#Where I recieved an update error, reading around I can either use a dummy Where clause, say Where 1= 1;
#Or disable safe update, change my columns, then reenable when done.     
SET SQL_SAFE_UPDATES = 0;
 
UPDATE SFILSMASTER
SET WithinSFBool = 
		case 
        When WithinSFCounty = 'True' THEN 1
        When WithinSFCounty = 'False' THEN 0
        
END;

UPDATE SFILSMASTER
SET ProvidedEmailBool = 
	CASE
		WHEN ProvidedEmailAddress = 'True' THEN 1
        WHEN ProvidedEmailAddress = 'False' THEN 0
END;
    
SET SQL_SAFE_UPDATES = 1;
    
ALTER TABLE SFILSMASTER
	DROP COLUMN WithinSFCounty,
    DROP COLUMN ProvidedEmailAddress;
   
ALTER TABLE SFILSMASTER 
	CHANGE COLUMN WithinSFBool WithinSFCounty Boolean,
	ChANGE COLUMN ProvidedEmailBool ProvidedEmailAddress Boolean;
#Now I can attempt to create the tables that we actually care about, our normalized database.

#This was to ensure that the values looked like how I wanted them to. 
#SELECT * FROM SFILSMASTER LIMIT 100;


#Now I can attempt to create the tables that we actually care about, our normalized database.
#This will help us with duplicate values, multiple rows have the same PatronType "Juvenile, Senior, etc. We can store definition and 
#associated elements (in this case library-goer age demographics(
CREATE TABLE PATRONTYPE(
	PatronTypeCode int PRIMARY KEY,
	PatronTypeDefinition VARCHAR(25)
); 

CREATE TABLE PATRONAGE(
	PatronAgeID int auto_increment primary key,
    AgeRange VARCHAR(100)
);

#Library def is dependent on library code
CREATE TABLE LIBRARYTYPE(
	HomeLibraryCode VARCHAR(10) PRIMARY KEY,
    HomeLibraryDefinition VARCHAR(100)
);

#CodeDefinition is dependet on MediumCode Type, i.e. if MediumCode = '-' = 'none' user does not want notifcation
CREATE TABLE NOTFICATIONTYPE(
    NotificationMediumCode VARCHAR(5) Primary KEY, #There are four types 'none', 'text', 'email', 'phone' 
    NotificationCodeDefinition VARCHAR(100)	
);

#This is our primary table, each row corresponds to a Library card holder in the SF bay area
#I couldn't see any other dependencies, but this table contains far more columns than the other tree
#Circulation month/year corresponds to last activity of account, this isnt a record of what they may of done
#Same with Renewel and checkout total. The just correspond to the total # of transactions
#So this would make our table 3NF, but I might be able to make it 4NF if I create additional tables with surrogate keys BookCheckoutID or LastCheckoutID
#I find this uncessecary, this is a small database,  450k rows that only update multiple times per hour. Personally I would be interested in lookups
#If we were keeping track of checkout histories, bookID (what books the patron is checking out), what books the library holds, then I would want a more normalised table
#But for this, I think this is normalized enough
CREATE TABLE PATRON(
	PatronID Int auto_increment Primary Key, #Each row doesn't really have any unique identification Email is good but why not use a surrogatre key  
	PatronTypeCode int, #FK of PATRONTYPE
    HomeLibraryCode VARCHAR(10), #FK of LIBRARYTYPE	
    NotificationMediumCode VARCHAR (5), #FK of NOTIFCATION TYPE
    PatronAgeID int, #FK of PATRONAGE
    CheckoutTotal INT,  #ALl of these are dependent on if our patron exists
    RenewalTotal INT, 
    YearRegistered INT,
	AgeRange VARCHAR(100),
    ProvidedEmailAddress BOOLEAN, 
	WithinSFCounty BOOLEAN, 
	CirculationActiveMonth VARCHAR(25), 
	CirculationActiveYear VARCHAR(25),
	FOREIGN KEY (PatronTypeCode) REFERENCES PATRONTYPE(PatronTypeCode),
	FOREIGN KEY (HomeLibraryCode) REFERENCES LIBRARYTYPE(HomeLibraryCode),
	FOREIGN KEY (NotificationMediumCode) REFERENCES NOTFICATIONTYPE(NotificationMediumCode),
    FOREIGN KEY (PatronAgeID) REFERENCES PATRONAGE(PatronAgeID) 
);

#Inserting our Master SFILS table into our "normalized" tables
#https://www.w3schools.com/sql/sql_insert.asp
#https://stackoverflow.com/questions/576441/insert-all-values-of-a-table-into-another-table-in-sql
Insert Into PATRONTYPE(PatronTypeCode, PatronTypeDefinition)
Select Distinct PatronTypeCode, PatronTypeDefinition
From SFILSMASTER;

Insert Into PATRONAGE(AgeRange)
Select Distinct AgeRange
From SFILSMASTER;

Insert Into LIBRARYTYPE(HomeLibraryCode, HomeLibraryDefinition)
Select Distinct HomeLibraryCode, HomeLibraryDefinition
From SFILSMASTER;

Insert Into NOTFICATIONTYPE(NotificationMediumCode, NotificationCodeDefinition)
Select Distinct NotificationMediumCode, NotificationCodeDefinition
From SFILSMASTER;


#I had this extremely annoying Error Code: 1054. Unknown column 'ProvidedEmailAddress' in 'field list'
#It took an embaressingly long time to find where the error was, It was in my Alter Table statement when switching 'True/False' to 1's and 0's
#I typed the new variable name as ProvidedEmailAdress, I must of read that over 100 times when trying to bug fix 
INSERT INTO PATRON (PatronTypeCode, HomeLibraryCode, NotificationMediumCode, CheckoutTotal, RenewalTotal, YearRegistered, AgeRange, 
					ProvidedEmailAddress, WithinSFCounty, CirculationActiveMonth, CirculationActiveYear)
Select PatronTypeCode, HomeLibraryCode, NotificationMediumCode, CheckoutTotal, RenewalTotal, YearRegistered, AgeRange, 
		ProvidedEmailAddress, WithinSFCounty, CirculationActiveMonth, CirculationActiveYear
From SFILSMASTER; 

#This was a last minute addition, I decided to make a PatronAgeID to store AgeRange in an additional table, as it would make the table slightly more normalized
#I edited code from earlier, but inorder to insure that PatronAgeID was placed correctly in Patron table, we need to join the values by using AgeRange as a mutual
#Once the PatronAgeID is inserteted correctly, we can drop AgeRange from our Patron, then perform a lookup through ID   
#https://www.w3schools.com/sql/sql_join.asp
#https://stackoverflow.com/questions/35805781/joining-tables-on-foreign-key
#https://www.w3schools.com/sql/sql_ref_set.asp
#This is an inner join
#Again, since this is going over our entire table, we need to temporarily disable safe update mode 
SET SQL_SAFE_UPDATES = 0;
Update PATRON Pat
Inner JOIN PATRONAGE Age
	on Age.AgeRange = Pat.AgeRange
Set Pat.PatronAgeID = Age.PatronAgeID;
SET SQL_SAFE_UPDATES = 1;

#After a fair amount of time viewing values I concluded that PatronAgeID was joined successfully
#We can now drop AgeRange as it is redundant
#SELECT * FROM PATRON LIMIT 100;
#SELECT * FROM PATRONAGE LIMIT 100;
ALTER TABLE PATRON DROP COLUMN AgeRange;

DROP TABLE IF EXISTS SFILSMASTER;

