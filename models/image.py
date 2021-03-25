from db import db
from models.base import BasePage


class PageImage(BasePage):
    image = db.Column(db.LargeBinary)

    def to_json(self):
        res = super().to_json()
        res.update({"image": self.image})
        return res
