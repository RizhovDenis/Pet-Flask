from flask_admin.contrib.sqla import ModelView

from components.post.models import Post


class PostsView(ModelView):
    column_list = (
        'user',
        'title',
        'post',
        'status',
        'created_at'
    )

    form_columns = (
        'user',
        'status',
        'title',
        'post'
    )

    column_formatters = dict(
        created_at=lambda view,
        context, model, name: model.created_at.strftime("%H:%M %d.%m.%Y")
    )

    column_default_sort = ('status', True)  # name column, descending

    create_modal = True
    edit_modal = True


def load_views(admin, bd_session):
    admin.add_view(PostsView(Post, bd_session, name='Посты'))
