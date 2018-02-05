import random

GREETINGS = ["Hello,",
             "Hi,",
             "greetings,",
             "Welcome,"]

INSTRUCTIONS = ["""I will ask you questions about your dataset.
You will be able to communicate with me by answering with the
3 buttons in the bottom."""]

BAD_ANSWER = ["""Sorry, I didn't understood your answer.
Can you answer with 'yes', 'no' or an empty answer"""]

CLASS_QUESTIONS = ["It seems that field {field_name} describes {class_description}? Is it true?",
                   "Looks like the field {field_name} represents {class_description}. Am I right?",
                   "Is the field {field_name} in your dataset describes {class_description}?",
                   "Does the field {field_name} in your dataset represents {class_description}?",
                   "Does your dataset contains {class_description} in the field {field_name}?"]

PROPERTY_QUESTIONS = ["It seems that the field {field_name} represents {predicate_description} of {associated_class}? Is it true?",
                      "Is the field {field_name} represents {predicate_description} and is an attribute of {associated_class}?",
                      "I think that the field {field_name} represents {predicate_description} of {associated_class}.",
                      "Does your field {field_name} is {predicate_description} of {associated_class}?"]

POSITIVE_ANSWER = ["yes", "yep", "ok", "y"]

POSITIVE_REPLY = ["Perfect, I added this information to your dataset.",
                  "Thanks, this information is added to your dataset.",
                  "Good. This was added to your dataset"]

NEGATIVE_ANSWER = ["no", "nop", "n"]

NEGATIVE_REPLY = ["Okay, lets forget about that.",
                  "Ok, i will try to find something better.",
                  "Thanks, I will find something else.",
                  ]

NEUTRAL_ANSWER = ["idk", "don't know", "dont know", "", " "]

NEUTRAL_REPLY = ["Okay, We will see that later.",
                 "I will put this one apart.",
                 "Ok, maybe later"]

SALUTATION = ["I have no more questions to ask.\nYour mapping have benn updated.\nHave a good day!"]


def greeting():
    return random.choice(GREETINGS)


def instructions():
    return random.choice(INSTRUCTIONS)


def bad_answer():
    return random.choice(BAD_ANSWER)


def class_question(field_name, class_description):
    return random.choice(CLASS_QUESTIONS).format(field_name=field_name, class_description=class_description)


def property_question(field_name, predicate_description, associated_class):
    return random.choice(PROPERTY_QUESTIONS).format(field_name=field_name, predicate_description=predicate_description, associated_class=associated_class)


def is_valid(answer):
    if answer.lower() in POSITIVE_ANSWER or answer.lower() in NEGATIVE_ANSWER or answer.lower() in NEUTRAL_ANSWER:
        return True
    return False


def is_positive(answer):
    if answer.lower() in POSITIVE_ANSWER:
        return True
    elif answer.lower() in NEGATIVE_ANSWER:
        return False
    return None


def is_neutral(answer):
    if answer.lower() in NEUTRAL_ANSWER:
        return True
    return False


def reply_to_positive():
    return random.choice(POSITIVE_REPLY)


def reply_to_negative():
    return random.choice(NEGATIVE_REPLY)


def reply_to_neutral():
    return random.choice(NEUTRAL_REPLY)


def salutation():
    return random.choice(SALUTATION)
