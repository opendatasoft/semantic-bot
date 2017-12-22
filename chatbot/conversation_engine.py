import random

GREETINGS = ["Hello",
             "Hi",
             "greetings",
             "Welcome"]

INSTRUCTIONS = ["""I will ask you questions about your dataset.
                You will be able to communicate with me by answering with 'yes', 'no'."""]

CLASS_QUESTIONS = ["It seems that your dataset contains {class_description}? Is it true?",
                   "Looks like you have {class_description} in your dataset. Am I right?",
                   "Is your dataset describes {class_description}?",
                   "Does your dataset represents {class_description}?",
                   "Does your dataset contains {class_description}?"]

PREDICATE_QUESTIONS = ["It seems that the field {field_name} represents {predicate_question}? Is it true?",
                       "Is the field {field_name} represents {predicate_question}?",
                       "I think that the field {field_name} represents {predicate_question}",
                       "Does your field {field_name} is {predicate_question}?"]

POSITIVE_ANSWER = ["Yes, yes, yep, Yep, Ok, ok"]

NAGATIVE_ANSWER = ["No, no, nop, Nop"]


def Greeting():
    return random.choice(GREETINGS)


def Instructions():
    return random.choice(INSTRUCTIONS)


def class_question(class_description):
    return random.choice(CLASS_QUESTIONS).format(class_description=class_description)


def predicate_question(field_name, predicate_description):
    return random.choice(PREDICATE_QUESTIONS).format(field_name=field_name, predicate_question=predicate_description)


def is_positive(answer):
    if answer in POSITIVE_ANSWER:
        return True
    elif answer in NAGATIVE_ANSWER:
        return False
    return None
