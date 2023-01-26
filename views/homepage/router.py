from . import views


def install(app):
    app.add_url_rule('/',
                     view_func=views.HelloPageView.as_view('hello-page'))
    app.add_url_rule(
        '/<user_url>/',
        view_func=views.IndexView.as_view('user-page')
    )
    app.add_url_rule(
        '/post',
        view_func=views.PostView.as_view('post-page')
    )
    app.add_url_rule(
        '/feed/<int:page>/',
        view_func=views.FeedView.as_view('feed-page')
    )
    app.add_url_rule(
        '/following/',
        view_func=views.FollowingView.as_view('following-page')
    )
    app.add_url_rule(
        '/followers/',
        view_func=views.FolowersView.as_view('followers-page')
    )
