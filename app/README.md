# The App to Query, Retrieve, and Update Database

This folder contains the source code of the (minimal) application that allows user interaction with the database.


https://downloads.mysql.com/docs/mysql-for-excel-en.a4.pdf

Place: SFPL_DataSF_library-usage_Jan_2023 - Sheet1 
Into FilePath: C:\ProgramData\MySQL\MySQL Server 8.0\Uploads

Note: This may be on a different partition for you (D:drive, E:drive, etc. We place it here in order to avoid having to turn off certain sql safety systems) , 

Note: Since I had to zip the file it may be labeled SFPL_DataSF_library-usage_Jan_2023 - Sheet1 - Copy


—-----------------------------------------------------------------------------------------------------------------------------
IN .SQL FILE  
Make sure you set disk partition on the right disk partition

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/SFPL_DataSF_library-usage_Jan_2023 - Sheet1.csv'

^Make sure this follows your filepath (where you placed the .csv file)
In the loading statement we have the line:

IGNORE 12 LINES 

Typically this should be ignore 1 line, where the excel stores variable column names, but when I imported the csv and examined it in notepad++ the first 12 lines were dedicated to column names. This maybe different for you, so if there is an issue loading the csv with improper data type, opened the csv with notepad, notepad++ and check what line you should be looking at 

The rest of the SQL should work as intended. Just make sure that default schema is set to SFILS. .    
