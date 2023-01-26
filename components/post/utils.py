import csv

from typing import List


def write_csv(posts: List):
    fieldnames = [
        'post_title', 
        'post_message', 
        'post_status', 
        'created_at'
        ]
    user_label = posts[0].mail.split('@')[0]
    
    with open(f'records/{user_label}.csv', 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for post in posts:
            record = {
                'post_title': post.title, 
                'post_message': post.post, 
                'post_status': post.status, 
                'created_at': post.created_at
            }
            writer.writerow(record)
