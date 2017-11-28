from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


def extract_noun(text):
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
        print text_nouns
    return text_nouns
