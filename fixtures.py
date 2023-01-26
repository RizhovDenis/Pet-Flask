from datetime import datetime
from random import choice
from werkzeug.security import generate_password_hash

from database import bd_session
from components.post.models import Post
from components.user.models import User, Subscription


def load_fixtures():
    status = ['anon', 'public']
    for user_id in range(1, 1001):
        bd_session.add(User(
            mail=f"user{user_id}@humanity.com",
            password=generate_password_hash("12345"),
            name=f"Jhon{user_id}",
            surname=f"Smith{user_id}",
            birthday=datetime.now())
        )
    bd_session.commit()

    for user_id in range(1, 1001):
        for post_id in range(1, 11):
            bd_session.add(Post(
                status=choice(status),
                title=f"Post№{user_id}.{post_id}",
                post=f"Some post {user_id}.{post_id}",
                user_id=user_id))
    bd_session.commit()


if __name__ == "__main__":
    start_users = datetime.utcnow()
    print("-----Start generation of users and posts-----")
    load_fixtures()
    print(f"Duration: {datetime.utcnow() - start_users}")
