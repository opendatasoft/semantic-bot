# ontology-mapping-chatbot

Ontology Mapping ChatBot is a  semi-interactive ontology mapping algorithm. It provides an easy-to-use interface (Yes or No questions) in order to semantize (e.g. to map ontologies on) OpenDataSoft datasets.

# The curse word (Ontology)

An `ontology` is a vocabulary defining the concepts and relationships used to describe an area of concern.
It's composed of:
* `classes` (i.e. Car, Building, Person, Disease, Source Code) to represent a concept.
* `properties` (i.e. horsepower, financed By, date of birth, has Symptoms, Author) to represent relation between concepts.
* `rules` (i.e. A person have a unique date of birth).
Ontologies can be created for every area of concern and by everyone using RDF (Resource Description Framework), RDFS (RDF Schema) and OWL (Web Ontology Language).

# LOV (Linked Open Vocabularies)
LOV is a ontology search engine. [This API](http://lov.okfn.org/dataset/lov/api) is used by the chatbot to find candidate ontologies for opendatasoft datasets.

# NLTK (Natural Language ToolKit)
This chatbot use NLTK to perform natural language processing:

### Lemmatization
Lemmatization is a process of removing and replacing word suffixes to arrive at a common root form of the word.

> Eating -> Eat

> Persons -> Person

### Stop words
We dont wants useless word to be stored and treated in order to improve performance and reduce noise.
we can easily remove them with nltk:
> This is perfect -> "This Perfect"

### Part of Speech tagging
For `class` detection, we are only interested in Noun.
nltk Part of Speech tagging labels words in a sentence as nouns, adjectives, verbs...

### Named Entity Recognition
The idea is to have the machine immediately be able to pull out "entities" like people, places, things, locations, monetary figures, and more.

> OpenDataSoft - ORGANIZATION

# Prelude
Assuming you already have `python` and `pip`
install `NLTK` and `beautifulsoup`

```bash
pip install nltk
```

```bash
python -m nltk.downloader popular
```

```bash
pip install wikipedia
```

```bash
pip install beautifulsoup4
```
# Run the demo
Navigate to ontology-mapping-chatbot folder and execute:

```bash
python ontobot.py <dataset_id>
```
replace `<dataset_id>` with the dataset_id of the dataset you want to semantize (only support DATA domain)

> python ontobot.py roman-emperors@public

