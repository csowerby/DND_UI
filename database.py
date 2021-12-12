
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
