import json
import time
import requests
import schedule
import praw

reddit = praw.Reddit(client_id='client_id', 
                     client_secret="secret_key", 
                     user_agent='user_agent', 
                     username='username',
                     password='password')

class DonKing(object):
    def __init__(self, urls):
        self.urls = urls
        self.times = {}
        self.days = [
            'Monday','Tuesday','Wednesday','Thursday',
            'Friday','Saturday','Sunday'
        ]
        
    def check_time(self, day, hour):
        hour_counter = 1
        day_counter = day
        day_hour = (day, hour)
        if day_hour not in self.times:
            self.times[day_hour] = day_hour
            return day_hour
        else:
            next_hour = hour + hour_counter
            if next_hour == 24:
                next_hour = hour_counter = 0
                day_counter = day_counter + 1 if day_counter < 6 else 0
            check = self.check_time(day_counter, next_hour)
            if check:
                self.times[check] = (day_counter, next_hour)
                return check
            counter += 1

    def get_optimal_time(self, subreddit):
        url = "https://dashboard.laterforreddit.com/graphql"

        payload = {
            u'operationName': u'analysis',
            u'query': u'query analysis($subreddit: String!, $threshold: Int!, $tzid: String, $tzoffset: Int) {\n  subreddit_suggestions(subreddit: $subreddit) {\n    subreddit\n    weight\n    normalized_weight\n    __typename\n  }\n  analysis(subreddit: $subreddit, threshold: $threshold, timezone_id: $tzid, timezone_offset: $tzoffset) {\n    overall\n    daily {\n      count\n      labels\n      datasets {\n        data\n        __typename\n      }\n      __typename\n    }\n    hourly {\n      count\n      labels\n      datasets {\n        data\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
            u'variables': {
                u'subreddit': u'/'+subreddit+'',
                u'threshold': 5,
                u'tzid': u'America/Chicago',
                u'tzoffset': 300
            }
        }

        headers = {
            'host': "dashboard.laterforreddit.com",
            'connection': "keep-alive",
            'content-length': "736",
            'accept': "*/*",
            'origin': "https://dashboard.laterforreddit.com",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            'content-type': "application/json",
            'referer': "https://dashboard.laterforreddit.com/analysis/?subreddit=%2F"+subreddit+"&threshold=5",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.8,it;q=0.6",
            'cookie': "_gat=1; _ga=GA1.2.1595759139.1489776882",
            'cache-control': "no-cache",
            'postman-token': "549dce9a-bdec-7546-0fcb-7101d0d23b3c"
            }

        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

        json_resp = response.json()

        analysis = json_resp['data']['analysis']
        daily = analysis['daily']
        daily_labels = daily['labels']
        daily_data = daily['datasets'][0]['data']
        hourly = analysis['hourly']
        hourly_labels = hourly['labels']
        hourly_data = hourly['datasets'][0]['data']

        daily_count = dict(zip(daily_labels, daily_data))
        hourly_count = dict(zip(hourly_labels, hourly_data))

        optimal_day = max(daily_count, key=lambda k: daily_count[k])
        optimal_hour = max(hourly_count, key=lambda k: hourly_count[k])
        
        optimal_day, optimal_hour = self.check_time(
            self.days.index(optimal_day), int(optimal_hour)
        )
        optimal_day = self.days[optimal_day]
        print optimal_day, optimal_hour
        return optimal_day, optimal_hour

    def queue_articles(self, hours_before=0, hours_after=0):
        for url,v in self.urls.iteritems():
            for subreddit in v['subreddits']:
                optimal_day, optimal_hour = self.get_optimal_time(subreddit)
                optimal_hour_adjusted = str(optimal_hour + hours_before + hours_after) + ':00'
                getattr(
                    schedule.every(), 
                    optimal_day.lower()
                )\
                .at(optimal_hour_adjusted)\
                .do(job, subreddit=subreddit,
                    title=v['title'], url=url)\
                .tag(url, subreddit)
        return None
    
    def event(self, subreddit, title, url):
#         subreddit_request = reddit.subreddit(subreddit)
#         subreddit_request.submit(title, url)
        print subreddit, title, url
        schedule.CancelJob
        return None
    
    def promote(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
