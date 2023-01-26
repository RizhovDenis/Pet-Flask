from werkzeug.security import generate_password_hash

from flask_admin.contrib.sqla import ModelView
from sqlalchemy import event

from components.user.models import User, Subscription


@event.listens_for(User.password, 'set', retval=True)
def hash_password(target, value, oldvalue, initiator):
    return generate_password_hash(value)


class UserView(ModelView):
    column_list = (
        "mail",
        "name",
        "surname",
        "birthday",
        "created_at"
    )

    column_formatters = dict(
        birthday=lambda view,
        context, model, name: model.birthday.strftime("%d.%m.%Y"),
        created_at=lambda view,
        context, model, name: model.birthday.strftime("%H:%M %d.%m.%Y")
    )

    create_modal = True
    edit_modal = True


class SubscribeView(ModelView):
    column_list = (
        'user',
        'subscription'
    )

    create_modal = True
    edit_modal = True


def load_views(admin, bd_session):
    admin.add_view(UserView(User, bd_session,
                   name='Личные данные', category='Пользователи'))
    admin.add_view(SubscribeView(Subscription, bd_session,
                   name='Подписки', category='Пользователи'))
