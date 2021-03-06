import socket
import string

import unicodedata
import urllib.request
from collections import defaultdict
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4.element import Comment

from utils.misc import DEFAULT_REQUEST_TIMEOUT

SKIP_TAGS = ['style', 'script', 'head', 'title', 'meta', '[document]']


class WordCounter:
    def from_html(html):
        def tag_visible(element):
            if element.parent.name in SKIP_TAGS:
                return False
            if isinstance(element, Comment):
                return False
            return True

        def text_from_html(body):
            soup = BeautifulSoup(body, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)
            return visible_texts

        counter = defaultdict(int)
        texts = text_from_html(html)
        for text in texts:
            # normalize character, like space
            text = unicodedata.normalize('NFKD', text.strip())
            for word in text.split(' '):
                word_strip = word.strip().lower()
                # strip special characters, e.g Furthermore, => Furthermore
                # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
                for c in string.punctuation:
                    word_strip = word_strip.strip(c)
                if word_strip:
                    counter[word_strip] += 1

        return counter

    @staticmethod
    def from_website(website_url):
        error = False
        counter = {}
        try:
            html = urllib.request.urlopen(
                website_url, timeout=DEFAULT_REQUEST_TIMEOUT).read()
            counter = WordCounter.from_html(html)
        except Exception as e:
            if hasattr(e, 'reason'):
                if isinstance(e.reason, socket.timeout):
                    error = 'Timeout occurred while fetching'
                else:
                    error = 'Fetching error: {}'.format(e.reason.capitalize())
            else:
                error = str(e)

        return counter, error


def parser_website_url(website_url):
    if website_url:
        # set default schema
        parser = urlparse(website_url, scheme='http')
        website_url = parser.geturl()

    # TODO Seems geturl() from urllib.parse return redundant scheme mapping
    return website_url.replace('http:///', 'http://').lower()
