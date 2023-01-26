from setup_admin import creat_admin
from config import config


if __name__ == "__main__":
    app = creat_admin()
    app.run(debug=True, port=config.admin_port)
