import random


EMPHASIS = "<b>{}</b>"

GREETINGS = ["Hello,",
             "Hi,",
             "Welcome,"]

INSTRUCTIONS = ["""<b>Semantic</b> description of dataset can significantly <b>improve data quality</b>.<br>
I will assist you during this process by asking you <b>questions</b> about your dataset.<br>
You can <b>answer with the buttons in the bottom</b>.<br>
You can also check the progression of the process with the <b>Toggle mapping button</b>"""]


CLASS_QUESTIONS = ["It seems that field {field_name} contains <a href='{uri}' target='_blank'>{class_description}</a>? Is it true?",
                   "Looks like the field {field_name} contains <a href='{uri}' target='_blank'>{class_description}</a>. Am I right?",
                   "Is the field {field_name} in your dataset contains <a href='{uri}' target='_blank'>{class_description}</a>?",
                   "Does the field {field_name} in your dataset contains <a href='{uri}' target='_blank'>{class_description}</a>?",
                   "Does the dataset contains <a href='{uri}' target='_blank'>{class_description}</a> in the field {field_name}?"]

PROPERTY_QUESTIONS = ["It seems that the field {field_name} is <a href='{uri}' target='_blank'>{predicate_description}</a>?",
                      "Is the field {field_name} is <a href='{uri}' target='_blank'>{predicate_description}</a>.",
                      "I think that the field {field_name} is <a href='{uri}' target='_blank'>{predicate_description}</a>.",
                      "Does the field {field_name} is <a href='{uri}' target='_blank'>{predicate_description}</a>?"]

PROPERTY_CLASS_QUESTIONS = ["<a href='{uri}' target='_blank'>{predicate_description}</a>({field_name}) is the characteristic of which object?",
                            "Select the object that have <a href='{uri}' target='_blank'>{predicate_description}</a>({field_name}) as a characteristic.",
                            "Select the object that have the characteristic <a href='{uri}' target='_blank'>{predicate_description}</a>({field_name})."]


SALUTATION = ["""I have no more questions to ask.<br>
                 You will find your mapping below.<br>
                 Feel free to improve the quality of the mapping using <a href="https://help.opendatasoft.com/apis/tpf/#rml-mapping" target="_blank">RML</a>.<br>
                 Have a good day!"""]

ERROR_LOV_UNAVAILABLE = ["""Sorry, the chatbot is unavailable for the moment.<br>
                           Try again later"""]

ERROR_NO_CONFIRMED_CLASS = ["Sorry, I was not able to semantize your dataset."]


def greeting():
    return random.choice(GREETINGS)


def instructions():
    return random.choice(INSTRUCTIONS)


def class_question(field_name, class_description, uri):
    field_name = EMPHASIS.format(field_name)
    class_description = EMPHASIS.format(class_description)
    return random.choice(CLASS_QUESTIONS).format(field_name=field_name, class_description=class_description, uri=uri)


def property_question(field_name, predicate_description, uri):
    field_name = EMPHASIS.format(field_name)
    predicate_description = EMPHASIS.format(predicate_description)
    return random.choice(PROPERTY_QUESTIONS).format(field_name=field_name, predicate_description=predicate_description, uri=uri)


def property_class_question(field_name, predicate_description, uri):
    field_name = EMPHASIS.format(field_name)
    predicate_description = EMPHASIS.format(predicate_description)
    return random.choice(PROPERTY_CLASS_QUESTIONS).format(predicate_description=predicate_description, field_name=field_name, uri=uri)


def salutation():
    return random.choice(SALUTATION)


def error_lov_unavailable():
    return random.choice(ERROR_LOV_UNAVAILABLE)


def error_no_confirmed_class():
    return random.choice(ERROR_NO_CONFIRMED_CLASS)
