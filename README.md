# database-space
This is an automation project I undertook to automate a task I do every month.

The task:
1) For all of our servers, run a SQL script (that I created) to grab the size of the databases.
2) Edit an existing spreadsheet for the specified server and add a column for the current date. Remove the entry from two months ago.
3) Paste in the the new sizes and note the change.
4) Save the document and upload it to Confluence.

The program:
Runs for every server provided in a file that's not posted here on GitHub

- Setup -
1) Connect to SQL and run the SQL script to get the database space.
2) Based upon the number of times looped through, set the File name for both the old_file and the new temporary file. The XLS version is also set.
3) Open the old_file as read only and create a new file with the new_file name.

- Check for deletions/renames -
1) Read the old_file csv and reformat everything into a list (excluding the header row).
2) Create a new list to hold the results from the SQL query.
3) Compare the two lists for databases that exist in the old list that no longer exist in the new one.
4) Store those databases in their own 'test' list.
NOTE: Renames are being treated as deletes due to the face that a similar named database does not mean the database was renamed.
Most of our databases have very similar names so it was decided to just treate renames as a delete followed by a creation of a new database.

- The main loop -
