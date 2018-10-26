from os.path import dirname

PROJECT_ROOT = dirname(__file__)
with open('{}/connections.txt'.format(PROJECT_ROOT)) as connection_string_file:
    connection_string = connection_string_file.readlines()
connection_args = {}