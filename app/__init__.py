from flask import Flask
from config import Config

from .auth.routes import auth 
from ftlod.routes import ftlod


# import db
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(auth)
app.register_blueprint(ftlod)

app.config.from_object(Config)

db.init_app(app)
login.init_app(app)

login.login_view = "auth.logMeIn"

migrate = Migrate(app, db)

from . import routes
from . import models

