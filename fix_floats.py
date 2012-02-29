__author__ = 'therms'

import sqlite3
import os

db_filename = 'profile.db'

db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    profile_id = '117177689300294532641'

    cursor = conn.cursor()

    dates = cursor.execute("SELECT id, datetime FROM follower_count")


    fixed_dates = []
    for row in dates:
#        print row[0], int(row[1])
        new_row = (row[0], int(row[1]))
        fixed_dates.append(new_row)

    for row in fixed_dates:
        print row[0], row[1]
        cursor.execute("UPDATE follower_count SET datetime=? WHERE id=?", (row[1], row[0]))

    cursor.execute ("SELECT datetime FROM follower_count")

    print cursor.fetchall()


