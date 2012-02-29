import sqlite3
import CairoPlot
import os

db_filename = 'profile.db'

db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        #create db
        print 'Creating schema'
        conn.execute("""
        create table follower_count (
            id          integer primary key autoincrement not null,
            profile     text,
            datetime    integer,
            followers   integer)
        """)

    else:
        #don't
        print 'Database exists.  Assuming schema does too'

    profile_id = '117177689300294532641'

    cursor = conn.cursor()

    cursor.execute("select datetime, followers from follower_count where profile = ?", (profile_id,))

    results = cursor.fetchall()

    data = {profile_id: []}
    legend = []
    for datum in results:
        data[profile_id].append(int(datum[1]))
        legend.append(datum[0])

#    print data
#    print legend

    CairoPlot.dot_line_plot("test", data, 1000, 500, h_labels = legend, axis = True, grid = True)

