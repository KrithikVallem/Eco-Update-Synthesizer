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


def make_summary(text):
  # Summary: takes in article text and returns a 30 word summary 
  
  # from gensim library 
  # split = False  - does NOT split text into indv. sentences 
  summary = summarize(text, word_count= 30, split=False)
  # add "..." to summary 
  summary_final = summary + "..."
  
  return summary_final


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