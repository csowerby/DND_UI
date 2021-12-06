


"""
This is a tool meant for easy dungeons and dragons spell lookup and to practice SQL skills. This python program
using a Postgres database to store the list of all spells. I used PySimpleGUI to make a nice simple GUI to view
spells easily ingame. Since my friends and I only have the Players Handbook (5e), it is annoying to look up spells
on the internet as there are many spells that are in other expansions, so this program only contains info from that book.

Ideas for this program

Combat simulator:
Keeps track of the move order, status of your character(prone/upright/concentration/health/etc)
and what actions you can do in a given turn, move, disengage, help, all your available
spells (greyed out if you don't have prepared or spell slots or something)

Level Up/Learn New Spells Simulator Simulator:
Hard Coded rules about what spells you can get if you level up. Includes a menu of all possible spells you want
can select a list of favorite to consider and they will show up with their descriptions so you can narrow down the list

There should always be a button called "Spell Lookup" and you can put your criteria for a bunch of spells and it will bring them up. The level up/learn new spells
simulator will use the code for this feature to look up the correct spells


potentially this tool will have different profiles available also using a different table in the dnd database so fred and nigel and everyone can use the tool to level up their spells.
These profiles might be able to store info about


DATABASE LAYOUT

spell_name  | level   | casting_time | range        | components   | duration     | classes       | ritual  | concentration | school       | description
------------+---------+--------------+--------------+--------------+--------------+---------------+---------+---------------+--------------+---------------
varchar(50) | integer | varchar(255) | varchar(255) | varchar(255) | varchar(255) | varchar(50)[] | boolean | boolean       | varchar(255) | varchar(2047)

To insert varchar, have it inside single quotes, to insert varchar[] either ARRAY['wizard', 'cleric', 'etc'] or '{"Wizard", "Cleric", "etc"}'

[spell_name, level, casting_time, range, components, duration, classes, ritual, concentration, school, description]

"""

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

class GUI:
    def __init__(self, database):
        self.database = database

        # Search Screen Layout
        self.input_frame= [
                    [sg.Text("Spell Name", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Spell Level", size=(12, 1)), sg.Combo(['Cantrip', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 9', 'Any'], default_value='Cantrip', size=(24, 1))],
                    [sg.Text("Casting Time", size=(12, 1)), sg.Combo(['1 Action', '1 Bonus Action', '1 Reaction', 'Other', 'Any'], default_value='Any', size=(24, 1))],
                    [sg.Text("Range (ft)", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Duration", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Class", size=(12, 1)), sg.Combo(['Wizard', 'Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Any' ], default_value='Any', size=(24, 1))],
                    [sg.Text("Ritual?", size=(12, 1)), sg.Checkbox('Yes', default=False)],
                    [sg.ReadButton('Add'), sg.ReadButton('Replace'), sg.Button('Quit')]]

        self.spell_name_col = [[sg.Text("Spell Name")]]

        self.lvl_col = [[sg.Text("Lvl")]]

        self.time_col = [[sg.Text("Cast Time")]]

        self.range_col = [[sg.Text("R (ft)")]]

        self.components_col = [[sg.Text("Components ($)")]]

        self.duration_col = [[sg.Text("Duration")]]

        self.ritual_col = [[sg.Text("Ritual?")]]

        # RESULTS FRAME
        self.results_frame = [[   sg.Column(self.spell_name_col),
                            sg.Column(self.lvl_col),
                            sg.Column(self.time_col),
                            sg.Column(self.range_col),
                            sg.Column(self.components_col),
                            sg.Column(self.duration_col),
                            sg.Column(self.ritual_col)
                        ]]





        # FINAL LAYOUT
        self.layout = [  [sg.Frame("Spell Criteria", self.input_frame, vertical_alignment='top'), sg.VerticalSeparator(pad=None), sg.Frame("Results", self.results_frame, vertical_alignment='top')],
                    ]
        # create the window

        window = sg.Window(title='Spell Lookup', layout=self.layout, size = (1000, 800))

        # read the window
        while True:
            button, values = window.Read()
            if button is None or button == 'Quit':
                break
            if button == 'Add' or button == 'Replace':
                self.search(values)
                #Probably need a window.update of some kind here

    def search(self, values):
        print("searching!")
        # SQL Search here
        rows = []
        self.display_results(rows)


    def display_results(self, rows):
        pass




if __name__ == "__main__":
    print("\nRunning Main...\n")
    database = Postgres()
    gui = GUI(database)


    database.cursor.execute("SELECT * from spells WHERE spell_name = \'Acid Splash\';")
    rows = database.cursor.fetchall()
