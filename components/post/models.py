from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base, bd_session
from components.user.models import User


class Post(Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, nullable=False,
                     unique=True, autoincrement=True)
    status: str = Column(String, nullable=False, default="public")
    title: str = Column(String, nullable=False)
    created_at: TIMESTAMP = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow)
    post = Column(String, nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    user = relationship('User')

    @classmethod
    def write_post(self, user_id: int, post_message: str, post_status: str, post_title: str):
        post = Post(user_id=user_id, status=post_status,
                    title=post_title, post=post_message)
        bd_session.add(post)
        bd_session.commit()

    @classmethod
    def all_user_posts(self, user_id: int) -> List:
        params = {'user_id': user_id}
        return bd_session.execute(
            """SELECT * FROM users join posts
                    on users.id=posts.user_id and users.id = :user_id 
                ORDER BY posts.created_at DESC""",
            params=params
        ).fetchall()

    @classmethod
    def public_user_posts(self, user_id: int) -> List:
        params = {'user_id': user_id}
        return bd_session.execute(
            """SELECT * FROM users join posts
                    on users.id=posts.user_id and users.id = :user_id 
                        and status = 'public'
                ORDER BY posts.created_at DESC""",
            params=params
        ).fetchall()

    @classmethod
    def show_feed(self, user_id: int, page: int, pagination_number: int, text: str) -> List:
        # Split on subscribers, anon and other users and order by all
        if text:
            text = f'%{text}%'
        params = {
            'user_id': user_id,
            'page': page,
            'pagination': pagination_number,
            'text': text
        }
        return bd_session.execute(
            """WITH user_posts as (
                SELECT *, u.created_at as u_c_at, p.created_at as p_c_at
                    FROM users u join posts p
                    on u.id=p.user_id and u.id <> :user_id
                WHERE 
                    CASE WHEN :text IS NOT NULL 
                        THEN LOWER(p.post) LIKE LOWER(:text)
                            or LOWER(p.title) LIKE LOWER(:text)
                        ELSE True
                    END
                )
            SELECT * FROM (
                SELECT *, ROW_NUMBER() OVER(ORDER BY NULL) as num FROM (
                    (SELECT up.* FROM user_posts up join subscriptions s
                        on up.user_id=s.subscription_id and
                            s.user_id= :user_id and 
                            up.status= 'public' 
                    ORDER BY p_c_at DESC)
                    UNION ALL
                    (SELECT * FROM user_posts up
                    WHERE status = 'anon'
                        or user_id not in
                        (SELECT subscription_id FROM subscriptions
                            WHERE user_id = :user_id)    
                    ORDER BY p_c_at DESC)
                ) as union_table
            ) as row_number

            WHERE num BETWEEN ((:page - 1) * :pagination) + 1 
                and :page * :pagination
            """,
            params=params
        ).fetchall()

    @classmethod
    def number_user_posts(self, user_id: int) -> int:
        params = {'user_id': user_id}
        return bd_session.execute(
            """SELECT COUNT(*) FROM posts
                WHERE user_id= :user_id""",
            params=params
        ).fetchone()[0]

    @classmethod
    def number_feed(self, user_id: int, text: str) -> int:
        if text:
            text = f'%{text}%'
        params = {
            'user_id': user_id,
            'text': text
        }
        return bd_session.execute(
            """SELECT COUNT(*) FROM posts p
                WHERE user_id <> :user_id
                    and CASE WHEN :text IS NOT NULL
                            THEN LOWER(p.post) LIKE LOWER(:text)
                                or LOWER(p.title) LIKE LOWER(:text)
                            ELSE True
                        END""",
            params=params
        ).fetchone()[0]
