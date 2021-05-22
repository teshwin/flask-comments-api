# process posts
def process_posts(posts, comments):
    processed_posts = list()
    for post in posts:
        processed_post = {f'post_{k}' if k != 'userId' else 'user_id':v for k,v in post.items()}
        processed_post['total_number_of_comments'] = len(list(filter(lambda c: c['postId'] == processed_post['post_id'], comments)))
        processed_posts.append(processed_post)

    return sorted(processed_posts, key=lambda x: x['total_number_of_comments'], reverse=True)

# process comments
def process_comments(comments):
    processed_comments = list()
    for comment in comments:
        processed_comment =  {f'comment_{k}' if k != 'postId' else 'post_id':v for k,v in comment.items()}
        processed_comments.append(processed_comment)
        
    return processed_comments