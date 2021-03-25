from io import BytesIO
from typing import Dict, List

from flask import send_file
from flask_restful import Resource, reqparse

from app import celery
from models.image import PageImage
from models.text import PageText
from tools.utils import archive_bytes_stream


class PageTextTask(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", type=str, required=True, help="URL required!")

    def post(self) -> Dict:
        """
        Sends task for scraping text for url given in request body

        Returns:
            Dict: Celery task ID
        """
        data = PageTextTask.parser.parse_args()
        task = celery.send_task("celery_scrape_text", args=[data["url"]])

        return {"task_id": task.id}


class PageImageTask(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", type=str, required=True, help="URL required!")

    def post(self) -> Dict:
        """
        Sends task for scraping images for url given in request body

        Returns:
            Dict: Celery task ID
        """
        data = PageImageTask.parser.parse_args()
        task = celery.send_task("celery_scrape_images", args=[data["url"]])

        return {"task_id": task.id}


class PageTaskStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("task_id", type=str, required=True, help="Task ID is required!")

    def get(self) -> Dict:
        """
        Get status for celery task

        Returns:
            Dict: Status of celery task
        """
        data = PageTaskStatus.parser.parse_args()
        res = celery.AsyncResult(data["task_id"])
        return {"status": res.state}


class PageTextView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", type=str, required=True, help="URL required!")

    def get(self):
        """
        Get PageText for already scrapped page.

        Returns:
            [type]: [description]
        """
        data = PageTextView.parser.parse_args()
        return PageText.find_url_or_404(data["url"]).to_json()


class PageTextListView(Resource):
    def get(self):
        """
        List all pages which were scrapped for text

        Returns:
            List: of dicts of scrapped pages
        """
        return [entry.to_json() for entry in PageText.query.all()]


class PageImageView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", type=str, required=True, help="URL required!")

    def get(self):
        """
        Get PageImage for already scrapped page.

        Returns:
            [type]: [description]
        """
        data = PageImageView.parser.parse_args()
        return PageImage.find_url_or_404(data["url"]).to_json()


class PageImageArchive(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", type=str, required=True, help="URL required!")

    def get(self):
        """
        Get all images for already scrapped url as zip .

        Returns:
            [type]: [description]
        """
        data = PageImageView.parser.parse_args()
        page = PageImage.find_url_or_404(data["url"])

        images_data = [img.data for img in page.images]

        if images_data:
            zf = archive_bytes_stream(images_data)

            return send_file(
                BytesIO(zf),
                attachment_filename=f"{page.url}_images.zip",
                as_attachment=True,
            )


class PageImageListView(Resource):
    def get(self) -> List:
        """
        List all pages which were scrapped for images

        Returns:
            List: of dicts of scrapped pages
        """
        return [entry.to_json() for entry in PageImage.query.all()]
