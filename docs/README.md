# Project Documentation

Here, we maintain the documentation of the project.

This includes how to build and run the software, along with any screenshots that can be of help.


----------------------------------------------------------------------------------------------------------------------------
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

