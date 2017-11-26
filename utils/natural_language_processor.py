from nltk import word_tokenize, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords
from wikipedia import wikipedia
from bs4 import BeautifulSoup


class NLProcessor(object):
    """
    This class implements Natural Language Processing used by the Ontology ChatBot.
    It use BeautifulSoup to extract text from HTML and NLTK for Natural Language Processing
    """

    @staticmethod
    def extract_noun(text):
        """Return a list with singular and plural noun."""
        stop_words = set(stopwords.words('english'))
        text = BeautifulSoup(text, 'html.parser').get_text()
        text = word_tokenize(text)
        filtered_text = []
        for word in text:
            if word not in stop_words:
                filtered_text.append(word)
        filtered_text = pos_tag(filtered_text)
        text_nouns = []
        for item in filtered_text:
            if item[1] == 'NNS' or item[1] == 'NNP':
                text_nouns.append(item[0])
        return text_nouns

    @staticmethod
    def named_entity_recognition(records):
        """Return a list with singular and plural noun."""
        print wikipedia.page("test", auto_suggest=True).content
