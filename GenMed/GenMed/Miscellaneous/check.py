import MySQLdb
username=input('Enter the user name:')

def connect():
    return MySQLdb.connect(user="root",passwd="DKumar@14",db="GEN_MED")


db=connect()
c=db.cursor()
c.execute(
    """ select user_id from shop
        where username = %s """,
        (username,)
)
user_id = c.fetchone()
print(user_id,type(user_id))