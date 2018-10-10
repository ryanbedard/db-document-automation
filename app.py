import csv
from datetime import date
import settings
from decimal import Decimal
from database.connections import Connection
from shutil import copyfile
import os
import pandas


if __name__ == "__main__":
    t = 0
    for connection in settings.connection_string:
        db_test = Connection(connection, settings.connection_args)
        result = db_test.executor.execute(("SELECT database_name = DB_NAME(database_id) , "
                                       "total_size_gb = CAST(SUM(size) * 8. / 1024/1024 AS DECIMAL(8,3)) "
                                       "FROM sys.master_files WITH(NOWAIT) "
                                       "where DB_NAME(database_id) "
                                       "NOT IN ('AdventureWorks2012_Data','master','tempdb','model','msdb','ReportServer','ReportServerTempDB','Northwind') "
                                       "AND DB_NAME(database_id) NOT LIKE 'z%' GROUP BY database_id ORDER BY database_name"))
        r = list(result)
        if t == 0:
            old_file = 'DRDEV-D01.csv'
            new_file = 'change.csv'
            xls_file = 'DRDEV-D01.xls'
        elif t == 1:
            old_file = 'DRDEV-T01.csv'
            new_file = 'change1.csv'
            xls_file = 'DRDEV-T01.xls'
        elif t == 2:
            old_file = 'DRDEV-M01.csv'
            new_file = 'change2.csv'
            xls_file = 'DRDEV-M01.xls'
        elif t == 3:
            old_file = 'DRDEV-N01.csv'
            new_file = 'change3.csv'
            xls_file = 'DRDEV-N01.xls'
        elif t == 4:
            old_file = 'DRDEV11.csv'
            new_file = 'change4.csv'
            xls_file = 'DRDEV11.xls'
        else:
            pass
        t += 1
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
                            y = (r[i][1]-Decimal(x.strip(' "')))
                            writer.writerow(row[:-3] + [row[-2]] + [r[i][1]] + [y])
                            i += 1
                            successful = True
                        elif row[0] in test:
                            writer.writerow(row[:-3] + [row[-2]] + ['Deleted'] + ['0'])
                            successful = True
                        else:
                            n = len(row) - 3
                            writer.writerow([r[i][0]] + ['']*n + [r[i][1]] + ['0'])
                            i += 1
        pandas.read_csv(new_file).to_excel(xls_file, index=False)
        copyfile(old_file, 'old_' + old_file)
        copyfile(new_file, old_file)
        if os.path.exists(new_file):
            os.remove(new_file)
    db_test.executor.close()
