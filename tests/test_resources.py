import unittest
from datetime import datetime

from werkzeug.exceptions import NotFound

from app import app
from db import db
from models.image import Image, PageImage
from models.text import PageText


class TestPageTextViews(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object("tests.TestConfig")
        self.db = db
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.db.create_all()

    def test_get_all_texts_list_view(self):
        """
        Test get method for TextListView
        Should return all created PageText objects
        """
        page = PageText(
            url="http://example.com",
            text="awesome website",
            created_at=datetime.now(),
        )
        page.save_to_db()
        page2 = PageText(
            url="http://other.com",
            text="totally other website",
            created_at=datetime.now(),
        )
        page2.save_to_db()

        response = self.client.get("/texts")
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json, [page.to_json(), page2.to_json()])

    def test_get_specific_text_view(self):
        """
        Test get method for TextView
        Should return response for given url only
        """
        page = PageText(
            url="http://example.com",
            text="awesome website",
            created_at=datetime.now(),
        )
        page.save_to_db()
        page2 = PageText(
            url="http://other.com",
            text="totally other website",
            created_at=datetime.now(),
        )
        page2.save_to_db()

        response = self.client.get("/text", data={"url": "http://other.com"})
        self.assertEqual(response.json, page2.to_json())

    def tearDown(self):
        self.db.drop_all()
        self.ctx.pop()


class TestPageImageViews(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object("tests.TestConfig")
        self.db = db
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.db.create_all()

    def test_get_all_images_list_view(self):
        """
        Test get method for ImageListView
        Should return all created PageImage objects
        """
        page = PageImage(
            url="http://example.com",
            created_at=datetime.now(),
        )
        page.save_to_db()
        page2 = PageImage(
            url="http://other.com",
            created_at=datetime.now(),
        )
        page2.save_to_db()

        response = self.client.get("/images")
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json, [page.to_json(), page2.to_json()])

    def test_get_specific_image_view(self):
        """
        Test get method for ImageView
        Should return response for given url only
        """
        page = PageImage(
            url="http://example.com",
            created_at=datetime.now(),
        )
        page.save_to_db()
        page2 = PageImage(
            url="http://other.com",
            created_at=datetime.now(),
        )
        page2.save_to_db()

        response = self.client.get("/image", data={"url": "http://other.com"})
        self.assertEqual(response.json, page2.to_json())

    def tearDown(self):
        self.db.drop_all()
        self.ctx.pop()


class TestTasks(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object("tests.TestConfig")
        self.db = db
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.db.create_all()

    def tearDown(self):
        self.db.drop_all()
        self.ctx.pop()
