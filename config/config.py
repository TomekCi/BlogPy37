class Config(object):
    DEBUG = True
    SECRET_KEY = "itissecret"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    POSTGRES = {
        'user': 'postgres',
        'pw': 'dupa1',
        'db': 'flasklogin',
        'host': 'localhost',
        'port': '5432',
    }

    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES