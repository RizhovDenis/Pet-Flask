from flask import flash, render_template, redirect, request, url_for
from flask.views import MethodView

from components.user.models import User


class RegistrationView(MethodView):

    def get(self):
        return render_template("pages/sign_up/index.html")

    def post(self):
        user = User.add_user(
            request.form.get('mail'),
            request.form.get('password'),
            request.form.get('name'),
            request.form.get('surname'),
            request.form.get('birthday')
        )
        if not user:
            flash('This mail have profile', category="error")
            return render_template("pages/sign_up/index.html")

        flash('Account was created', category="success")
        return render_template("pages/sign_up/index.html")
