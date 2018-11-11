import MySQLdb
import hashlib as hl

def connect():
    return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

db=connect()
c=db.cursor()

for i in range(0,26):
    ch = chr(97+i)
    ch+=str(i)
    # print(ch)
    hash_object = hl.sha256(ch.encode('utf-8'))
    pwd=hash_object.hexdigest()
    c.execute(
        """ update shop
            set passwd = %s
            where shop_id = %s """,
            (pwd,i+1,)
    )
    db.commit()