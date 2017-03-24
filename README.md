# Bot, Don King
Bot, Don King is an automatic Reddit promoter that posts to the specified sub-reddits at the sub-reddits' optimal time.

    urls_subreddits = {
        'http://www.learndatasci.com/': {
            'title': 'this is a test',
            'subreddits': ['pystats', 'datascience', 'statistics'],
        },
        'http://www.learndatasci.com/#test=true': {
            'title': 'this is still a test',
            'subreddits': ['python'],
        }
    }

    dk = DonKing(urls_subreddits)
    dk.queue_articles()
    dk.promote()

