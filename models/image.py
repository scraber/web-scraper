from db import db


class PageImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, primary_key=True)
    image = db.Column(db.LargeBinary)