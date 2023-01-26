from celery import Celery

from config import config


app = Celery('humanity',
             broker=config.redis_url,
             backend=config.redis_url,
             include=[
                 'components.post.tasks'
             ])


if __name__ == '__main__':
    app.start()
