from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from tables import User, Device, Data, Base
from auth import MyBasicAuth
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs

app = Eve(validator=ValidatorSQL, data=SQL, auth=MyBasicAuth)
Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')
# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()

# Insert some example data in the db
# if not db.session.query(People).count():
#     import example_data
#     for item in example_data.test_data:
#         db.session.add(People.from_tuple(item))
#     db.session.commit()

app.run(debug=True, use_reloader=False)  # using reloaded will destory in-memory sqlite db




