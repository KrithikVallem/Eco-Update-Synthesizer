import json
# import custom code we wrote
from utilities import website_scraping, article_scraping, article_class, analysis
# flask: web framework for rendering website
from flask import Flask, render_template, jsonify

# run the scrapers and analyze the newly scraped articles
# return a list of article objects encoded as JSON
def get_new_articles():
    # scrape all websites, and return a small subset of the scraped articles from all the websites
    # articles_dict is a dict of { "headline": "url" }
    articles_dict = website_scraping.run_website_scrapers()

    # remove articles with irrelevant headlines
    # same format as articles_dict, { "headline": "url" }
    filtered_articles_dict = {
        headline : url
        for headline,url in articles_dict.items()
        #if analysis.is_headline_relevant(headline)
    }

    # scrape every article for its html
    # scraped_articles_list is a list of tuples of (headline,url,html)
    scraped_articles_list = article_scraping.scrape_articles(filtered_articles_dict)
    
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
  current_articles = {}

  # get_current_articles fetches articles stored in db
  # if, for some reason, there is an error doing so, then
  # the default articles (scraped previously, never changing)
  # are used instead
  current_articles = current_articles or get_default_articles()
  return current_articles


def refresh_db():
  pass


app = Flask('app')

@app.route('/', methods=['GET'])
def main():
  
  all_articles = get_current_articles()
  
  return render_template('index.html', all_articles=all_articles)

app.run(host='0.0.0.0', port=8080)