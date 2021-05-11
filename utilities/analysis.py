import newspaper, justext # used for extracting article's details from its html
import requests
import re
import string
import numpy as np
import scipy
#import gensim
import pprint
# from gensim.summarization import summarize # not working, how do I install this? ask analysis team later
import math 

keywords = [
  'polar',
  'green',
  'nature',
  'iceberg',
  'biodiversity',
  'biology',
  'dioxide',
  'monoxide',
  'carpooling',
  'habitat'
  'warming',
  'acid',
  'pollution',
  'quality',
  'air',
  'algae',
  'alternative',
  'energy',
  'atmosphere',
  'burning',
  'biodegradable',
  'biodiversity',
  'bioenergy',
  'biofuels',
  'biomass',
  'biome',
  'biosphere',
  'biotech',
  'biotechnology',
  'carbon',
  'neutrality',
  'cfcs',
  'cfl',
  'climate',
  'change',
  'compost',
  'compostable',
  'composting',
  'conservation',
  'cryptosporidium',
  'deforestation',
  'dioxins',
  'disposal',
  'draught',
  'dumping',
  'ecosystem',
  'ecotourism',
  'electric',
  'emissions',
  'projections',
  'energy',
  'efficiency',
  'rating',
  'environmental',
  'flora',
  'fauna',
  'fossil',
  'fuel',
  'fuels',
  'garden',
  'gardening',
  'global',
  'green',
  'greenhouse',
  'gases',
  'water',
  'hazardous',
  'incinerator',
  'insulation',
  'kyoto',
  'landfill',
  'mbt',
  'mulch',
  'npws',
  'epa',
  'noxious',
  'oil',
  'organic',
  'organic',
  'organism',
  'ozone',
  'pollution',
  'pesticides',
  'plastic',
  'plants',
  'pollutants',
  'planting',
  'radiation',
  'radioactive',
  'radon',
  'recycle',
  'reforestation',
  'renewable',
  'reuse',
  'river',
  'sewage',
  'smog',
  'smokeless',
  'solar',
  'sustainable',
  'sustainability',
  'toxic',
  'toxin',
  'utility',
  'ventilation',
  'waste',
  'prevention',
  'vapour',
  'wind',
  'turbine',
  'wwf',
  'zero',
]

#print(keywords)


def is_headline_relevant(headline):
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


# def make_summary(text):
#   # Summary: takes in article text and returns a 30 word summary 
  
#   # from gensim library 
#   # split = False  - does NOT split text into indv. sentences 
#   summary = summarize(text, word_count= 30, split=False)
#   # add "..." to summary 
#   summary_final = summary + "..."
  
#   return summary_final


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
  if len(l) < 1: ## added this if branch because the program crashes without it ~ Krithik
    top3 = []
  elif len(l) == 1:
    top3 = [l[0]] ##
  elif len(l) == 2:
    top3 = [l[0], l[1]]
  else:
    # top 3 keywords with the highest freqs
    top3 = [l[0], l[1], l[2]]
  
  return top3


def calc_read_time(text):
  # get the number of words in the text
  # 0 is placeholder for  now
  text = text.lower()
  text = re.sub(r'[^\w\s]', '', text) 
  
  word_list = text.split()
  num_words = len(word_list)
  #print(num_words, "words")
  
  # define variable that is average human read time / min
  aver_words_per_minute = 225
  # divide numWords by aver read time
  read_time = math.ceil(num_words / aver_words_per_minute)
  return read_time
