import uuid

from datetime import datetime
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, Integer, TIMESTAMP, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database import Base, bd_session


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, nullable=False,
                     unique=True, autoincrement=True)
    mail: str = Column(String, nullable=False, unique=True)
    url: UUID = Column(UUID(as_uuid=True), nullable=False,
                       unique=True, default=uuid.uuid4)
    avatar: str = Column(String, unique=True)
    password: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)
    surname: str = Column(String, nullable=False)
    birthday: TIMESTAMP = Column(
        TIMESTAMP, nullable=False)
    created_at: TIMESTAMP = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __str__(self):
        return f"{self.name} {self.surname}"

    @classmethod
    def by_id(self, id: int):  # return User
        return bd_session.query(User).filter(User.id == id).first()

    @classmethod
    def by_url(self, url: uuid.uuid4):
        params = {'url': url}
        return bd_session.execute(
            """SELECT * FROM users 
                WHERE url = :url""",
            params=params
        ).fetchone()

    @classmethod
    def add_user(
            self,
            mail: str,
            password: str,
            name: str,
            surname: str,
            birthday: TIMESTAMP
    ) -> bool:

        if bd_session.query(User).where(User.mail == mail).first():
            return False

        user = User(mail=mail, password=generate_password_hash(password),
                    name=name, surname=surname, birthday=birthday)
        bd_session.add(user)
        bd_session.commit()
        return True

    @classmethod
    def read_user(self, mail: str):
        params = {'mail': mail}
        return bd_session.execute(
            """SELECT * FROM users
                WHERE mail = :mail limit 1""",
            params=params
        ).fetchone()

    @classmethod
    def auth_read_user(self, mail: str, password: str):
        user = self.read_user(mail)
        if not user:
            return None

        if check_password_hash(user.password, password):
            print(user)
            return user
        return None

    @classmethod
    def update_avatar(self, user_id: int, image_name: str):
        params = {
            'avatar': image_name,
            'user_id': user_id
        }
        bd_session.execute(
            """UPDATE users
                SET avatar = :avatar
                WHERE id = :user_id
                RETURNING * """,
            params=params
        )
        bd_session.commit()


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: int = Column(Integer, primary_key=True, nullable=False,
                     unique=True, autoincrement=True)
    session_id: UUID = Column(UUID(as_uuid=True), nullable=False,
                              unique=True, default=uuid.uuid4)
    user_id: int = Column(Integer, ForeignKey("users.id"))

    @classmethod
    def create(self, session_id: int, user_id: int):
        user_session = UserSession(
            session_id=session_id,
            user_id=user_id
        )
        bd_session.add(user_session)
        bd_session.commit()

    @classmethod
    def get_user(self, session_id: int):
        params = {'session_id': session_id}
        return bd_session.execute(
            """SELECT u.* FROM user_sessions us JOIN users u
                    on us.user_id=u.id
                WHERE us.session_id= :session_id""",
            params=params
        ).fetchone()


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'subscription_id'),
    )

    user_id: int = Column(Integer, ForeignKey("users.id"))
    subscription_id: int = Column(Integer, ForeignKey("users.id"))
    created_at: TIMESTAMP = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow)
    user = relationship('User', foreign_keys=[user_id])
    subscription = relationship('User', foreign_keys=[subscription_id])

    @classmethod
    def create_subscription(self, user_id: int, subscription_id: int):
        subscription = Subscription(
            user_id=user_id, subscription_id=subscription_id)
        bd_session.add(subscription)
        bd_session.commit()

    @classmethod
    def check_subscription(self, user_id: int, subscription_id: int):
        params = {
            'user_id': user_id,
            'subscription_id': subscription_id
        }
        return bd_session.execute(
            """SELECT * FROM subscriptions
                WHERE user_id = :user_id 
                and subscription_id = :subscription_id""",
            params=params
        ).fetchone()

    @classmethod
    def delete_subscription(self, user_id: int, subscription_id: int):
        params = {
            'user_id': user_id,
            'subscription_id': subscription_id
        }
        bd_session.execute(
            """DELETE FROM subscriptions
                WHERE user_id = :user_id
                and subscription_id = :subscription_id
                RETURNING * """,
            params=params
        ).fetchall()
        bd_session.commit()

    @classmethod
    def show_subscriptions(self, user_id: int) -> List:
        params = {'user_id': user_id}
        return bd_session.execute(
            """SELECT * FROM users u join subscriptions sub
                    on u.id=sub.subscription_id and sub.user_id= :user_id
                ORDER BY sub.created_at DESC""",
            params=params
        ).fetchall()

    @classmethod
    def show_subscribers(self, user_id: int) -> List:
        params = {'user_id': user_id}
        return bd_session.execute(
            """SELECT * FROM users u join subscriptions sub
                    on u.id=sub.user_id and sub.subscription_id= :user_id
                ORDER BY sub.created_at DESC """,
            params=params
        ).fetchall()
