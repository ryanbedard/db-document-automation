# database-space
This is an automation project I undertook to automate a task I do every month. This program runs for every server provided in a file that's not posted here on GitHub

The task:
1) For all of our servers, run a SQL script (that I created) to grab the size of the databases.
2) Edit an existing spreadsheet for the specified server and add a column for the current date. Remove the entry from two months ago.
3) Paste in the the new sizes and note the change.
4) Save the document and upload it to Confluence.

The program:

- Setup
1) Connect to SQL and run the SQL script to get the database space.
2) Based upon the number of times looped through, set the File name for both the old_file and the new temporary file. The XLS version is also set.
3) Open the old_file as read only and create a new file with the new_file name.

- Check for deletions/renames
1) Read the old_file csv and reformat everything into a list (excluding the header row).
2) Create a new list to hold the results from the SQL query.
3) Compare the two lists for databases that exist in the old list that no longer exist in the new one.
4) Store those databases in their own 'test' list.
NOTE: Renames are being treated as deletes due to the face that a similar named database does not mean the database was renamed.
Most of our databases have very similar names so it was decided to just treate renames as a delete followed by a creation of a new database.

- The main loop
1) Set a successful flag. The point of this flag is to make sure we don't skip comparing any databases if there were any new databases
added since the last run of the program.
2) Check if the row[0] is equal to "Database". If it is, write the row as the old row without the column that is two months old. The
column that is two months old will always be in position -3. Then add the current date as well as a column for the 'Change'.
3) If the current row looped on is named the same as the query database in the [i] position, insert the row with the old data, followed by the new data, and a new column that displays the difference between them.
4) If the current row looped on is in the list of databases that were deleted, simply take the old information and put the "size" column
as 'Deleted'.
5) Lastly, if none of the following were true, then the row must be new, so a new database entry is set up.

- The filing and cleanup
1) Using pandas, make a copy of the new file as an XLS. This is done as Confluence doesn't accept csv.
2) Take the old_file and rename it with 'old_'  put in front of the name.
3) Rename the new_file to the old_file's original name.
4) Delete the new_file if it still exists.
