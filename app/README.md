# The App to Query, Retrieve, and Update Database

This folder contains the source code of the (minimal) application that allows user interaction with the database.



Make sure you run the SFILS .sql script before running in python (We need a database before we can connect to it)


---------------------------------------------------------------------------------------------------------------------------------
If it has issues with the funciton, you can use this placed in the .py (Same as DOC readme file)

mydb = mysql.connector.connect( host="{hostservername}", user="{username}", password="{user password}", #Enter whatever your password is here database = "SFILS" #Locks us to this Database )
