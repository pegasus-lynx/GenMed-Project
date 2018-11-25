import MySQLdb
from datetime import datetime as dt

def connect():
    return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

db=connect()
c=db.cursor()

c.execute(
    """ select * from shop """
)

rows = list(c.fetchall())
row = []
for i in rows:
    row.append(list(i))

for i in row:

    c.execute(
        """ update shop
            set shop_id = %s
            where user_id = %s """ ,
            (i[0],i[0],)
    )

    db.commit()