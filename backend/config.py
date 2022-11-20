# import os

# basedir = os.path.abspath(os.path.dirname(__name__))


# class Config(object):
#     DEBUG = False
#     TESTING = False
#     CSRF_ENABLED = True
#     SECRET_KEY = '69d7ac70ab6671e2e1e3e90fd03ae47001fb05103667f1dbdae03f6059cd74ff'


SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
