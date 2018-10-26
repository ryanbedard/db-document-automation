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
        old_file = '{}/'.format(settings.PROJECT_ROOT) + server_name + '.csv'
        oldversion_file = '{}/'.format(settings.PROJECT_ROOT) + 'old_' + server_name + '.csv'
        new_file = '{}/change.csv'.format(settings.PROJECT_ROOT)
        xls_file = '{}/'.format(settings.PROJECT_ROOT) + server_name + '.xls'
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
                            print(row)
                            y = (r[i][1] - Decimal(x.strip(' "')))
                            writer.writerow(row[:-3] + [row[-2]] + [r[i][1]] + [y])
                            i += 1
                            successful = True
                        elif row[0] in test:
                            writer.writerow(row[:-3] + [row[-2]] + ['0'] + ['0'])
                            successful = True
                        else:
                            n = len(row) - 3
                            writer.writerow([r[i][0]] + [''] * n + [r[i][1]] + ['0'])
                            i += 1
        pandas.read_csv(new_file).to_excel(xls_file, index=False)
        copyfile(old_file, oldversion_file)
        copyfile(new_file, old_file)
        if os.path.exists(new_file):
            os.remove(new_file)
        db_test.executor.close()


def console():
    instructions()
    past_selection = ''
    selection_number = ''
    new_settings = settings.connection_string
    while True:
        selection = ''
        while selection == '':
            selection = input('>')

        selection = selection.lower().strip()

        if past_selection == 'remove':
            past_selection = ''
            if selection == 'exit':
                past_selection = ''
                selection_number = ''
                instructions()
            elif len(new_settings) > int(selection) >= 0:
                del new_settings[int(selection)]
                with open('connections.txt', "w") as newfile:
                    newfile.writelines(new_settings)
                print('Entry removed')
            else:
                print('Invalid Entry')
        elif past_selection == 'add':
            past_selection = ''
            if selection == 'exit':
                past_selection = ''
                selection_number = ''
                instructions()
            else:
                with open('connections.txt', "w") as newfile:
                    new_settings.append('\n' + selection)
                    newfile.writelines(new_settings)
                print('Entry added')
        elif past_selection == 'edit':
            if selection == 'exit':
                past_selection = ''
                selection_number = ''
                instructions()
            elif len(new_settings) > int(selection) >= 0:
                past_selection = 'string'
                selection_number = selection
                print('Enter in the new string:')
            else:
                past_selection = 'edit'
                print('Invalid selection')
        elif past_selection == 'string':
            past_selection = ''
            if selection == 'exit':
                past_selection = ''
                selection_number = ''
                instructions()
            else:
                with open('connections.txt', "w") as newfile:
                    if selection_number == len(new_settings) - 1:
                        new_settings[int(selection_number)] = selection
                        newfile.writelines(new_settings)
                    else:
                        new_settings[int(selection_number)] = selection + '\n'
                        newfile.writelines(new_settings)
                print('Entry edited')
        else:
            if selection == 'view':
                print(''.join(new_settings))
            elif selection == 'remove':
                past_selection = selection
                print('Select an option to remove or type exit to return to the main menu:')
                t = 0
                for connection in new_settings:
                    connection = connection.rstrip('\n')
                    print(str(t) + ' ' + connection),
                    t += 1
            elif selection == 'add':
                past_selection = selection
                print('Enter a connection string or type exit to return to the main menu:')
            elif selection == 'edit':
                past_selection = selection
                print('Select an option to edit or type exit to return to the main menu:')
                t = 0
                for connection in new_settings:
                    connection = connection.rstrip('\n')
                    print(str(t) + ' ' + connection),
                    t += 1
            elif selection == 'run':
                generate_documents()
                print('''Documents have been generated
                    Copy the xls files and upload them into Confluence''')
            elif selection == 'help':
                instructions()


if __name__ == "__main__":
    console()
