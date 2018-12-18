from chatbot import conversation_engine as ConversationEngine


class TestConversationEngine(object):

    def test_complete_conversation(self):
        assert ConversationEngine.greeting()
        assert ConversationEngine.instructions()
        assert ConversationEngine.class_question('field_name', 'class_description', 'uri')
        assert ConversationEngine.property_question('field_name', 'predicate_description', 'uri')
        assert ConversationEngine.property_class_question('field_name', 'predicate_description', 'uri')
        assert ConversationEngine.salutation()

    def test_conversation_errors(self):
        assert ConversationEngine.error_lov_unavailable()
        assert ConversationEngine.error_no_confirmed_class()
