import json
# flask: web framework for rendering website
from flask import Flask, render_template, jsonify

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

# run scrapers, analyze, and store into db
def get_new_articles():
  pass


app = Flask('app')

@app.route('/', methods=['GET'])
def main():
  
  all_articles = get_current_articles()
  
  return render_template('index.html', all_articles=all_articles)

app.run(host='0.0.0.0', port=8080)