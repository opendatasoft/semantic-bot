import random

# HTML tag used to accentuate a text
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

PROPERTY_QUESTIONS = ["It seems that the field {field_name} is <a href='{uri}' target='_blank'>{predicate_description}</a> of {domain}?",
                      "Is the field {field_name} is <a href='{uri}' target='_blank'>{predicate_description}</a> of {domain}.",
                      "I think that the field {field_name} is <a href='{uri}' target='_blank'>{predicate_description}</a> of {domain}. Am I right?",
                      "Does the field {field_name} is <a href='{uri}' target='_blank'>{predicate_description}</a> of {domain}?"]

PROPERTY_CLASS_QUESTIONS = ["Select the field that identifies {domain} that have {predicate_description} as a characteristic.",
                            "Select the field that contains {domain} that have {predicate_description} as a characteristic.",
                            "Which field contains {domain} that have {predicate_description} as a characteristic?",
                            "Which field identifies {domain} that have {predicate_description} as a characteristic?"]

SALUTATION = ["""I have no more questions to ask.<br>
                 You will find your mapping below.<br>
                 Feel free to improve the quality of the mapping using <a href="https://help.opendatasoft.com/apis/tpf/#rml-mapping" target="_blank">RML</a>.<br>
                 Have a good day!"""]

ERROR_LOV_UNAVAILABLE = ["""Sorry, the chatbot is unavailable for the moment.<br>
                           Try again later"""]

ERROR_NO_CONFIRMED_CLASS = ["Sorry, I was not able to semantize your dataset."]


def greeting():
    """Returns the first string that will be sent to the user"""
    return random.choice(GREETINGS)


def instructions():
    """Returns the string that briefly explains how the chatbot works"""
    return random.choice(INSTRUCTIONS)


def class_question(field_name, class_description, uri):
    """
        Returns the string that proposes a class correspondance to the user

        Asks if a field is containing resources of a specific class of an ontology
    """
    field_name = EMPHASIS.format(field_name)
    class_description = EMPHASIS.format(class_description)
    return random.choice(CLASS_QUESTIONS).format(field_name=field_name, class_description=class_description, uri=uri)


def property_question(field_name, predicate_description, uri, domain_uri, domain_description):
    """
        Returns the string that proposes a property correspondance to the user

        Asks if a field represents a specific property of an ontology
    """
    if not domain_uri:
        domain = 'something'
    else:
        domain = "<a href='{domain_uri}' target='_blank'>{domain_description}</a>".format(domain_uri=domain_uri, domain_description=domain_description)
    field_name = EMPHASIS.format(field_name)
    predicate_description = EMPHASIS.format(predicate_description)
    domain = EMPHASIS.format(domain)
    return random.choice(PROPERTY_QUESTIONS).format(field_name=field_name, predicate_description=predicate_description, uri=uri, domain=domain)


def property_class_question(predicate_description, domain_uri, domain_description):
    """Returns the string that ask the user to define domain of the property"""
    if not domain_uri:
        domain = 'an object'
    else:
        domain = "<a href='{domain_uri}' target='_blank'>{domain_description}</a>".format(domain_uri=domain_uri, domain_description=domain_description)
    domain = EMPHASIS.format(domain)
    predicate_description = EMPHASIS.format(predicate_description)
    return random.choice(PROPERTY_CLASS_QUESTIONS).format(domain=domain, predicate_description=predicate_description)


def salutation():
    """Returns the last string that will be sent to the user when a mapping is proposed"""
    return random.choice(SALUTATION)


def error_lov_unavailable():
    """Returns the string that will be sent to the user if lov service is unavailable"""
    return random.choice(ERROR_LOV_UNAVAILABLE)


def error_no_confirmed_class():
    """Returns the last string that will be sent to the user when no mapping could be proposed"""
    return random.choice(ERROR_NO_CONFIRMED_CLASS)
