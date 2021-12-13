

"""
This is a tool meant for easy dungeons and dragons spell lookup and to practice SQL skills. This python program
using a Postgres database to store the list of all spells. I used PySimpleGUI to make a nice simple GUI to view
spells easily in-game. Since my friends and I only have the Players Handbook (5e), it is annoying to look up spells
on the internet as there are many spells that are in other expansions, so this program only contains info from that book.

Some ideas for the program that may/may not be implemented

Combat simulator:

Keeps track of the move order, status of your character(prone/upright/concentration/health/etc)
and what actions you can do in a given turn, move, disengage, help, all your available
spells (greyed out if you don't have prepared or spell slots or something)

Level Up/Learn New Spells Simulator Simulator:
Hard Coded rules about what spells you can get if you level up. Will include a menu of all possible spells you want.
Can select a list of favorite to consider and they will show up with their descriptions so you can narrow down the list

There should always be a button called "Spell Lookup" and you can put your criteria for a bunch of spells and it will bring them up. The level up/learn new spells
simulator will use the code for this feature to look up the correct spells

Ideally this tool will be able to save profiles (using another table in the db)


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
# External Packages
import psycopg2
import PySimpleGUI as sg

# Homemade imports
from database import Postgres
from gui import GUI



#------------------ MAIN METHOD ------------------------

if __name__ == "__main__":
    print("\nRunning Main...\n")
    database = Postgres()


    gui = GUI(database)
