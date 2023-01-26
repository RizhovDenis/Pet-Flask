import os
import uuid

from flask import request, redirect, render_template, session

from config import config
from components.user.models import User, UserSession


def login_required(func):

    def inner(*args, **kwargs):
        if not session.get('id'):
            return render_template('pages/error/index.html')
        return func(*args, **kwargs)

    return inner


def upload_avatar(func):

    def inner(*args, **kwargs):
        image = request.files.get('avatar')
        if image:
            user = UserSession.get_user(session['id'])

            image_name = f"{str(uuid.uuid4())}.{image.filename.split('.')[-1]}"
            image.save(os.path.join(config.upload_folder, image_name))
            User.update_avatar(user.id, image_name)
            return redirect(request.url)
        return func(*args, **kwargs)

    return inner
