from celery import Celery
from flask import Flask
from flask_restful import Api

from db import db, migrate

import os


app = Flask(__name__)
app.config.from_object('config.Config')
api = Api(app)
db.init_app(app)
migrate.init_app(app, db)

celery = Celery(app.name, backend=os.environ.get("CELERY_BACKEND"), broker=os.environ.get("CELERY_BROKER"))
celery.conf.update(task_serializer='json')
TaskBase = celery.Task

# http://matrix.umcs.lublin.pl/DOC/python-flask-doc/rst/patterns/celery.txt
class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

celery.Task = ContextTask

# app must be fully loaded at this stage
from resources.api import PageTaskStatus, PageTextTask, PageImageTask, PageImageView, PageImageListView, PageTextView,PageTextListView
# tasks must be imported, otherwise celery doesn't register them
from tasks.tasks import scrape_text, scrape_images    

api.add_resource(PageTaskStatus, '/scraper/status')

api.add_resource(PageTextTask, '/scraper/text')
api.add_resource(PageImageTask, '/scraper/image')

api.add_resource(PageImageView, '/image')
api.add_resource(PageImageListView, '/images')

api.add_resource(PageTextView, '/text')
api.add_resource(PageTextListView, '/texts')
