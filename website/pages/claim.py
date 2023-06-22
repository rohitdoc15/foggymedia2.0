import snscrape.modules.twitter as sntwitter

#specify the number of tweets you want 
maxTweets = 15000

# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list

#set the first parameter to "Raymond" since you want tweets related to raymond 
# set lang:en to retrieve tweets in english
#set the date parameter using since and until

for i,tweet in enumerate(sntwitter.TwitterSearchScraper(' Raymond lang:en since:2023-01-31 until:2023-02-14').get_items()):
    if i>maxTweets:
        break
    tweets_list2.append([tweet.date, tweet.content])
    print(tweet.content)

