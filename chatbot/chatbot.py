import conversation_engine as Speech
import semantic_engine as SemanticEngine

import logging

logging.basicConfig(filename='info.log', level=logging.INFO)


class ChatBot(object):

    def __init__(self, ods_dataset_metas, ods_dataset_records, learned_denied_correspondances={}):
        self.introduction()
        self.learned_denied_correspondances = learned_denied_correspondances
        self.confirmed_correspondances = {'classes': {}, 'properties': {}}
        self.candidate_correspondances = SemanticEngine.init_correspondances_set(ods_dataset_metas, ods_dataset_records)
        self.awaiting_correspondances = {'classes': {}, 'properties': {}}
        self.denied_correspondances = {'classes': {}, 'properties': {}}

    def introduction(self):
        print Speech.greeting()
        print Speech.instructions()

    def start(self):
        self.process_classes_candidate_correspondances()
        self.process_properties_candidate_correspondances()

    def process_classes_candidate_correspondances(self):
        correspondance_type = 'classes'
        while self.candidate_correspondances[correspondance_type]:
            candidate = self.candidate_correspondances[correspondance_type].popitem()
            field_name = candidate[0]
            clss = candidate[1]
            candidate = SemanticEngine.get_class_uri(clss)
            if candidate:
                user_response = raw_input(Speech.class_question(field_name, candidate['description'][0]))
                while not Speech.is_valid(user_response):
                    print Speech.bad_answer()
                    user_response = raw_input(Speech.class_question(field_name, candidate['description'][0]))
                if Speech.is_positive(user_response):
                    self.confirm_class_correspondance(field_name, candidate['uri'], clss)
                    logging.info('USER:field {} of type {} ACCEPTED'.format(field_name, clss))
                    print Speech.reply_to_positive()
                elif not Speech.is_positive(user_response):
                    self.deny_class_correspondance(field_name, candidate['uri'], clss)
                    logging.info('USER:field {} of type {} DENIED'.format(field_name, clss))
                    print Speech.reply_to_negative()
                else:
                    self.postpone_class_correspondance(field_name, candidate['uri'], clss)
                    logging.info('USER:field {} of type {} POSTPONED'.format(field_name, clss))
                    print Speech.reply_to_neutral()
            else:
                self.deny_class_correspondance(field_name)
                logging.info('BOT:field {} of type {} DENIED cause: LOV SCORE TOO LOW'.format(field_name, clss))

    def process_properties_candidate_correspondances(self):
        correspondance_type = 'properties'
        while self.candidate_correspondances[correspondance_type]:
            candidate = self.candidate_correspondances[correspondance_type].popitem()
            field_name = candidate[0]
            field_label = candidate[1]
            candidate = SemanticEngine.get_property_uri(field_label)
            if candidate:
                for field, association in self.confirmed_correspondances['classes'].iteritems():
                    associated_class = association['class']
                    if field_name in self.learned_denied_correspondances:
                        if associated_class in self.learned_denied_correspondances[field_name]:
                            logging.info('BOT:field {} property {} linked to {} DENIED cause: LEARNED'.format(field_name, candidate['description'][0], associated_class))
                            continue
                    user_response = raw_input(Speech.property_question(field_name, candidate['description'][0], associated_class))
                    while not Speech.is_valid(user_response):
                        print Speech.bad_answer()
                        user_response = raw_input(Speech.class_question(field_name, candidate['description'][0]))
                    if Speech.is_positive(user_response):
                        self.confirm_property_correspondance(field_name, candidate['uri'], associated_class, field)
                        print Speech.reply_to_positive()
                        logging.info('USER:field {} property {} linked to {} ACCEPTED'.format(field_name, candidate['description'][0], associated_class))
                        break
                    elif not Speech.is_positive(user_response):
                        self.deny_property_correspondance(field_name, candidate['uri'], associated_class, field)
                        print Speech.reply_to_negative()
                        logging.info('USER:field {} property {} linked to {} DENIED'.format(field_name, candidate['description'][0], associated_class))
                        if field_name not in self.learned_denied_correspondances:
                            self.learned_denied_correspondances[field_name] = []
                        self.learned_denied_correspondances[field_name].append(associated_class)
                    else:
                        self.postpone_property_correspondance(field_name, candidate['uri'], associated_class, field)
                        print Speech.reply_to_neutral()
            else:
                self.deny_property_correspondance(field_name)
                logging.info('BOT:field {} property DENIED cause: LOV SCORE'.format(field_name))

    def confirm_class_correspondance(self, field, uri, clss):
        correspondance_type = 'classes'
        self.confirmed_correspondances[correspondance_type][field] = {}
        self.confirmed_correspondances[correspondance_type][field]['uri'] = uri
        self.confirmed_correspondances[correspondance_type][field]['class'] = clss

    def deny_class_correspondance(self, field, uri=None, clss=None):
        correspondance_type = 'classes'
        self.denied_correspondances[correspondance_type][field] = {}
        self.denied_correspondances[correspondance_type][field]['uri'] = uri
        self.denied_correspondances[correspondance_type][field]['class'] = clss

    def postpone_class_correspondance(self, field, uri, clss):
        correspondance_type = 'classes'
        self.awaiting_correspondances[correspondance_type][field] = {}
        self.awaiting_correspondances[correspondance_type][field]['uri'] = uri
        self.awaiting_correspondances[correspondance_type][field]['class'] = clss

    def confirm_property_correspondance(self, field, uri, associated_class, associated_field):
        correspondance_type = 'properties'
        self.confirmed_correspondances[correspondance_type][field] = {}
        self.confirmed_correspondances[correspondance_type][field]['uri'] = uri
        self.confirmed_correspondances[correspondance_type][field]['associated_class'] = associated_class
        self.confirmed_correspondances[correspondance_type][field]['associated_field'] = associated_field

    def deny_property_correspondance(self, field, uri=None, associated_class=None, associated_field=None):
        correspondance_type = 'properties'
        self.denied_correspondances[correspondance_type][field] = {}
        self.denied_correspondances[correspondance_type][field]['uri'] = uri
        self.denied_correspondances[correspondance_type][field]['associated_class'] = associated_class
        self.denied_correspondances[correspondance_type][field]['associated_field'] = associated_field

    def postpone_property_correspondance(self, field, uri, associated_class, associated_field):
        correspondance_type = 'properties'
        self.awaiting_correspondances[correspondance_type][field] = {}
        self.awaiting_correspondances[correspondance_type][field]['uri'] = uri
        self.awaiting_correspondances[correspondance_type][field]['associated_class'] = associated_class
        self.awaiting_correspondances[correspondance_type][field]['associated_field'] = associated_field
