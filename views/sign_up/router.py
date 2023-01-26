from views.sign_up import views


def install(app):
    app.add_url_rule(
        '/registration',
        view_func=views.RegistrationView.as_view("registration-page")
    )
