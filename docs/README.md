# Project Documentation

Here, we maintain the documentation of the project.

This includes how to build and run the software, along with any screenshots that can be of help.

**#NOTE: Installation steps are included in appropiate files.**


----------------------------------------------------------------------------------------------------------------------------
**#SQL Installation Steps**

https://downloads.mysql.com/docs/mysql-for-excel-en.a4.pdf

Place: SFPL_DataSF_library-usage_Jan_2023 - Sheet1 
Into FilePath: C:\ProgramData\MySQL\MySQL Server 8.0\Uploads
Note: This may be on a different partition for you (D:drive, E:drive, etc. We place it here in order to avoid having to turn off certain sql safety systems) , 
Note: Since I had to zip the file it may be labeled SFPL_DataSF_library-usage_Jan_2023 - Sheet1 - Copy

IN .SQL FILE  
Make sure you set disk partition on the right disk partition

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/SFPL_DataSF_library-usage_Jan_2023 - Sheet1.csv'

^Make sure this follows your filepath (where you placed the .csv file)
In the loading statement we have the line:

IGNORE 12 LINES 
Typically this should be ignore 1 line, where the excel stores variable column names, but when I imported the csv and examined it in notepad++ the first 12 lines were dedicated to column names. This maybe different for you, so if there is an issue loading the csv with improper data type, opened the csv with notepad, notepad++ and check what line you should be looking at 

The rest of the SQL should work as intended. Just make sure that default schema is set to SFILS in mySql.     


----------------------------------------------------------------------------------------------------------------------------
**#Python Installation Steps**


I integrated this .py CLC with Visual Studio. Just make sure that you have mysql-connector-python 9.5.0 installed on the machine you are running code with. 

You can manually install from: https://pypi.org/project/mysql-connector-python/

Or use pip install, you can copy and place this in a Command Prompt

$ pip install mysql-connector-python


If pip is not installed on local machine, then you probably don’t have python installed on the machine. In that case download the current version of python here https://www.python.org/downloads/
After successful installation you should be able to use command prompt line.  

If there is an issue connecting to the database, Simply comment out def dbConnect() and utilize this command

mydb = mysql.connector.connect(
    host="{hostservername}",
    user="{username}",
    password="{user password}", #Enter whatever your password is here
    database = "SFILS"  #Locks us to this Database
    )
 
Just write in your server name, username, and password where there are brackets {}. I didn’t have any issues connecting (since it is through a local machine, so I hope for both our sakes that you don’t have any connection issues either.  


----------------------------------------------------------------------------------------------------------------------------
