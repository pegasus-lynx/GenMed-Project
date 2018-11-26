import MySQLdb
from django.db import connection

# this function is to connect to the database
def connect():
    return MySQLdb.connect(user="root",passwd="DKumar@14",db="GEN_MED")

# this function returns the list of username
def get_userlist(request,c):
    c.execute(
        """ SELECT username from shop """
    )
    res = c.fetchall()
    userlist = [ i[0] for i in res]
    return userlist

# this function returns the maximum shop_id
def get_max_shopid(request,c):
    c.execute(
        """ select max(shop_id) from shop_info """
    )

    return c.fetchone()[0]

# This function is to get the shop_id from the request.username
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

# This function is used to get the user_id
def get_userid(request,c,shop_id):
    c.execute(
        """ select user_id from shop_info
            where shop_id = %s """,
            (shop_id,)
    )
    return c.fetchone()[0]

# This function is used to get the user_id from the request.user
def get_userid_by_name(request,c):
    username = request.user.username
    c.execute(
        """ select user_id from shop
            where username = %s """,
            (username,)
    )
    return c.fetchone()

# This function is used to get the med_id of the given gen_name
def get_medid(request,c,gen_name):
    c.execute(
        """ select med_id from med_info
            where lower(gen_name) = %s """,
            (gen_name.lower(),)
    )
    med_id = c.fetchone()[0]
    print(med_id)
    return med_id

# this function is used to get the medicine info from the given name
def get_med(request,c,name):
    c.execute(
        """ select med_id from med_info
            where lower(gen_name) = %s """,
            (name.lower(),)
    )

    med_id = c.fetchone()

    if med_id is not None:
        return med_id

    c.execute(
        """ select med_id from com_name
            where lower(custom_name) = %s """,
            (name.lower(),)
    )

    med_id = c.fetchone()

    return med_id

# This function is used t get the information of the logged in user
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

# This is used to get the shop license information for a given shop_id
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

# This is used to get the current stock information for a given shop id
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

# This is used to get the shopinfo from the given shop_id
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

# this iis used to get the shop location of the shop from the shop_id
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

# This is used to get the coordinates of the shop from the given shop_id
def get_shopcord(c,shop_id):
    c.execute(
        """ select  lat,lon from shop_loc
            where shop_id = %s """,
            (shop_id,)
    )

    cord = list(c.fetchone())
    print(cord)
    return cord

# This is used to get the shop list from the available medicines in the app
def get_shops_by_med(request,c,med_id):
    c.execute(
        """ select avail.shop_id,shop_info.name,avail.units,avail.price
            from avail inner join shop_info on avail.shop_id=shop_info.shop_id
            where avail.med_id = %s """,
            (med_id,)
    )
    res = list(c.fetchall())
    shops = {}

    for i in range(len(res)):
        shops[res[i][0]]=list(res[i][1:])
    print(shops)
    return shops

# This is used to get the list of all shop ids
def get_shopid_list(c):
    c.execute(
        """ select shop_id from shop_info """
    )
    res = c.fetchall()
    shop_ids = [i[0] for i in res]
    print(shop_ids)
    return  shop_ids

# This is used to get the city    
def get_city(c,shop_id):
    c.execute(
        """ select city from shop_loc
            where shop_id = %s """ ,
            (shop_id,)
    )

    return c.fetchone()

# This is to get the shop name list
def get_shopname_list(c):
    c.execute(
        """ select name from shop_info """
    )

    res = list(c.fetchall())
    shopname = []
    for i in res:
        shopname.append(i[0])
    print(shopname)
    return shopname

# This is to get the shop_id by the name of the shop
def get_shopid_by_name(c,shop_name):
    c.execute(
        """ select shop_id from shop_info
            where name = %s """ ,
            (shop_name,)
    )

    return c.fetchone()[0]

# This is to get the shop name and shop location from the shop_id
def get_shop_search(c,shop_id):
    c.execute(
        """ select shop_info.name, shop_loc.city
            from shop_info inner join shop_loc using(shop_id)
            where shop_id = %s """ ,
            (shop_id,)
    )

    return list(c.fetchone())

# This is used to get the shop in a single city
def get_shop_by_city(c,city):
    c.execute(
        """ select SI.shop_id,SI.name,SL.city
            from shop_info as SI, shop_loc  as SL
            where SI.shop_id = SL.shop_id and SL.city = %s """ ,
            (city,)
    )
    res = list(c.fetchall())
    shops = {}
    for i in res:
        shops[i[0]]=list(i[1:])
    return shops
