import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, abort, jsonify
from flask import request, make_response, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from .models import Base
from api import config
from .forms import UserForm
from .models import User, Data, Device
from flask_restful import Resource, Api, reqparse, abort
#from flask.ext.restless import APIManager
from flask_restless_swagger import SwagAPIManager as APIManager



app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
db.Model = Base
api = Api(app)
manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'], collection_name='user', results_per_page=5, allow_functions=True)
manager.create_api(Device, methods=['GET', 'POST', 'DELETE', 'PUT'], collection_name='device', results_per_page=5, allow_functions=True)
manager.create_api(Data, methods=['GET', 'POST', 'DELETE', 'PUT'], collection_name='data', results_per_page=5, allow_functions=True)

# def init_db():
#           with closing(connect_db()) as db:
#                   with app.open_resource('schema.sql',mode='r') as f:
#                           db.cursor().executescript(f.read())
#                           db.commit()
#
# def connect_db():
#           return sqlite3.connect(app.config['DATABASE'])
#
#
# DATABASE = 'api.db'
# DEBUG =  True
#



# app.logger.debug(__name__)
# app.logger.debug(SQLALCHEMY_DATABASE_URI)

#
# @app.before_request
# def before_request():
#           g.db = connect_db()
#
# @app.teardown_request
# def teardown_request(exception):
#           db = getattr(g,'db',None)
#           if db is not None:
#                   db.close()
#

# @app.route('/user/')
# def user_list():
#   """Provide HTML listing of all users."""
#   # Query: Get all User objects, sorted by date.
#   usrs = (db.session.query(User)
#     .order_by(User.created.asc()).all())
#   return render_template('user/index.html',
#     usrs=usrs)
#
# @app.route('/user/create/', methods=['GET', 'POST'])
# def user_create():
#   """Provide HTML form to create a new user."""
#   form = UserForm(request.form)
#   if request.method == 'POST' and form.validate():
#     usr = User()
#     form.populate_obj(usr)
#     db.session.add(usr)
#     db.session.commit()
#     # Success. Send user back to full user list.
#     return redirect(url_for('user_list'))
#   # Either first load or validation error at this point.
#   return render_template('user/edit.html', form=form)


# @app.route('/')
# def get_posts():
#           cur = g.db.execute('SELECT title, text FROM posts ORDER BY id DESC ')
#           posts = [dict(title=row[0], text=row[1])
#                            for row in cur.fetchall()]
#           return render_template('base.html', posts=posts)
#
#
# def hello_world():
#           return 'Hello World!'
#
#
# @app.route('/api/v1/posts/',methods=['GET'])
# def show_entries():
#           cur = g.db.execute('SELECT title, text FROM posts ORDER BY id DESC ')
#           posts = [dict(title=row[0], text=row[1])
#                            for row in cur.fetchall()]
#           return jsonify({'count':len(posts),'posts':posts})
#
# @app.route('/api/v1/posts/<int:post_id>',methods=['GET', 'DELETE'])
# def single_post(post_id):
#           method = request.method
#           if method == 'GET':
#                   cur = g.db.execute('SELECT title, text FROM posts WHERE id = ?', [post_id])
#                   posts = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
#                   return jsonify({'count':len(posts), 'posts':posts})
#           elif method == 'DELETE':
#                   g.db.execute('DELETE FROM posts WHERE id = ?', [post_id])
#                   return jsonify({'status':"Post deleted"})

@app.route('/bootstrap/')
def bootstrap():
    return render_template('index.html')



def dump_request_detail(request):
  request_detail = """
# before request #
request.endpoint: {request.endpoint}
request.method: {request.method}
request.view_args: {request.view_args}
request.args: {request.args}
request.form: {request.form}
request.user_agent: {request.user_agent}
request.files: {request.files}
request.is_xhr: {request.is_xhr}

## request.headers ##
{request.headers}
  """.format(request=request).strip()
  return request_detail

# @app.before_request
# def callme_before_every_request():
#   # demo only: the before_request hook.
#   app.logger.debug(dump_request_detail(request))
#
# @app.after_request
# def callme_after_every_response(response):
#   # demo only: the after_request hook.
#   app.logger.debug('# after request #\n' + repr(response))
#   return response

# @app.before_request
# def g_before_request():
#     x = random.randint(1,9)
#     app.logger.debug('before request, g(x)={x}'.format(x=x))
#     g.x = x
#
# @app.after_request
# def g_after_request(response):
#     app.logger.debug('after request, g(x)={g.x}'.format(g=g))
#     return response

# @app.route('/string/')
# def return_string():
#   return 'hello, world!'
#
# @app.route('/object/')
# def return_object():
#   headers = {'content-type': 'text/plain'}
#   return make_response('hello, world!', 200,
#     headers)
#
# @app.route('/tuple/')
# def return_tuple():
#   return 'hello, world!', 200, {'content-type':
#     'text/plain'}

# @app.errorhandler(404)
# def error_not_found(error):
#     """Render a custom template when page not found."""
#     return render_template('error/not_found.html'), 404



# USERS = {
#     '1': {'name': 'Cristian Lupu', 'email': 'cristianlupu@gmail.com', 'password':'secret'},
#     '2': {'name': 'Roxana Cazacu', 'email': 'roxana.cazacu93@gmail.com', 'password':'secret'},
#     '3': {'name': 'Daniel Rosner', 'email': 'rosner.daniel@gmail.com', 'password':'secret'},
# }
#
# # app.logger.debug(USERS)
#
# def abort_if_user_doesnt_exist(id):
#     """Aborts if user does not exist"""
#     if id not in USERS:
#         abort(404, message="User with id {} doesn't exist".format(id))
#
# parser = reqparse.RequestParser()
# parser.add_argument('name', required=True, type=str, help='Input a name')
# parser.add_argument('email', required=True, type=str, help='Input an e-mail')
# parser.add_argument('password', required=True, type=str, help='Input a password')
#
# class UserApi(Resource):
#     """Handles a single user entry"""
#     def get(self, id=None):
#         """Returns 404 Not Found error if there is no user, else prints the list of users or user info"""
#         if id == None:
#             return USERS
#         abort_if_user_doesnt_exist(id)
#         return USERS[id]
#
#     def delete(self, id):
#         """Returns 404 Not Found error if the user id does not exist, else delete the entry and returns 204 No Content"""
#         abort_if_user_doesnt_exist(id)
#         del USERS[id]
#         return '', 204
#
#     def put(self, id):
#         """Adds an user with a given id, returns 201 Created"""
#         args = parser.parse_args()
#         user = {'name': args['name'], 'email': args['email'], 'password':args['password']}
#         USERS[id] = user
#         return user, 201
#
#     def post(self):
#         """Creates a new user with an autoincremented id (not specified), returns 201 Created"""
#         args = parser.parse_args()
#         app.logger.debug(args['name'])
#         app.logger.debug(args['email'])
#         app.logger.debug(args['password'])
#
#         id = str(int(max(USERS.keys())) + 1)
#         user = {'name': args['name'], 'email': args['email'], 'password':args['password']}
#         USERS[id] = user
#         return USERS[id], 201
#
# ##
# ## Actually setup the Api resource routing here
# ##
# api.add_resource(UserApi, '/user','/user/<id>')


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug = True)
