from os.path import dirname

PROJECT_ROOT = dirname(__file__)
# connection_string = ["mssql+pyodbc://RoboBedard:python@drdev-d01.meditech.com:1433/d21matdb?driver=SQL+Server+Native+Client+10.0",
# "mssql+pyodbc://RoboBedard:python@drdev-t01.meditech.com:1433/t21matdb?driver=SQL+Server+Native+Client+10.0",
#                      "mssql+pyodbc://RoboBedard:python@drdev-m01.meditech.com:1433/restapi?driver=SQL+Server+Native+Client+11.0",
#                      "mssql+pyodbc://RoboBedard:python@drdev-n01.meditech.com:1433/t608matdb?driver=SQL+Server+Native+Client+11.0",
#                      "mssql+pyodbc://RoboBedard:python@drdev11.meditech.com:1433/C201?driver=SQL+Server+Native+Client+11.0"]
with open('{}/connections.txt'.format(PROJECT_ROOT)) as connection_string_file:
    connection_string = connection_string_file.readlines()
connection_args = {}