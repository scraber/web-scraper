from db import db
from models.base import BasePage


class PageText(BasePage):
    __tablename__ = "pagetext"
    text = db.Column(db.String)

    def to_json(self):
        """
        Override adds object text to response dict
        """
        res = super().to_json()
        res.update({"text": self.text})
        return res
