import random
from bs4 import BeautifulSoup

GREETINGS = ["Hello,",
             "Hi,",
             "greetings,",
             "Welcome,"]

INSTRUCTIONS = ["""I will ask you questions about your dataset.
You will be able to communicate with me by answering with 'yes' or 'no'."""]

BAD_ANSWER = ["""Sorry, I didn't understood your answer.
Can you answer with 'yes' or 'no'."""]

CLASS_QUESTIONS = ["It seems that your dataset contains {class_description}? Is it true?",
                   "Looks like you have {class_description} in your dataset. Am I right?",
                   "Is your dataset describes {class_description}?",
                   "Does your dataset represents {class_description}?",
                   "Does your dataset contains {class_description}?"]

PREDICATE_QUESTIONS = ["It seems that the field {field_name} represents {predicate_question}? Is it true?",
                       "Is the field {field_name} represents {predicate_question}?",
                       "I think that the field {field_name} represents {predicate_question}",
                       "Does your field {field_name} is {predicate_question}?"]

POSITIVE_ANSWER = ["yes", "yep", "ok"]

NAGATIVE_ANSWER = ["no", "nop"]


def greeting():
    return random.choice(GREETINGS)


def instructions():
    return random.choice(INSTRUCTIONS)


def bad_answer():
    return random.choice(BAD_ANSWER)


def class_question(class_description):
    cleaned_description = BeautifulSoup(class_description, "html5lib").get_text()
    return random.choice(CLASS_QUESTIONS).format(class_description=cleaned_description)


def predicate_question(field_name, predicate_description):
    cleaned_description = BeautifulSoup(predicate_description, "html5lib").get_text()
    return random.choice(PREDICATE_QUESTIONS).format(field_name=field_name, predicate_question=cleaned_description)


def is_positive(answer):
    if answer.lower() in POSITIVE_ANSWER:
        return True
    elif answer.lower() in NAGATIVE_ANSWER:
        return False
    return None
