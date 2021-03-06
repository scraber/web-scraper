import os

basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")
