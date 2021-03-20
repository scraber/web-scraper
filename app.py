from flask import Flask

from db import db, migrate


app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate.init_app(app, db)





