from flask_restful import Resource, reqparse
from celery.result import AsyncResult

from models.text import PageText
from models.image import PageImage
from app import celery



class PageTextTask(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help="URL required!")

    def post(self):
        data = PageTextTask.parser.parse_args()
        task = celery.send_task('celery_scrape_text', args=[data['url']])

        return {"task_id": task.id}

class PageImageTask(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help="URL required!")

    def post(self):
        data = PageImageTask.parser.parse_args()
        task = celery.send_task('celery_scrape_images', args=[data['url']])

        return {"task_id": task.id}

class PageTaskStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('task_id', type=str, required=True, help="Task ID is required!")

    def get(self):
        data = PageTaskStatus.parser.parse_args()
        res = celery.AsyncResult(data['task_id'])
        return {"status": res.state}

class PageTextView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help="URL required!")

    def get(self):
        data = PageTextView.parser.parse_args()
        return PageText.find_url_or_404(data['url']).to_json()


class PageTextListView(Resource):
    def get(self):
        return [entry.to_json() for entry in PageText.query.all()]

class PageImageView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help="URL required!")

    def get(self):
        data = PageImageView.parser.parse_args()
        return PageImage.find_url(data['url']).to_json()

class PageImageListView(Resource):
    def get(self):
        return [entry.to_json() for entry in PageImage.query.all()]

    
