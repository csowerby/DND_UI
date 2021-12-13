
import psycopg2
import PySimpleGUI as sg



class Postgres:
    def __init__(self):
        """ Set up a connection and cursor for the postgres database "dnd" to query while the program is running. """

        self.connection = psycopg2.connect(
            host="localhost",
            database="dnd",
            user="postgres",
            password="")
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        """ Executes a query to the database, returns a list of rows that should be iterated through. """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def generate_query(self, table, conditions=None, result_columns = None):
        """
        Function to return a string of SQL code that can be executed on the postgres database with the execute_query function.
        This function is essentially a wrapper for that function so you can pass the table, conditions, and columns you want returned as parameters.

        Also, for the class column of the spells table, it will return rows that INCLUDE the specified param

        table: str
        conditions: dict
        result_columns: list? I guess (this functionality is not likely to be implemted yet since I'm almost always querying for all columns)

        """

        results = result_columns # Skeleton for formatting result string
        if results == None:
            results = '*'

        condition_list = "" # Skeleton for formatting conditions
        if conditions == None:
            condition_list = '*'
        else:
            for key, val in conditions.items():
                if key=='classes':
                    condition_list += f"classes @> ARRAY[\'{val}\']::varchar[] AND "
                else:
                    condition_list += f"{key}=\'{val}\' AND "

            condition_list = condition_list[:-5] # Chop off last " AND "

        query_string = f"SELECT {results} from {table} WHERE {condition_list};"

        return query_string

    def query_spells(self, dict):
        """ Does a query of spells on the db according to the params in this function. Returns rows

            dict -> dictionary with spell_name, level, range, duration, classes, ritual, concentration, school
        """
        # Initial String:
        query_string = f"SELECT * FROM spells "

        if len(dict) != 0:
            query_string += "WHERE "

        for key, value in dict.items():
            if key == 'classes':
                continue
            query_string += f"{key}=\'{value}\' AND "

        if 'classes' in dict.keys():
            query_string += f"classes @> ARRAY[\'{dict['classes']}\']::varchar[]"


        if query_string[-4:] == "AND ":
            query_string = query_string[:-4]
        query_string += ";"

        print(query_string)

        rows = self.execute_query(query_string)
        return rows



#------------------------------------------------------------------------------
