import pandas as pd 
import os 
import tweepy as tw
import yfinance as yf
import sys
import secrets

print('please work')

def yahoo_history_scraper(ticker, period, start, end): 
    '''
    Creates a pandas dataframe for specified stock from start to end by specified period and makes a csv 

    Parameters: 
        ticker (str) : stock ticker from yahoo
        period (str) : '1d', '1h', etc.
        start (str) : 'YYYY-MM-DD'
        end (str) : 'YYYY-MM-DD'
    
    Returns: 
        DataFrame and csv with features Open High Low Close Volume Dividends Stock Splits
    '''
    ticker_symbol = ticker 

    tickerData = yf.Ticker(ticker_symbol)

    tickerDf = tickerData.history(period = period, start = start, end = end)

    tickerDf.to_csv('finance.csv')
    return tickerDf


doge = yahoo_history_scraper('DOGE-USD', '1d', '2020-10-01', '2021-04-10')

# Going to make a class eventually for this with auth method 


def twitter_fetch(hashtag, date, max_tweets): 
    '''
    Creates a txt file of tweets from search query 

    Parameters:
        hashtag (str): what would be typed into twitter -> explore -> search
        date (str): 'YYYY-MM-DD' start date
        max_tweets (int): max amount of tweets scraped

    Returns: 
        txt file of raw tweets
    '''
    consumer_key = secrets.API_Key
    consumer_secret_key = secrets.API_Secret_Key
    access_token = secrets.Access_Token
    access_token_secret = secrets.Access_Token_Secret

    auth = tw.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    search_words = str(hashtag)
    date_since = date
    retweet_filter = '-filter:retweets'
    tweets_per_query = 100 
    fName = 'raw_tweets.txt'
    max_tweets = max_tweets
    id = -1
    tweetCount = 0

    print('Downloading maximum of {0} tweets'.format(max_tweets))

    with open(fName, 'w') as f: 
        while tweetCount < max_tweets: 
            tweets = []
            try: 
                if (id <= 0):  
                        new_tweets = api.search( q = search_words+retweet_filter, count = tweets_per_query, lang = 'en', since=date_since, tweet_mode = 'extended')
                        tweets.append(new_tweets)
                else: 
                    continue

                if not new_tweets: 
                    print("Cannot get tweets")
                    break
                for tweet in new_tweets: 
                    f.write(str(tweet.full_text.replace('\n', '').encode('utf-8')) + '\n')

                tweetCount += len(new_tweets)
                print('Finished downloading {0} tweets'.format(tweetCount))

            except tw.TweepError as e:
                print('error :' + str(e))
                break

    print('Downlaoded {0} tweets, saved to {1}'.format(tweetCount, fName))

twitter_fetch('dogecoin', '2021-04-12', 200)

def persons_tweets(screen_name, oldest): 
    '''
    Creates a txt of a users tweets

    Parameters:  
        username (str): must be exact username of the tweeter
        tweets (int): how many tweets to be taken
    Returns: 
        txt of raw tweets
    '''
    consumer_key = secrets.API_Key
    consumer_secret_key = secrets.API_Secret_Key
    access_token = secrets.Access_Token
    access_token_secret = secrets.Access_Token_Secret

    auth = tw.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    alltweets = []
    
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
  
    oldest = str(oldest)
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        alltweets.extend(new_tweets)
        
        print(f"...{len(alltweets)} tweets downloaded so far")
    
    #transform the tweepy tweets into a 2D array that will populate the txt 
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    #write the csv  
    with open(f'new_{screen_name}_tweets.txt', 'w') as f:
        writer = f.write(str(outtweets))
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass


persons_tweets('elonmusk', '2021-03-31')
