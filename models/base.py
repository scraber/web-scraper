import datetime
from typing import Dict

from db import db


class BasePage(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __str__(self):
        return f"url: {self.url}"

    @classmethod
    def find_url_or_404(cls, url: str):
        """
        Method looks up for objects with given url
        In case of multiple matches, returns the newest one
        Raises 404 error if it doesn't exist

        Args:
            url (str): URL to look for

        Returns:
            BasePage: found object if exists
        """

        return (
            cls.query.filter_by(url=url)
            .order_by(db.desc(cls.created_at))
            .first_or_404()
        )

    def save_to_db(self):
        """
        Auxiliary method for adding object to DB
        """
        db.session.add(self)
        db.session.commit()

    def to_json(self) -> Dict:
        """
        Return JSON of object data

        Returns:
            Dict: of pairs Column-Value for object
        """
        return {
            "id": self.id,
            "url": self.url,
            "created_at": datetime.datetime.strftime(
                self.created_at, "%d/%m/%y %H:%M:%S"
            ),
        }
