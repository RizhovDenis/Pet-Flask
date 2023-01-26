from flask import Flask
from flask_admin import Admin

from database import bd_session
from config import config

from components.user import admin as user_views
from components.post import admin as post_views


def creat_admin():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = config.secret_key

    admin = Admin(app, name="Humanity", template_mode='bootstrap3')

    user_views.load_views(admin, bd_session)
    post_views.load_views(admin, bd_session)

    return app
