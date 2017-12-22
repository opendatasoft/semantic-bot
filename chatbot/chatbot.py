import conversation_engine as Speech
import semantic_engine as SemanticeEngine


class ChatBot(object):

    def __init__(self, ods_dataset_metas, ods_dataset_records):
        self.confirmed_correspondances = {'classes': {}, 'properties': {}}
        self.candidate_correspondances = SemanticeEngine.init_correspondances_set(ods_dataset_metas, ods_dataset_records)
        self.awaiting_correspondances = {'classes': {}, 'properties': {}}
        self.denied_correspondances = {'classes': {}, 'properties': {}}

    def start(self):
        for field, clss in self.candidate_correspondances['classes'].iteritems():
            candidate = SemanticeEngine.get_class_uri(clss)
            if candidate:
                user_response = raw_input(Speech.class_question(candidate['description']))
                if Speech.is_positive(user_response):
                    self.confirm_correspondance('classes', field, candidate['uri'])
                else:
                    self.deny_correspondance('classes', field)
            else:
                self.deny_correspondance('classes', field)

    def confirm_correspondance(self, correspondance_type, field, uri):
        self.confirmed_correspondances[correspondance_type][field] = self.candidate_correspondances[correspondance_type][field]
        self.confirmed_correspondances[correspondance_type][field]['uri'] = uri

    def deny_correspondance(self, correspondance_type, field):
        self.denied_correspondances[correspondance_type][field] = self.candidate_correspondances[correspondance_type][field]
