import socket
import string
import unicodedata
import urllib.request
from collections import defaultdict
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
from bs4.element import Comment

from utils.misc import DEFAULT_REQUEST_TIMEOUT

SKIP_TAGS = ['style', 'script', 'head', 'title', 'meta', '[document]']


class WordCounter:
    @staticmethod
    def from_website(website_url):
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

        error = False
        counter = defaultdict(int)
        try:
            html = urllib.request.urlopen(
                website_url, timeout=DEFAULT_REQUEST_TIMEOUT).read()
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
        except Exception as e:
            error = e

        return counter, error
