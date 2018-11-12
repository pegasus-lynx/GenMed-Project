import MySQLdb
from datetime import datetime as dt

def connect():
    return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

db=connect()
c=db.cursor()

# for i in range(6,26):
#     ch = chr(97+i)
#     print(ch)
#     c.execute(
#         """ update shop
#             set username = %s
#             where shop_id = %s """,
#             (ch,i+1,)
#     )
#     db.commit()

c.execute(
    """ select * from avail """
)

rows = list(c.fetchall())
row = []
for i in rows:
    row.append(list(i))

for i in row:
    
    mfg_mon = str(i[4].month)
    if len(mfg_mon)==1:
        mfg_mon = '0'+mfg_mon

    exp_mon = str(i[5].month)
    if len(exp_mon)==1:
        exp_mon = '0'+exp_mon
    i[6] = chr(65+i[0])+chr(65+i[1])+mfg_mon+str(i[4].year)[2:]+exp_mon+str(i[5].year)[2:]
    print(i)

    c.execute(
        """ update avail
            set batch = %s
            where med_id = %s and shop_id = %s """ ,
            (i[6],i[0],i[1],)
    )

    db.commit()