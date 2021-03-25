import unittest
from datetime import datetime

from freezegun import freeze_time
from werkzeug.exceptions import NotFound

from app import app
from db import db
from models.image import Image, PageImage
from models.text import PageText


class TestPageTextModel(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object("tests.TestConfig")
        self.db = db
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.db.create_all()

    def test_save_to_db(self):
        """
        Test auxiliary method for saving objects in DB
        """
        page = PageText(
            url="http://example.com",
            text="awesome website",
            created_at=datetime.now(),
        )
        self.assertIsNone(page.id)
        self.assertEqual(PageText.query.all(), [])

        page.save_to_db()

        # Objects receive ID after saving in DB
        self.assertIsNotNone(page.id)
        self.assertEqual(PageText.query.all()[0], page)

    def test_to_json_method(self):
        """
        Test auxiliary method for returing JSON object
        """
        with freeze_time("2021-03-25 14:15:16"):
            page = PageText(
                url="http://example.com",
                text="awesome website",
                created_at=datetime.now(),
            )
        self.db.session.add(page)
        self.db.session.commit()
        expected_response = {
            "id": page.id,
            "url": "http://example.com",
            "text": "awesome website",
            "created_at": "25/03/21 14:15:16",  # expected date format is "%d/%m/%y %H:%M:%S"
        }
        self.assertEqual(page.to_json(), expected_response)

    def test_find_url_or_404(self):
        """
        Test classmethod should return only newer object
        """
        with freeze_time("2021-03-24 14:15:16"):
            page = PageText(
                url="http://example.com",
                text="awesome website",
                created_at=datetime.now(),
            )
        self.db.session.add(page)
        self.db.session.commit()
        with freeze_time("2021-03-25 17:15:16"):
            page2 = PageText(
                url="http://example.com",
                text="newer awesome website",
                created_at=datetime.now(),
            )
        self.db.session.add(page2)
        self.db.session.commit()

        self.assertEqual(PageText.find_url_or_404(url="http://example.com"), page2)

    def test_find_url_or_404_no_object(self):
        """
        Test classmethod should raise NotFound exception if object with given URL does not exist
        """
        with self.assertRaises(NotFound):
            PageText.find_url_or_404(url="http://example.com")

    def tearDown(self):
        self.db.drop_all()
        self.ctx.pop()


class TestPageImageModel(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object("tests.TestConfig")
        self.db = db
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.db.create_all()

    def test_save_to_db(self):
        """
        Test auxiliary method for saving objects in DB
        """
        page = PageImage(
            url="http://example.com",
            created_at=datetime.now(),
        )
        self.assertIsNone(page.id)
        self.assertEqual(PageImage.query.all(), [])

        page.save_to_db()

        # Objects receive ID after saving in DB
        self.assertIsNotNone(page.id)
        self.assertEqual(PageImage.query.all()[0], page)

    def test_to_json_method(self):
        """
        Test auxiliary method for returing JSON object
        """
        with freeze_time("2021-03-25 14:15:16"):
            page = PageImage(
                url="http://example.com",
                created_at=datetime.now(),
            )
        self.db.session.add(page)
        self.db.session.commit()
        img1 = Image(
            img_url="http://example.com/img_1.png", page_id=page.id, data=b"123"
        )
        self.db.session.add(img1)
        self.db.session.commit()
        expected_response = {
            "id": page.id,
            "url": "http://example.com",
            "images": ["<Image url: http://example.com/img_1.png>"],
            "created_at": "25/03/21 14:15:16",  # expected date format is "%d/%m/%y %H:%M:%S"
        }
        self.assertEqual(page.to_json(), expected_response)

    def test_find_url_or_404(self):
        """
        Test classmethod should return only newer object
        """
        with freeze_time("2021-03-24 14:15:16"):
            page = PageImage(
                url="http://example.com",
                created_at=datetime.now(),
            )
        self.db.session.add(page)
        self.db.session.commit()
        with freeze_time("2021-03-25 17:15:16"):
            page2 = PageImage(
                url="http://example.com",
                created_at=datetime.now(),
            )
        self.db.session.add(page2)
        self.db.session.commit()

        self.assertEqual(PageImage.find_url_or_404(url="http://example.com"), page2)

    def test_find_url_or_404_no_object(self):
        """
        Test classmethod should raise NotFound exception if object with given URL does not exist
        """
        with self.assertRaises(NotFound):
            PageImage.find_url_or_404(url="http://example.com")

    def tearDown(self):
        self.db.drop_all()
        self.ctx.pop()
