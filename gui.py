
import PySimpleGUI as sg

import database as db



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

            if values[0] == "" and values[1] == 'Any' and values [2] == "Any" and values[3] == '' and values[4] == '' and values[5] == 'Any' and values[6] == 'Any' and values[7]== False:
                blank = True
            else:
                blank = False

            # Split on numbers
            if button[-2].isdigit():
                button_num = int(button[-2:])
                button = button[:-2]
            elif button[-1].isdigit():
                button_num = int(button[-1])
                button = button[:-1]
            else:
                button_num = None


            if button is None or button == 'Quit':
                break
            elif button == 'Add':
                if blank:
                    continue
                self.add(values)
                self.update()
            elif button == 'Replace':
                if blank:
                    continue
                self.replace(values)
                self.update()
            elif button == 'Highlight':
                pass
            elif button == 'Clear':
                self.rows = []
                self.hl_rows = []
                self.update()
            elif button == 'up':
                row = self.rows.pop(button_num)
                self.hl_rows.append(row)
                self.update()
            elif button == 'hl_down':
                row = self.hl_rows.pop(button_num)
                self.rows.append(row)
                self.update()
            elif button == 'hl_del':
                self.hl_rows.pop(button_num)
                self.update()
            elif button == 'del':
                self.rows.pop(button_num)
                self.update()
            elif button == 'hl_spell_name':
                print(self.hl_rows[button_num][0])
                print("-------------")
                print(self.hl_rows[button_num][10])
                print("")
            elif button == 'spell_name':
                print(self.rows[button_num][0])
                print("-------------")
                print(self.rows[button_num][10])
                print("")
            elif button == 'hl_info':
                row = self.hl_rows[button_num]
                sg.popup(self.make_popup_text(row), font=(35), line_width=150)

            elif button == 'info':
                row = self.rows[button_num]
                sg.popup(self.make_popup_text(row), font=(35), line_width=150)

    def make_popup_text(self, row):
        string = row[0]
        string += "\n----------------\n"
        string += f"Level: {row[1]}\n"
        string += f"Casting Time: {row[2]}\n"
        string += f"Range: {row[3]}\n"
        string += f"Components: {row[4]}\n"
        string += f"Duration: {row[5]}\n"
        string += f"Classes: {row[6]}\n"
        string += f"Ritual: {row[7]}\n"
        string += f"Concentration: {row[8]}\n"
        string += f"School: {row[9]}\n"
        string += f"\nDescription:\n\n"
        string += row[10]

        return string


    def make_window(self):

        # Set Up Screen Layout
        input_frame= [
                    [sg.Text("Spell Name", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Spell Level", size=(12, 1)), sg.Combo([
                                                                        'Cantrip',
                                                                        'Level 1',
                                                                        'Level 2',
                                                                        'Level 3',
                                                                        'Level 4',
                                                                        'Level 5',
                                                                        'Level 6',
                                                                        'Level 7',
                                                                        'Level 8',
                                                                        'Level 9'], default_value='Any', size=(24, 1))],

                    [sg.Text("Casting Time", size=(12, 1)), sg.Combo(['1 Action', '1 Bonus Action', '1 Reaction', 'Other', 'Any'], default_value='Any', size=(24, 1))],
                    [sg.Text("Range", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Duration", size=(12, 1)), sg.InputText(size=(36, 1))],
                    [sg.Text("Class", size=(12, 1)), sg.Combo(['Wizard', 'Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Any' ], default_value='Any', size=(24, 1))],
                    [sg.Text("School", size=(12, 1)), sg.Combo(['Abjuration', 'Conjuration', 'Divination', 'Enchantment', 'Evocation', 'Illusion', 'Necromancy', 'Transmutation', 'Any'], default_value='Any', size=(24,1))],
                    [sg.Text("Ritual?", size=(12, 1)), sg.Checkbox('Yes', default=False)],
                    [sg.Button('Add'), sg.Button('Replace'), sg.Button('Highlight'), sg.Button('Clear'), sg.Button('Quit')]]




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
            if row[4] is not None and ' gp' in row[4]:
                components += " ($)"

            duration = row[5]
            ritual = '  Y' if row[7] else ""


            results_col.append([    sg.Button(spell_name, size=(18, 1), key=f'hl_spell_name{ii}'),
                                    sg.Text(level, size=(5, 1)),
                                    sg.Text(cast_time, size=(10, 1)),
                                    sg.Text(range, size=(15, 1)),
                                    sg.Text(components, size=(12, 1)),
                                    sg.Text(duration, size=(12, 1)),
                                    sg.Text(ritual, size=(8, 1)),
                                    sg.Button('↑', key=f'hl_up{ii}'), sg.Button('↓', key=f'hl_down{ii}'), sg.Button('x', key=f'hl_del{ii}'), sg.Button('?', key=f'hl_info{ii}')
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
            if row[4] is not None and ' gp' in row[4]:
                components += " ($)"

            duration = row[5]
            ritual = '  Y' if row[7] else ""


            results_col.append([    sg.Button(spell_name, size=(18, 1), key=f'spell_name{ii}'),
                                    sg.Text(level, size=(5, 1)),
                                    sg.Text(cast_time, size=(10, 1)),
                                    sg.Text(range, size=(15, 1)),
                                    sg.Text(components, size=(12, 1)),
                                    sg.Text(duration, size=(12, 1)),
                                    sg.Text(ritual, size=(8, 1)),
                                    sg.Button('↑', key=f'up{ii}'), sg.Button('↓', key=f'down{ii}'), sg.Button('x', key=f'del{ii}'), sg.Button('?', key=f'info{ii}')
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
                dict["level"] = '0'
            else:
                dict["level"] = int(values[1][-1])
        if values[2] != "Any":
            dict["casting_time"] = values[2].lower()
        if values[3] != "":
            dict["range"] = values[3].lower()
        if values[4] != "":
            dict["duration"] = values[4].lower()
        if values[5] != "Any":
            dict["classes"] = values[5]
        if values[6] != "Any":
            dict["school"] = values[6]
        if values[7] == True:
            dict["ritual"] = True

        rows = self.database.query_spells(dict)
        return rows

    def update(self):
        self.window.close()
        self.window = self.make_window()

    def sort_func(self, row):
        return row[0]

    # Button Methods

    def add(self, values):
        rows = self.search(values)
        rows.sort(key=self.sort_func)
        self.rows += rows
        self.update()

    def replace(self, values):
        rows = self.search(values)
        self.rows = rows
        self.rows.sort(key=self.sort_func)
        pass

    def highlight(self, values):
        pass
