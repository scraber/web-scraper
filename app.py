from flask import Flask
from flask_restful import Api, Resource

from db import db, migrate
from resources.image import PageImageListView, PageImageView
from resources.text import PageTextListView, PageTextView

app = Flask(__name__)
app.config.from_object('config.Config')
api = Api(app)
db.init_app(app)
migrate.init_app(app, db)


api.add_resource(PageTextView, '/text')
api.add_resource(PageTextListView, '/texts')
api.add_resource(PageImageView, '/image')
api.add_resource(PageImageListView, '/images')