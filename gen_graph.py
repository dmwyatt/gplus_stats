import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
import matplotlib.dates
from matplotlib.ticker import FormatStrFormatter
import sqlite3
import os
import sys

db_filename = sys.argv[1]

db_is_new = not os.path.exists(db_filename)

out_file = sys.argv[2]

try:
    hours_to_graph = int(sys.argv[3])
except:
    hours_to_graph = 100000

print "Processing: " + db_filename
print "Saving to: " + out_file

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

    #all data
    data = {profile_id: []}
    legend = []
#    for datum in results:
#        data[profile_id].append(int(datum[1]))
#        legend.append(datum[0])

    now = int(time.time())
    hours_in_the_past = hours_to_graph*60*60


    for datum in results:
#        if hours_to_graph > -1:
        diff = now-datum[0]

        if diff < hours_in_the_past:
            data[profile_id].append(int(datum[1]))
            legend.append(datum[0])
#        else:
#            data[profile_id].append(int(datum[1]))
#            legend.append(datum[0])

    fig = plot.figure()
    ax = fig.add_subplot(111)

    hfmt = matplotlib.dates.DateFormatter('%m/%d %H:%M')
    ax.xaxis.set_major_formatter(hfmt)

#    formy = matplotlib.ticker.ScalarFormatter()
#    formy.set_scientific(False)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

    plot.plot(matplotlib.dates.epoch2num(legend), data[profile_id])
    fig.autofmt_xdate(rotation=90)
    plot.savefig(out_file)

    print "Saved %d data points" % len(data[profile_id])
