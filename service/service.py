import praw
import time
import os

def get_reddit_instance():
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')

    if not all([client_id, client_secret, user_agent]):
        raise ValueError("Missing one or more Reddit API credentials in environment variables.")

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def fetch_mentions(search_term):
    reddit = get_reddit_instance()
    posts = []
    comments = []
    mentions_count = 0

    for submission in reddit.subreddit('all').search(search_term, sort='new', time_filter='week', limit=50):
        posts.append({
            'title': submission.title,
            'score': submission.score,
            'url': submission.url,
            'created_utc': submission.created_utc
        })
        mentions_count += 1

        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if search_term.lower() in comment.body.lower():
                comments.append({
                    'body': comment.body,
                    'score': comment.score,
                    'created_utc': comment.created_utc,
                    'link_id': comment.link_id
                })
                mentions_count += 1

    return {
        'mentions_count': mentions_count,
        'posts_count': len(posts),
        'comments_count': len(comments),
        'posts': posts[:5],
        'comments': comments[:5]
    }
