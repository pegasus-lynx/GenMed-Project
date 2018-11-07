# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import check_password
# import MySQLdb

# def connect():
#     return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

# # class MyBackend(object):

# #     # def get_user(self, user_id):
# #     #     MyUser =  get_user_model()
# #     #     try:
# #     #         return MyUser.object.get(username=username)
# #     #     except UserModel.DoesNotExist:

# #     #         return None

# #     def authenticate(self, username=None, password=None):
# #         UserModel = get_user_model()
# #         if username is None:
# #             # raise Error
        
# #         db.connect()
# #         c=db.cursor()
# #         # try:
# #         c.execute(
# #             """ select  username,password from shop
# #                 where username = %s and password = %s """,
# #                 (username,SHA(password),)
# #         )

# #         x = c.fetchall()

# #         if x is None:
# #             # raise an error where Username does not exist
# #         else:
# #             user = UserMod
# #             # user = UserModel._default_manager.get_by_natural_key(username)
# #             # if user.check_password(password):
# #             #     return user
# #             # except UserModel.DoesNotExist:
# #             # Run the default password hasher once to reduce the timing
# #             # difference between an existing and a non-existing user (#20760).

# #             # UserModel().set_password(password)

# # # from django.contrib.auth.models import User

# class MyBackend(object):
#     """
#     Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

#     Use the login name, and a hash of the password. For example:

#     ADMIN_LOGIN = 'admin'
#     ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
#     """

#     def get_user(self, username):
#     try:
#         return MyUser.objects.get(username=username)
#     except MyUser.DoesNotExist:
#         return None

#     def authenticate(self, username=None, password=None):
#         UserModel = get_user_model()
#         # if username is None:
#         #     raise 
#         db.connect()
#         c=db.cursor()
#         c.execute(
#             """ select  username,password from shop
#                 where username = %s and password = %s """,
#                 (username,check_password(password,)
#         )
#         cred = c.fetchall()
#         if cred is not None:
#             try:
#                 user = MyUser.objects.get(username=username)
#             except MyUser.DoesNotExist:
#                 c.execute(
#                     """ select * from shop
#                         where username = %s """,
#                         (username,)
#                 )
#                 cred = c.fetchone()
#                 # user = MyUser(username=cred[0], password=cred[1], email=cred[2])
#                 # user.save()
#             return user
#         return None