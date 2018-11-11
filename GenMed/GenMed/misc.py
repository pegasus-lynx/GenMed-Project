import MySQLdb

def connect():
    return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

db=connect()
c=db.cursor()
print(chr(97))
for i in range(6,26):
    ch = chr(97+i)
    print(ch)
    c.execute(
        """ update shop
            set username = %s
            where shop_id = %s """,
            (ch,i+1,)
    )
    db.commit()