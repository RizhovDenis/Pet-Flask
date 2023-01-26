from views.logout import views


def install(app):
    app.add_url_rule(
        '/logout',
        view_func=views.LogoutView.as_view('logout-page')
    )
