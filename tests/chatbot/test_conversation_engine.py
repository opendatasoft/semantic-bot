from chatbot import conversation_engine as ConversationEngine

URI = 'http://www.example.org/Class'
DOMAIN_URI = 'http://www.example.org/Property'


class TestConversationEngine(object):

    def test_complete_conversation(self):
        assert ConversationEngine.greeting()
        assert ConversationEngine.instructions()
        assert ConversationEngine.class_question('field_name', 'class_description', URI)
        assert ConversationEngine.property_question('field_name', 'predicate_description', URI, DOMAIN_URI, 'domain_description')
        assert ConversationEngine.property_question('field_name', 'predicate_description', URI, None, None)
        assert ConversationEngine.property_class_question('predicate_description', DOMAIN_URI, 'domain_description')
        assert ConversationEngine.property_class_question('predicate_description', None, None)
        assert ConversationEngine.salutation()

    def test_conversation_errors(self):
        assert ConversationEngine.error_lov_unavailable()
        assert ConversationEngine.error_no_confirmed_class()
