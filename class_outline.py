import newspaper, justext # used for extracting article's details from its html
import requests
import re
import string
import numpy as np
import scipy
import gensim
import pprint
from gensim.summarization import summarize
import math 

class Analyzer:
    # store filtering keywords here
    keywords = [
      "polar",
      "green tech",
      "nature",
      "iceberg",
      "biodiversity",
      "biology",
      "plants",
      'abatement',
      'acid rain',
      'air pollution',
      'air quality',
      'algae',
      'algal blooms',
      'alternative energy sources',
      'atmosphere',
      'backyard burning',
      'biodegradable waste',
      'biodiversity',
      'bioenergy',
      'biofuels',
      'biomass',
      'biosphere',
      'carbon',
      'carbon neutrality',
      'cfcs',
      'cfl bulbs',
      'civic amenity site',
      'climate',
      'climate change',
      'compost',
      'compostable',
      'composting',
      'conservation',
      'cryptosporidium',
      'deforestation',
      'development plan',
      'dioxins',
      'disposal',
      'domestic waste',
      'draught proofing',
      'dumping',
      'ecosystem',
      'ecotourism',
      'electric vehicle',
      'emissions',
      'emissions projections',
      'emissions trading allowance',
      'energy efficiency',
      'energy rating',
      'energy star',
      'environmental impact',
      'flora and fauna',
      'fossil fuels',
      'fuel poverty',
      'global warming',
      'green bin',
      'green design',
      'greener homes scheme',
      'greenhouse effect',
      'greenhouse gases',
      'ground water',
      'hazardous waste',
      'home energy saving scheme',
      'household waste',
      'incinerator',
      'insulation',
      'kyoto protocol',
      'kyoto agreement',
      'landfill',
      'mbt',
      'mulch',
      'municipal waste',
      'noise pollution',
      'npws', 
      'epa',
      'noxious gases',
      'oil spill',
      'organic food',
      'organic',
      'organism',
      'ozone layer',
      'paris climate'
      'pesticides',
      'planning permission',
      'plastic bag levy',
      'post-consumer waste',
      'radiation',
      'radioactive',
      'radon',
      'recycle',
      'reforestation',
      'renewable',
      'reuse',
      'river basin',
      'sewage',
      'smog',
      'smokeless fuel',
      'solar panel',
      'surface water',
      'sustainable',
      'toxic waste',
      'toxin',
      'tidy towns',
      'utility',
      'un framework convention on climate change',
      'unesco world heritage site',
      'ventilation',
      'warmer homes scheme',
      'waste management',
      'waste prevention',
      'water vapour',
      'wind energy',
      'wind turbine',
      'wwf',
      'world wildlife foundation',
      'zero emissions'
      ]

    @classmethod
    def is_headline_relevant(cls,headline):
      # Summary: checks if the headline include 2 words from the list of keywords above. Returns True if there are 2 or more keywords. Returns False otherwise. 
      
      # makes headline lowercase -- matches exactly with keywords
      headline = headline.lower()
      count = 0
      
      for word in keywords:
        # looks for one, single word
        # .find() returns -1 if the word is not found 
        if headline.find(word) != -1:
          count = count + 1
      
      if count >= 2:
        return True
      else:
        return False

      pass 

    @staticmethod
    def is_content_relevant(text):
      # Summary: checks if the article text is revelant based number of keywords. Content is relevant and function returns True if there are 10 or more keywords. Returns False otherwise. 

      text = text.lower()
      # removes puncuation from text
      text = re.sub(r'[^\w\s]', '', text) 
  
      count = 0

      for word in keywords:
        count += text.count(word)
  
      if count >= 10:
        return True
      else:
        return False 
      
      pass

    @staticmethod
    def make_summary(text):
      # Summary: takes in article text and returns a 30 word summary 
      
      # from gensim library 
      # split = False  - does NOT split text into indv. sentences 
      summary = summarize(text, word_count= 30, split=False)
      # add "..." to summary 
      summary_final = summary + ".."
      
      return summary_final 
      
      pass

    @staticmethod
    def calculate_sentiment(text): 
        # MACHINE LEARNING
        # use text
        # calculate sentiment
        # return sentiment
        pass

    @staticmethod
    def extract_article_keywords(text):
      # make dictionary of {keyword,frequency}
      keyword_dict = {}
      text = text.lower()
      # gets rid of punctuation
      text = re.sub(r'[^\w\s]', '', text)
      text_list = text.split()

      #making dictionary of keyword to frequency of occurence
      for word in text_list:
        if word in keywords:
          wordfreq = text_list.count(word)
          keyword_dict[word] = wordfreq

      #list of (frequency, keyword)
      aux = [(keyword_dict[key], key) for key in keyword_dict]
      # puts the dictionary in ascending order
      aux.sort()
      # reverses order so it's now in descending order
      aux.reverse() 
      
      l = []
      for (a,b) in aux:
        # adds just the keyword to a list - not freq num
        l.append(b)
      
      # returns the num of keywords found, up to 3 keywords
      if len(l) == 1:
        top3 = l[0]
      elif len(l) == 2:
        top3 = [l[0], l[1]]
      else:
        # top 3 keywords with the highest freqs
        top3 = [l[0], l[1], l[2]]
      
      return top3
    pass

    @staticmethod
    def calc_read_time(text):
      # get the number of words in the text
      # 0 is placeholder for  now
      text = text.lower()
      text = re.sub(r'[^\w\s]', '', text) 
      
      word_list = text.split()
      num_words = len(word_list)
      print(num_words, "words")
      
      # define variable that is average human read time / min
      aver_words_per_minute = 225
      # divide numWords by aver read time
      read_time = math.ceil(num_words / aver_words_per_minute)
      return read_time

class Article:
    # create class after headlines/urls/html are scraped
    def __init__(self, headline, url, html):
        self.headline = headline
        self.url = url
        self.html = html
        

    """
        extract_article_details is mostly finished already
        this function takes the article's html and extracts stuff from it like the actual article text and its image_url, etc...
    """
    def extract_article_details(self):
        # This function already works, but can be edited at the bottom to extract additional details from the article's html

        # use self.html, and extract stuff like text and image_url from it
        # then set the corresponding class properties

        npa = newspaper.Article(" ")
        npa.download(self.html)
        npa.parse()

        # helper function inside main function
        def get_article_text(html):
            """
                newspaper fails to extract text properly from many sites, so we use
                jusText for the text extraction, and newspaper for all else
            """
            paragraphs = justext.justext(html, justext.get_stoplist("English"))
            # join all useful(non-boilerplate) paragraphs together with a space
            article_text = " ".join( p.text for p in paragraphs if not p.is_boilerplate )
            return article_text

        self.text = get_article_text(self.html)
        self.image_url = npa.top_image
        # etc...


    def analyze(self):
        # TODO
        self.summary = Analyzer.make_summary(self.text)
        self.sentiment = Analyzer.calculate_sentiment(self.text)
        self.keywords = Analyzer.extract_article_keywords(self.text)
        # etc...


    """ 
        keep extract_locations separate from the other analysis functions as it involves api calls 
        also, this function is finished already
    """
    def extract_locations(self):
        # finished
        # use self.text
        # extract location names from it as a list of strings
        # convert each location name into a tuple of (lat,lng)
        # set self.locations to be a dictionary where each place name is keyed to its lat/lng coordinates as a Tuple
        pass


    def create_json_str(self):
        # TODO
        # use all self properties
        # convert all self properties into a json string representation of the article object
        # don't store anywhere, instead return a string from the function
        # article must be converted into a json string to store in database
        # this function will create a properly formatted json string from its self Article's properties
        # this function does NOT set any self properties, instead it returns a string
        pass        


# possible pipeline in code:

scraper_inputs = []
Database = None

def run_website_scrapers(scraper_inputs):
    # this function is finished already
    pass
def filter_headlines(articles_dict):
    # use Analyzer.is_headline_relevant() inside here
    pass
def scrape_articles(articles_dict):
    # use requests inside here to get the html
    pass

def main():
    # scrape all websites
    # articles_dict is a dict of { "headline": "url" }
    articles_dict = run_website_scrapers(scraper_inputs)

    # remove articles with irrelevant headlines
    # same format as articles_dict, { "headline": "url" }
    filtered_articles_dict = filter_headlines(articles_dict)

    # scrape every article for its html
    # scraped_articles_dict is a dict of { "headline": (url, html) }
    # each headline points to a tuple containing that article's url and then its html
    scraped_articles_dict = scrape_articles(filtered_articles_dict)
    
    for article_headline in scraped_articles_dict:
        # unpack the tuple into named variables
        article_url, article_html = scraped_articles_dict[article_headline]

        # make an article class
        article = Article(article_headline, article_url, article_html)

        # extract text, image_url,etc... from article.html
        article.extract_article_details()

        # skip Article if its content is irrelevant to ecological matters
        if not Analyzer.is_content_relevant(article.text):
           continue

        # get all place names and coordinates mentioned in article.text
        # this involves an api call to get coordinates
        article.extract_locations()

        # get summary, sentiment, article's keywords, etc...
        article.analyze()

        # store article's json string representation in the database
        Database.store( article.create_json_str() )

main()

