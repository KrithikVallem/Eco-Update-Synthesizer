"""
  Not all the functions in this file are used. They have just been left there in case they might be needed in the future or to revert back to later.
"""

import json, time

# import custom code we wrote
from . import website_scraping, article_scraping, article_class, analysis

# replit's database stuff
from replit import db



# run the scrapers and analyze the newly scraped articles
# return a list of article objects encoded as JSON
def get_new_articles():
    # scrape all websites, and return a small subset of the scraped articles from all the websites
    # filtering is automatically done on the websites that require filtering
    # articles_dict is a dict of { "headline": "url" }
    articles_dict = website_scraping.run_website_scrapers()

    # scrape every article for its html
    # scraped_articles_list is a list of tuples of (headline,url,html)
    scraped_articles_list = article_scraping.scrape_articles(articles_dict)
    
    new_articles = []
    for headline,url,html in scraped_articles_list:
        # make an article class
        article = article_class.Article(headline,url,html)

        # extract text, image_url,etc... from article.html
        article.extract_article_details()

        # skip Article if its content is irrelevant to ecological matters
        #if not analysis.is_content_relevant(article.text):
        #   continue

        # get all place names and coordinates mentioned in article.text
        # this involves an api call to get coordinates
        article.extract_locations()

        # get summary, sentiment, article's keywords, etc...
        article.analyze()

        # add article object to accumulator list
        new_articles.append(article)
    
    # return a list of the articles, stored as JSON
    return json.dumps(new_articles, default=lambda a: a.encode() )


# in case theres an error with the current articles, 
# use these default articles instead as a placeholder
def get_default_articles():
  default_articles = []
  with open("default_articles.json") as file:
    default_articles = json.load(file)
  return default_articles


def get_current_articles():
  # if the db['articles'] property is not set for some reason
  if 'articles' not in db.keys():
    refresh_db()

  # I seem to have accidently double-json-encoded the articles at some point
  # if this project is ever touched again in the future, this should probably be fixed
  current_articles = json.loads(
    json.loads(
      db['articles'] 
    )
  )

  # get_current_articles fetches articles stored in db
  # if, for some reason, there is an error doing so, then
  # the default articles (scraped previously, never changing)
  # are used instead
  current_articles = current_articles or get_default_articles()
  return current_articles



def refresh_db():
  try:
    new_articles = get_new_articles()
    db['articles'] = json.dumps(new_articles)
  except:
    # do nothing, just keep using the current
    # articles or the default articles
    pass


def refresh_func():   
  current_timestamp = int( time.time() )
  seconds_per_day = 60*60*24

  if 'most_recent_refresh_timestamp' not in db:
    db['most_recent_refresh_timestamp'] = 0

  # check to make sure that it has been 24 hours since the last refresh
  if (
    current_timestamp
    - int( db['most_recent_refresh_timestamp'] )
    > seconds_per_day
  ):
    db['most_recent_refresh_timestamp'] = current_timestamp

    # this does the actual refreshing
    refresh_db()

    # restart app
    #app.run(host='0.0.0.0', port=8080)

    return f"Successfully refreshed database at {current_timestamp}!"
  else:
    return f"It has been less than 24 hours since the most recent database refresh at {db['most_recent_refresh_timestamp']}! Please try again later!"

def sanity_check():
  print(time.ctime())