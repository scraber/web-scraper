from db import db


class BasePage(db.Model):
    __abstract__ = True

    url = db.Column(db.String, primary_key=True)

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
        return {"url": self.url}