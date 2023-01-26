from views.sign_in import views


def install(app):
    app.add_url_rule(
        '/login',
        view_func=views.LoginView.as_view('login-page')
    )
