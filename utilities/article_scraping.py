import requests_html
from typing import Dict, List, Tuple, NewType

HEADLINE = NewType("HEADLINE", str)
URL = NewType("URL", str)
HTML = NewType("HTML", str)


def scrape_articles(articles_dict: Dict[HEADLINE,URL]) -> List[Tuple[HEADLINE,URL,HTML]]:
    """
        @param articles_dict: a dict of {headline: url} pairs for each article
        @return: a list of tuples of (headline, url, html) for each article

        this function uses the requests_html library to scrape all articles asynchronously
    """
    asession = requests_html.AsyncHTMLSession()
    async_scrapers = []

    for headline,url in articles_dict.items():

        def make_async_scraper(headline, url):
            async def scraper_func():
                try:
                    response = await asession.get(url)
                    html = response.content
                    return (headline, url, html)
                except:
                    # in case of scraping error, return None
                    return None

            return scraper_func
        
        async_scrapers.append( make_async_scraper(headline,url) )

    # run all article scrapers and remove None values (caused by failed scraping attempts)
    return [
        article_tuple 
        for article_tuple in asession.run( *async_scrapers ) 
        if article_tuple is not None
    ]
