from flask import redirect, url_for, session
from flask.views import MethodView


class LogoutView(MethodView):

    def get(self):
        session.pop("id", None)
        return redirect(url_for('login-page'))

    def post(self):
        pass
