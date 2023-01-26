import os


class Config:
    secret_key = os.urandom(24)
    pagination_number: int = 20
    upload_folder: str = 'static/uploads/'

    db_host: str = os.environ.get('db_host', 'localhost')
    db_port: int = os.environ.get('db_port', 5432)
    db_user: str = os.environ.get('db_user', 'postgres')
    db_password: str = os.environ.get("db_password", 'postgres')
    db_name: str = os.environ.get('db_name', 'humanity')

    app_port: int = os.environ.get('app_port', 9090)
    admin_port: int = os.environ.get('admin_port', 9091)
    redis_port: int = os.environ.get('redis_port', 6379)

    @property
    def db_url(self):
        return f'postgresql://{self.db_user}:{self.db_password}@' \
               f'{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def redis_url(self):
        return f'redis://{self.db_host}:{self.redis_port}/0'


config = Config()
