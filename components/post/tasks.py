from run_celery import app
from components.post.utils import write_csv
from components.post.models import Post


@app.task
def create_record(user_id: int):
    posts = Post.all_user_posts(user_id)

    write_csv(posts)


@app.task
def add_post(
    user_id: int, 
    post_title: str, 
    post_message: str, 
    post_status: str
    ):

    Post.write_post(
        user_id,
        post_message,
        post_status,
        post_title
    )

    create_record.delay(
        user_id=user_id
    )
