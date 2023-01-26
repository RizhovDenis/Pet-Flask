import math
from typing import List

from config import config


def posts_meta(number_posts: int, page: int) -> List:
    if number_posts < config.pagination_number:
        return None

    last_page = math.ceil(number_posts / config.pagination_number)
    return [last_page, page]
