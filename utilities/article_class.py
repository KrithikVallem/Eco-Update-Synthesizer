# choose service to use for geocoding place names to coordinates
# full list here: https://geocoder.readthedocs.io/index.html#providers
GEOCODING_PROVIDER = "osm"
# some geocodingservices require api_keys, for those that don't, make this variable None
GEOCODING_API_KEY = None

# scrape urls's and connect to api for geocoding
from newspaper.urls import url_to_filetype
import requests_html

# extract text (justext) and other article details (newspaper) from article html
import justext
import newspaper

# extract location names from article text
# https://github.com/elyase/geotext
from geotext import GeoText

# convert place names to coordinates
import geocoder

# convert class properties into json
import json

# import all things we made ourselves
from . import analysis # analysis.py



class Article:
    def __init__(self, headline, url, html):
        self.headline = headline
        self.url = url
        self.html = html


    def extract_article_details(self):
        """
            uses: self.html
            sets: self.text and self.image_url, both as strings
        """

        npa = newspaper.Article("")
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

        # if jusText cannot successfully extract the text, then use newspaper as a backup
        self.text = get_article_text(self.html) or npa.text
        self.image_url = npa.top_image

    
    def analyze(self):
        ''' TODO '''
        """
            uses self.text
            sets self.summary, self.sentiment, self.keywords, self.reading_time
        """
        # self.summary = analysis.make_summary(self.text) # can't get this to run, ask analysis team later
        self.sentiment = ":)" # TODO
        self.keywords = analysis.extract_article_keywords(self.text)
        self.reading_time = analysis.calc_read_time(self.text)

    
    def extract_locations(self):
        """
            uses: self.text
            sets: self.locations as a dict of {placeName: (lat,lng)}
        """
        # extract cities from text
        places = GeoText(self.text).cities
        # remove duplicates
        places = list(set(places))

        # make a dictionary that will contain the located places and their coordinates
        coordinates_dict = {}

        # geocoder documentation recommends using sessions when you have a large number of requests to make
        with requests_html.HTMLSession() as session:
            for place in places:
                try:
                    # first get the specified mapping_service function
                    mapping_service_function = getattr(geocoder, GEOCODING_PROVIDER)
                    # next get the response from passing a location name to the online mapping service
                    response = mapping_service_function(place, key=GEOCODING_API_KEY, session=session)

                    coordinate = (response.json['lat'], response.json['lng'])

                    coordinates_dict[place] = coordinate
                except:
                    pass

        self.locations = coordinates_dict

    # returns a dictionary that can be converted to json by json.dumps
    def encode(self):
        return {
            "headline": self.headline,
            "url": self.url,
            "text": self.text,
            "image_url": self.image_url,
            # "summary": self.summary,
            "sentiment": self.sentiment,
            "keywords": self.keywords,
            "reading_time": self.reading_time,
            "locations": self.locations,
        }
