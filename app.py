from flask import Flask
from flask_login import LoginManager
from models import db
from config.config import Config


app = Flask(__name__)
app.config.from_object(Config)


login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
