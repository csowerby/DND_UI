


"""
This is a tool meant for easy dungeons and dragons spell lookup and to practice SQL skills. This python program using a
Postgres database to store the list of all spells. I intend to use a pygame to make a nice gui so its easy to use while playing actual dnd

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

"""

import psycopg2

if __name__ == "__main__":
    print("Starting...")

    test_num = 1


    connection = psycopg2.connect(
    host="localhost",
    database="dnd",
    user="postgres",
    password="")

    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM spells WHERE level={test_num};")
    rows = cursor.fetchall()

    for row in rows:
        print(row)
