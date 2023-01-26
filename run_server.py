from app import create_app
from config import config


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=config.app_port)
