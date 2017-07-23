from flask import Flask
from flask_admin import Admin

app = Flask(__name__)

admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here

app.run()