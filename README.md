# Bot, Don King
Bot, Don King is an automatic Reddit promoter that posts to the specified sub-reddits at the sub-reddits' optimal time.

Just specify the URLs, the titles, and all the subreddits you'd like to post in. Bot, Don King will then retrieve the peak hours for all of those subreddits (day and hour) and queue up your posts. When the peak time for a particular subreddit comes around, Bot, Don King will post for you. [This](https://tmthyjames.github.io/projects/Meet-Bot,-Don-King/) blog post explains how it was built. The following example shows how your data should be structured.

```python
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
```
