from db import db
from models.base import BasePage


class PageImage(BasePage):
    __tablename__ = "pageimage"

    images = db.relationship("Image", cascade="all, delete")

    def to_json(self):
        res = super().to_json()
        res.update({"images": [img.__repr__() for img in self.images]})
        return res


class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String)
    page_id = db.Column(db.Integer, db.ForeignKey("pageimage.id"))
    data = db.Column(db.LargeBinary)

    def __repr__(self) -> str:
        return f"<Image url: {self.img_url}>"

    def save_to_db(self):
        """
        Auxiliary method for adding object to DB
        """
        db.session.add(self)
        db.session.commit()
