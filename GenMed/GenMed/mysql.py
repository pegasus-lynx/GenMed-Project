import MySQLdb
from django.db import connection

def connect():
    return MySQLdb.connect(user="root",passwd="DKumar@14",db="GEN_MED")

def get_userlist(request,c):
    c.execute(
        """ SELECT username from shop """
    )
    res = c.fetchall()
    userlist = [ i[0] for i in res]
    return userlist

def get_max_shopid(request,c):
    c.execute(
        """ select max(shop_id) from shop_info """
    )

    return c.fetchone()[0]

def get_shopid(request,c):
    username = request.user.username
    c.execute(
        """ select user_id from shop
            where username = %s """ ,
            (username,)
    )
    user_id = c.fetchone()[0]
    print(user_id)
    c.execute(
        """ select shop_id from shop_info
            where user_id = %s """,
            (user_id,)
    )
    shop_id = c.fetchone()
    print(shop_id)
    return shop_id

def get_userid(request,c,shop_id):
    c.execute(
        """ select user_id from shop_info
            where shop_id = %s """,
            (shop_id,)
    )
    return c.fetchone()[0]

def get_userid_by_name(request,c):
    username = request.user.username
    c.execute(
        """ select user_id from shop
            where username = %s """,
            (username,)
    )
    return c.fetchone()

def get_medid(request,c,gen_name):
    c.execute(
        """ select med_id from med_info
            where lower(gen_name) = %s """,
            (gen_name.lower(),)
    )
    med_id = c.fetchone()[0]
    print(med_id)
    return med_id

def get_userinfo(request,c,shop_id):

    user_id = get_userid(request,c,shop_id)
    c.execute(
        """ select username,first_name,last_name,email
            from shop where user_id = %s """,
            (user_id,)
    )
    keys = [ 'username','first_name','last_name','email']
    res = c.fetchone()

    user_info = []
    for i in range(len(keys)):
        user_info[i] = tuple(keys[i],res[i])

    print(user_info)
    return user_info

def get_license(request,c,shop_id):
    c.execute(
        """ select SL.license,SL.dr_license_no,PD.ph_id,PD.name,PD.deg,PD.college
            from shop_license as SL inner join ph_detail as PD on 
            PD.ph_id = SL.ph_id
            where SL.shop_id = %s """,
            (shop_id,)
    )
    keys = [ "license", "drug_license", "ph_id","ph_name","deg","college"]
    res = c.fetchone()
    shop_license = []
    for i in range(len(keys)):
        shop_license.append([keys[i],res[i]])
    return shop_license

def get_curstock(request,c,shop_id):
    c.execute(
        """ select med_info.med_id,med_info.gen_name,avail.units,avail.price,avail.batch,avail.mfg_date,avail.exp_date
            from med_info,avail
            where avail.shop_id = %s and med_info.med_id=avail.med_id""",
            (shop_id,)
    )

    res = map(list,c.fetchall())

    cur_stock = {}
    for i in res:
        cur_stock[i[0]]=i[1:]

    print(cur_stock)
    return cur_stock

def get_shopinfo(request,c,shop_id):
    c.execute(
        """ select name,owner_name,mob_no,alt_no 
            from shop_info where shop_id = %s""",
            (shop_id,)
    )

    keys = ["shop_name","owner_name","mob_no","alt_no"]
    res = c.fetchone();

    shop_info = []
    for i in range(len(keys)):
        shop_info.append([keys[i],res[i]])

    return shop_info

def get_shoploc(request,c,shop_id):
    c.execute(
        """ select city,district,state
            from shop_loc where shop_id = %s """,
            (shop_id,)
    )
    keys = ["city","district","state"]
    res = c.fetchone();

    shop_loc = []
    for i in range(len(keys)):
        shop_loc.append([keys[i],res[i]])

    return shop_loc
