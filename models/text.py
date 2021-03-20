from db import db


class PageText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, primary_key=True)
    text = db.Column(db.String)