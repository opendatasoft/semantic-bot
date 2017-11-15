from utils.lov_api import LovApi

print LovApi.vocabulary_request("Person", "English")
print LovApi.term_request("Person", "class")
