


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


UPDATE DB COMMAND

dnd=# COPY spells(spell_name, level, casting_time, range, components, duration, classes, ritual, concentration, school, description)
FROM '/Users/charliesowerby/Desktop/Projects/dnd_ui/spells.csv'
DELIMITER ','
CSV HEADER;
"""

import psycopg2
import PySimpleGUI as sg

from database import Postgres

#------------------------------------------


class GUI:
    def __init__(self, database):
        sg.theme('DarkAmber')

        self.database = database
        self.rows = []
        self.hl_rows = []
        self.values_list = ['spell_name', 'level', 'casting_time', 'range', 'duration', 'classes', 'school', 'ritual']

        self.window = self.make_window()

        while True:
            button, values = self.window.Read()
            print(button)
            if button is None or button == 'Quit':
                break
            elif button == 'Add':
                self.add(values)
                self.update()
            elif button == 'Replace':
                self.replace(values)
                self.update()
            elif button == 'Highlight':
                pass
            elif button == 'Clear':
                self.rows = []
                self.hl_rows = []
                self.update()
            elif button[:-1] == 'up':
                row = self.rows.pop(int(button[-1]))
                self.hl_rows.append(row)
                self.update()
            elif button[:-1] == 'hl_down':
                row = self.hl_rows.pop(int(button[-1]))
                self.rows.append(row)
                self.update()
            elif button[:-1] == 'hl_del':
                self.hl_rows.pop(int(button[-1]))
                self.update()
            elif button[:-1] == 'del':
                self.rows.pop(int(button[-1]))
                self.update()



    def make_window(self):

        # Set Up Screen Layout
        input_frame= [
                    [sg.Text("Spell Name", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Spell Level", size=(12, 1)), sg.Combo([   'Cantrip',
                                                                        'Level 1',
                                                                        'Level 2',
                                                                        'Level 3',
                                                                        'Level 4',
                                                                        'Level 5',
                                                                        'Level 6',
                                                                        'Level 7',
                                                                        'Level 8',
                                                                        'Level 9',
                                                                        'Any'], default_value='Any', size=(24, 1))],

                    [sg.Text("Casting Time", size=(12, 1)), sg.Combo(['1 Action', '1 Bonus Action', '1 Reaction', 'Other', 'Any'], default_value='Any', size=(24, 1))],
                    [sg.Text("Range", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Duration", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Class", size=(12, 1)), sg.Combo(['Wizard', 'Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Any' ], default_value='Any', size=(24, 1))],
                    [sg.Text("School", size=(12, 1)), sg.Combo(['Abjuration', 'Conjuration', 'Divination', 'Enchantment', 'Evocation', 'Illusion', 'Necromancy', 'Transmutation', 'Any'], default_value='Any', size=(24,1))],
                    [sg.Text("Ritual?", size=(12, 1)), sg.Checkbox('Yes', default=False)],
                    [sg.ReadButton('Add'), sg.ReadButton('Replace'), sg.Button('Highlight'), sg.Button('Clear'), sg.Button('Quit')]]




        # RESULTS FRAME
        results_col = [[    sg.Text("Spell Name", size=(18, 1)),
                            sg.Text("Lvl", size=(5, 1)),
                            sg.Text("Cast Time", size=(10, 1)),
                            sg.Text("Range", size=(15, 1)),
                            sg.Text("Components", size=(12, 1)),
                            sg.Text("Duration", size=(12, 1)),
                            sg.Text("Ritual?", size=(8, 1)),
                            sg.Text("Buttons", size=(10, 1))
                        ], [sg.Text('_'*125)] ]



        # ADD HIGHLIGHTED ROWS HERE
        ii = 0
        for row in self.hl_rows:
            spell_name = row[0]
            level = row[1]
            cast_time = row[2]
            range = row[3]

            if row[4] is not None and '(' in row[4]:
                component_list = row[4].split('(')
                components = component_list[0]
            else:
                components = row[4]
            if row[4] is not None and ' gp ' in row[4]:
                components += " ($)"

            duration = row[5]
            ritual = '  Y' if row[7] else ""


            results_col.append([    sg.Text(spell_name, size=(18, 1)),
                                    sg.Text(level, size=(5, 1)),
                                    sg.Text(cast_time, size=(10, 1)),
                                    sg.Text(range, size=(15, 1)),
                                    sg.Text(components, size=(12, 1)),
                                    sg.Text(duration, size=(12, 1)),
                                    sg.Text(ritual, size=(8, 1)),
                                    sg.Button('↑', key=f'hl_up{ii}'), sg.Button('↓', key=f'hl_down{ii}'), sg.Button('x', key=f'hl_del{ii}')
            ])

            ii += 1 # Add one to index

        results_col.append([sg.Text('_'*125)])

        # ADD NON-HIGHLIGHTED ROWS HERE
        ii = 0
        for row in self.rows:
            spell_name = row[0]
            level = row[1]
            cast_time = row[2]
            range = row[3]

            if row[4] is not None and '(' in row[4]:
                component_list = row[4].split('(')
                components = component_list[0]
            else:
                components = row[4]
            if row[4] is not None and ' gp ' in row[4]:
                components += " ($)"

            duration = row[5]
            ritual = '  Y' if row[7] else ""


            results_col.append([    sg.Text(spell_name, size=(18, 1)),
                                    sg.Text(level, size=(5, 1)),
                                    sg.Text(cast_time, size=(10, 1)),
                                    sg.Text(range, size=(15, 1)),
                                    sg.Text(components, size=(12, 1)),
                                    sg.Text(duration, size=(12, 1)),
                                    sg.Text(ritual, size=(8, 1)),
                                    sg.Button('↑', key=f'up{ii}'), sg.Button('↓', key=f'down{ii}'), sg.Button('x', key=f'del{ii}')
            ])

            ii += 1 # Add one to index

        # Final Frames
        results_frame = [[sg.Column(results_col, scrollable=True, size = (1000, 750))]]

        # Final Layout
        layout = [[ sg.Frame("Selection Criteria", input_frame, vertical_alignment='top', size = (400, 750)),
                    sg.VerticalSeparator(pad=None),
                    sg.Frame("Results", results_frame, vertical_alignment='top', size = (1000, 750))
                ]]
        # create the window

        window = sg.Window(title='Spell Lookup', layout=layout, location=(0,0), element_padding=(5,5), font=(25))
        return window


    def search(self, values):
        # Translate values into a dict for calling database.query_spells(dictionary)
        dict = {}

        if values[0] != "":
            dict["spell_name"] = values[0]
        if values[1] != "Any":
            if values[1] == "Cantrip":
                dict["level"] = 'C'
            else:
                dict["level"] = int(values[1][-1])
        if values[2] != "Any":
            dict["casting_time"] = values[2]
        if values[3] != "":
            dict["range"] = values[3]
        if values[4] != "":
            dict["duration"] = values[4]
        if values[5] != "Any":
            dict["classes"] = values[5]
        if values[6] != "Any":
            dict["school"] = values[6]
        if values[7] == True:
            dict["ritual"] = True

        rows = database.query_spells(dict)
        print([row[0] for row in rows])
        return rows

    def update(self):
        self.window.close()
        self.window = self.make_window()

    # Button Methods

    def add(self, values):
        rows = self.search(values)
        self.rows += rows
        self.update()

    def replace(self, values):
        rows = self.search(values)
        self.rows = rows
        pass

    def highlight(self, values):
        pass

    def up(self):
        pass

    def down(self):
        pass

    def delete(self):
        pass



#------------------ MAIN METHOD ------------------------

if __name__ == "__main__":
    print("\nRunning Main...\n")
    database = Postgres()
    gui = GUI(database)
