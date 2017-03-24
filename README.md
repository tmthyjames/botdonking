# Bot, Don King
Bot, Don King is an automatic Reddit promoter that posts to the specified sub-reddits at the sub-reddits' optimal time.

    urls_subreddits = {
        'http://www.yourblog.com/your-article': { # URL
            'title': 'Check out this article', # title of the article
            'subreddits': ['python', 'rstats'], #subreddit you want to post to
        },
        'http://www.yourblog.com/your-other-article': {
            'title': 'this is still a test',
            'subreddits': ['pystats', 'datascience', 'statistics'],
        }
    }

    dk = DonKing(urls_subreddits)
    dk.queue_articles()
    dk.promote()

