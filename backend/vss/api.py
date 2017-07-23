# -*- coding: utf8 -*-

from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from models import Base, User, Device, Base, Input
from views import register_views
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs
from eve.auth import BasicAuth
from eve.auth import TokenAuth
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app as app, abort

import logging
from logging import FileHandler
file_handler = FileHandler('api.log')
file_handler.setLevel(logging.INFO)

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


class Sha1Auth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        app.logger.info('username={}|password={}|allowed_roles={}|resource={}|method={}'.format
                        (username,password,allowed_roles,resource,method))
        if (username == 'admin@domain'):
            return password == 'secret'
        account = db.session.query(User).filter_by(login=username).first()
        try:
            if (account.id_user > 0):
                self.set_request_auth_value(account.id_user)
        except AttributeError:
            abort(401)
        # import pdb; pdb.set_trace()
        return account and account.check_password(password)
               # check_password_hash(account.password, password)


# class TokenAuth(TokenAuth):
#     def check_auth(self, token, allowed_roles, resource, method):
#         """First we are verifying if the token is valid. Next
#         we are checking if user is authorized for given roles.
#         """
#         login = User.verify_auth_token(token)
#         # if login and allowed_roles:
#         if login:
#             # user = app.data.driver.session.query(User).get(login)
#             # return user.isAuthorized(allowed_roles)
#             return True
#         else:
#             return False

app = Eve(validator=ValidatorSQL,data=SQL, auth=Sha1Auth)
# register_views(app)
# app.logger.addHandler(file_handler)
# enable Eve-docs
Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')
# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.drop_all()
db.create_all()



# Insert some example data in the db
# if not db.session.query(People).count():
#     import example_data
#     for item in example_data.test_data:
#         db.session.add(People.from_tuple(item))
#     db.session.commit()

# new_user = User(name='Test User1',login='test1@domain.com',password='secret')
# new_user2 = User(name='Test User2',login='test2@domain.com',password='secret2')
# db.session.add(new_user)
# db.session.add(new_user2)
# new_device = Device(name='Device1', serial='123456', user=new_user)
# new_device2 = Device(name='Device2', serial='654321', user=new_user2)
# db.session.add(new_device)
# db.session.add(new_device2)
# new_data = Temperature(value='33', id=1, device=new_device)
# new_data2 = Temperature(value='37', id=2, device=new_device2)
# db.session.add(new_data)
# db.session.add(new_data2)
db.session.commit()
#
# print(db.session.query(User).count())
# print(db.session.query(User).filter_by(login='cristianlupu@gmail.com').first())

# import pdb; pdb.set_trace()
app.run(host='0.0.0.0',debug=True, use_reloader=False)  # using reloaded will destory in-memory sqlite db
# import pdb; pdb.set_trace()




