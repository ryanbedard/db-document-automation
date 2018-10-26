import csv
from datetime import date
import settings
from decimal import Decimal
from database.connections import Connection
from shutil import copyfile
import os
import pandas


def instructions():
    # print menu options
    print('''
Server and Database Program
========
Commands:
  help - Displays this menu again
  view - Displays connection strings for all databases
  edit - Brings up options to edit an existing connection string
  add - Adds a new connection string
  remove - Removes a selected connection string
  run - Runs the program
''')


def generate_documents():
    for connection in settings.connection_string:
        db_test = Connection(connection, settings.connection_args)
        result = db_test.executor.execute(("SELECT database_name = DB_NAME(database_id) , "
                                           "total_size_gb = CAST(SUM(size) * 8. / 1024/1024 AS DECIMAL(8,3)) "
                                           "FROM sys.master_files WITH(NOWAIT) "
                                           "where DB_NAME(database_id) "
                                           "NOT IN ('AdventureWorks2012_Data','master','tempdb','model','msdb','ReportServer','ReportServerTempDB','Northwind') "
                                           "AND DB_NAME(database_id) NOT LIKE 'z%' GROUP BY database_id ORDER BY database_name"))
        r = list(result)
        server_name = connection[connection.find('@') + 1:connection.find('.')].upper()
        old_file = server_name + '.csv'
        new_file = 'change.csv'
        xls_file = server_name + '.xls'
        with open(old_file, 'r', newline='') as csvinput:
            with open(new_file, 'w', newline='') as csvoutput:
                writer = csv.writer(csvoutput)
                i = 0
                originals = []
                reader = csv.reader(csvinput, delimiter=',')
                old_list = list(reader)
                for row in old_list:
                    if row[0] == "Database":
                        pass
                    else:
                        originals.append(row[0])
                currents = []
                for item in r:
                    currents.append(item[0])
                test = list(set(originals).difference(currents))
                for row in old_list:
                    successful = False
                    while not successful:
                        if row[0] == "Database":
                            writer.writerow(row[:-3] + [row[-2]] + [date.today().strftime('%m/%d/%Y')] + ['Change'])
                            successful = True
                        elif row[0] == r[i][0]:
                            x = row[-2]
                            y = (r[i][1] - Decimal(x.strip(' "')))
                            writer.writerow(row[:-3] + [row[-2]] + [r[i][1]] + [y])
                            i += 1
                            successful = True
                        elif row[0] in test:
                            writer.writerow(row[:-3] + [row[-2]] + ['Deleted'] + ['0'])
                            successful = True
                        else:
                            n = len(row) - 3
                            writer.writerow([r[i][0]] + [''] * n + [r[i][1]] + ['0'])
                            i += 1
        pandas.read_csv(new_file).to_excel(xls_file, index=False)
        copyfile(old_file, 'old_' + old_file)
        copyfile(new_file, old_file)
        if os.path.exists(new_file):
            os.remove(new_file)
    db_test.executor.close()


if __name__ == "__main__":
    instructions()
    pastSelection = ''
    selectionNumber = ''
    newSettings = settings.connection_string
    while True:
        selection = ''
        while selection == '':
            selection = input('>')

        selection = selection.lower().strip()

        if pastSelection == 'remove':
            pastSelection = ''
            if selection == 'exit':
                break
            elif len(newSettings) > int(selection) >= 0:
                del newSettings[int(selection)]
                with open('connections.txt', "w") as newfile:
                    newfile.writelines(newSettings)
                print('Entry removed')
            else:
                print('Invalid Entry')
                break
        elif pastSelection == 'add':
            pastSelection = ''
            if selection == 'exit':
                break
            else:
                with open('connections.txt', "w") as newfile:
                    newSettings.append('\n' + selection)
                    newfile.writelines(newSettings)
                print('Entry added')
        elif pastSelection == 'edit':
            pastSelection = ''
            if selection == 'exit':
                break
            elif len(newSettings) > int(selection) >= 0:
                pastSelection = 'string'
                selectionNumber = selection
                print('Enter in the new string:')
            else:
                pastSelection = 'edit'
                print('Invalid selection')
        elif pastSelection == 'string':
            pastSelection = ''
            if selection == 'exit':
                break
            else:
                with open('connections.txt', "w") as newfile:
                    if selectionNumber == len(newSettings) - 1:
                        newSettings[int(selectionNumber)] = selection
                        newfile.writelines(newSettings)
                    else:
                        newSettings[int(selectionNumber)] = selection + '\n'
                        newfile.writelines(newSettings)
                print('Entry edited')
        else:
            if selection == 'view':
                print(''.join(newSettings))
            elif selection == 'remove':
                pastSelection = selection
                print('Select an option to remove or type exit to return to the main menu:')
                t = 0
                for connection in newSettings:
                    connection = connection.rstrip('\n')
                    print(str(t) + ' ' + connection),
                    t += 1
            elif selection == 'add':
                pastSelection = selection
                print('Enter a connection string or type exit to return to the main menu:')
            elif selection == 'edit':
                pastSelection = selection
                print('Select an option to edit or type exit to return to the main menu:')
                t = 0
                for connection in newSettings:
                    connection = connection.rstrip('\n')
                    print(str(t) + ' ' + connection),
                    t += 1
            elif selection == 'run':
                generate_documents()
                print('''Documents have been generated
                Copy the xls files and upload them into Confluence''')
            elif selection == 'help':
                instructions()
