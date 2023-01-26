from flask import render_template, redirect, request, session, url_for
from flask.views import MethodView

from components.post import tasks
from components.post.models import Post
from components.user.models import User, UserSession, Subscription
from config import config

from utils.decorators import login_required, upload_avatar
from utils.pagination import posts_meta


class HelloPageView(MethodView):

    @login_required
    def get(self):
        user = UserSession.get_user(session.get('id'))
        return redirect(url_for('user-page', user_url=user.url))

    def post(self):
        pass


class IndexView(MethodView):
    """
    Work with homepage and 
        with pages other users
        """

    @login_required
    def get(self, user_url):
        # Show my page
        user = UserSession.get_user(session.get('id'))
        if user_url == str(user.url):
            posts_info = Post.all_user_posts(user.id)

            return render_template(
                "pages/homepage/mypage/index.html",
                user=user,
                posts=posts_info,
                userpage=False
            )

        # Show page another user
        another_page = User.by_url(user_url)
        posts_info = Post.public_user_posts(another_page.id)
        subscribe_status = Subscription.check_subscription(
            user.id,
            another_page.id
        )

        return render_template(
            "pages/homepage/mypage/index.html",
            another_user=another_page,
            user=user,
            posts=posts_info,
            userpage=True,
            subscribe=subscribe_status
        )

    @login_required
    @upload_avatar
    def post(self, user_url):
        form_status = request.form.get('subscription')
        user = UserSession.get_user(session.get('id'))
        subscribe_id = User.by_url(user_url).id

        if form_status == 'Subscribe':
            Subscription.create_subscription(
                user.id,
                subscribe_id
            )
            return redirect(url_for('following-page'))

        if form_status == 'Unsubscribe':
            Subscription.delete_subscription(
                user.id,
                subscribe_id
            )
            return redirect(url_for('following-page'))
        return redirect(url_for('user-page', user_url=user.url))


class PostView(MethodView):

    @login_required
    def get(self):
        user = UserSession.get_user(session.get('id'))

        return render_template(
            'pages/homepage/write_post/index.html',
            user=user
        )

    @login_required
    @upload_avatar
    def post(self):
        user = UserSession.get_user(session.get('id'))

        tasks.add_post.delay(
            user_id=user.id,
            post_title=request.form.get('post_title'),
            post_message=request.form.get('post_message'),
            post_status=request.form.get('post_status')
        )

        return redirect(url_for('post-page'))


class FeedView(MethodView):

    @login_required
    def get(self, page=1):
        text = request.args.get('text')
        user = UserSession.get_user(session.get('id'))
        number_posts = Post.number_feed(user.id, text)
        posts_info = Post.show_feed(
            user.id,
            page,
            config.pagination_number,
            text
        )
        pagination_meta = posts_meta(number_posts, page)

        return render_template(
            "pages/homepage/feed/index.html",
            title="Feed",
            user=user,
            posts=posts_info,
            pagination_meta=pagination_meta,
            text=text
        )

    @login_required
    @upload_avatar
    def post(self, page=1):
        text = request.form.get('text-matches')

        return redirect(f"{url_for('feed-page', page=1)}?text={text}")


class FollowingView(MethodView):

    @login_required
    def get(self):
        user = UserSession.get_user(session.get('id'))
        my_subscriptions = Subscription.show_subscriptions(user.id)

        return render_template(
            'pages/homepage/following/index.html',
            subscriptions=my_subscriptions,
            user=user
        )

    @upload_avatar
    def post(self):
        pass


class FolowersView(MethodView):

    @login_required
    def get(self):
        user = UserSession.get_user(session.get('id'))
        my_subscribers = Subscription.show_subscribers(user.id)

        return render_template(
            'pages/homepage/followers/index.html',
            subscriptions=my_subscribers,
            user=user
        )

    @upload_avatar
    def post(self):
        pass
