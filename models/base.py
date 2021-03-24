from db import db
import datetime


class BasePage(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __str__(self):
        return f"url: {self.url}"

    @classmethod
    def find_url(cls, url:str):
        return cls.query.filter_by(url=url).first()

    @classmethod
    def find_url_or_404(cls, url:str):
        return cls.query.filter_by(url=url).first_or_404()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {"id": self.id,
                "url": self.url,
                "created_at": datetime.datetime.strftime(self.created_at, "%d/%m/%y %H:%M:%S")}