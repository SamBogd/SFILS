# Findings

This folder contains our findings from this database project.

The findings include details about the library patrons. For example, how many from the age range 0 to 9 years used the library, how many of them were repeat patrons (can be found from total checkouts), how many renewed (can be found from total renewals).

# Performance Metrics

This folder also contains the performance values.

Did we store the data in our database appropriately?

This is meant to be a more manageable database with multiple tables. We are not simply dumping the whole Excel sheet into one giant MySQL table.

-------------------------------------------------------------------------------------------------------------------------------------------------------------
If it has issues with the funciton, you can use this placed in the .py (Same as thhe App file)

mydb = mysql.connector.connect( host="{hostservername}", user="{username}", password="{user password}", #Enter whatever your password is here database = "SFILS" #Locks us to this Database )



-------------------------------------------------------------------------------------------------------------------------------------------------------------
My findings were very basic, as I wasn’t exactly sure what to look for here. I was interested in the average checkouts versus renewals. It seems checking out is far more popular than renewals, San Francisco readers must be fast I guess. What I thought was interesting was that it was faster to fetch the entire table, than the same table where it only returns Patrons that have more than 100 renewals on their account. Though this makes sense than you think of it, there is some sort of conditional for each row, so there are more steps the iterate through the table.   

The Tables should bestored in 3NF, Where Patron Type, Patron Library, Preffered Notification Type, and Patron Age are put on seperate tables. All other values I deemed to dependent on Patron (Not dependent via transitive relationships to our other tables) to seperate into a new table (If there was more to this dataset maybe it would be possible, say we have to keep track of transaction history or book stock, book type, book return rate, etc. Some more values and I think this could be a really interesting dataset to work with.      

I think in terms of findings I would be more interested if this SFILS table set provided more information, renewal history, checkout history, book stock, condition of book etc. I guess what I am trying to say is I'm more interested in the books, and how patrons would interact with them, than the patrons themselves. So I’m sorry if I don’t have as many findings as you were hoping for, I truly wasn’t sure what you were looking for. 

Maybe that could be a good bag of tasks, given your assignment 01 integration, please find x information. Then our task can be to write the appropriate sql statement for said information. I truly drew a blank when trying to come with things to look for. 

