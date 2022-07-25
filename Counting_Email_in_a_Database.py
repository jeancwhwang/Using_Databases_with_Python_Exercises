''' Learning Objectives: 
    1. Use Python to count the number of email messages per organization (e.g., the domain name of the email address) from the mbox text file.
    2. Get the sqlite database with the schema '''CREATE TABLE Counts (org TEXT, count INTEGER)''' to maintain the counts.
    3. The the mbox.txt can be found here: https://www.py4e.com/code3/mbox.txt?PHPSESSID=0247e4414c5c3134ae1d5b4223d317bc
'''

import sqlite3

conn = sqlite3.connect('orgdb.sqlite') # connect a file & create a dbfile
cur = conn.cursor() 

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name:')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From:'): continue
    pieces = line.split()
    email = pieces[1]
    org = email.split('@')[1]
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org,)) #? 
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
        VALUES (?, 1) ''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))

    conn.commit()

#http://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in conn.execute(sqlstr):
    print(str(row[0]), row[1])
cur.close()
