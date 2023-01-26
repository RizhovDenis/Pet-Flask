from flask import Flask
from config import config


def create_app() -> Flask:

    from views.homepage import router as homepage_router
    from views.logout import router as logout_router
    from views.sign_in import router as signin_router
    from views.sign_up import router as signup_router

    app = Flask(__name__)

    app.config['SECRET_KEY'] = config.secret_key
    app.config['UPLOAD_FOLDER'] = config.upload_folder

    homepage_router.install(app)
    logout_router.install(app)
    signin_router.install(app)
    signup_router.install(app)

    return app
