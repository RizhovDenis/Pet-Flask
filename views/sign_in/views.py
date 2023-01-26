import uuid

from flask import flash, redirect, render_template, request, session, url_for
from flask.views import MethodView

from components.user.models import User, UserSession


class LoginView(MethodView):

    def get(self):
        return render_template("pages/auth/index.html")

    def post(self):
        user = User.auth_read_user(
            request.form.get('mail'),
            request.form.get('password')
        )
        if user:
            session['id'] = uuid.uuid4()
            UserSession.create(session.get('id'), user.id)
            return redirect(url_for('user-page', user_url=user.url))

        flash('Incorrect login or password', category="error")
        return redirect(url_for("login-page"))
