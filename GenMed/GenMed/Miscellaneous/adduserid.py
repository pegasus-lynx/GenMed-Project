import MySQLdb
from datetime import datetime as dt

def connect():
    return MySQLdb.connect(user="root",passwd="DKumar@14",db="GEN_MED")

db=connect()
c=db.cursor()

c.execute(
    """ select * from shop_info """
)

rows = list(c.fetchall())
row = []
for i in rows:
    row.append(list(i))

for i in row:

    c.execute(
        """ update shop_info
            set user_id = %s
            where shop_id = %s """ ,
            (i[0],i[0],)
    )
    print(i[0])
    db.commit()