# from eve import Eve
# from eve.auth import BasicAuth
# from eve.auth import TokenAuth
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask import current_app as app
# from tables import User
# from api import db
#
# class MyBasicAuth(BasicAuth):
#     def check_auth(self, username, password, allowed_roles, resource, method):
#         print('resource={}'.format(resource))
#         if resource in ('devices','data','users'):
#             return True
#         else:
#             # all the other resources are secured
#             return username == 'admin' and password == 'secret'
#
# class MySecondAuth(BasicAuth):
#     def check_auth(self, username, password, allowed_roles, resource, method):
#         return username == 'admin' and password == 'secret2'
#
#
# class Sha1Auth(BasicAuth):
#     def check_auth(self, username, password, allowed_roles, resource, method):
#         account = db.session.query(User).filter_by(email='cristianlupu2@gmail.com').first()
#         print(account)
#         return account and \
#             check_password_hash(account['password'], password)
#
#
# class TokenAuth(TokenAuth):
#     def check_auth(self, token, allowed_roles, resource, method):
#         """For the purpose of this example the implementation is as simple as
#         possible. A 'real' token should probably contain a hash of the
#         username/password combo, which sould then validated against the account
#         data stored on the DB.
#         """
#         # use Eve's own db driver; no additional connections/resources are used
#         accounts = app.data.driver.db['accounts']
#         return accounts.find_one({'token': token})

