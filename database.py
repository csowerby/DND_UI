
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

    def query_spells(self, spell_name=None, level=None, range=None, duration=None, classes=None, ritual=None, concentration=None, school=None):
        """ Does a query of spells on the db according to the params in this function. Returns rows """

        # Spell Name
        if spell_name is None:
            spell_name = "*"

        # Spell Level
        if level is None:
            level = "*"
        else:
            level = str(level)
        # Spell Range
        if range is None:
            range = "*"


        self.execute_query(f"""SELECT * FROM spells WHERE
        spell_name={spell_name} AND
        level={level} AND
        range={range} AND
        duration={duration} AND
        ritual={ritual} AND
        concentration={concentration}
        school={school} AND
        classes @> ARRAY[\'{classes}\']::varchar[];
        """)

#------------------------------------------------------------------------------
