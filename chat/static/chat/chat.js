var chat = new Vue({
  el: '#chat-app',
  data: {
    dataset_id: document.location.pathname,
    messages: [],
    correspondances: {},
    confirmed_correspondances: {'classes': [], 'properties': []},
    denied_correspondances: {'classes': [], 'properties': []},
    awaiting_correspondances: {'classes': [], 'properties': []},
    awaiting_user: false,
    current_correspondance: {},
    current_correspondance_type: 'classes',
  },
  mounted: function(){
        this.bot_introduction();
  },
  methods: {
    push_user_message: function (message) {
      this.messages.push({
       text: message,
       type: 'user'
      })
    },
    push_bot_message: function (message) {
      this.messages.push({
       text: message,
       type: 'bot'
     })
    },
    bot_introduction: function () {
      this.$http.get('/api/conversation/greeting').then(response => {
        this.push_bot_message(response.body['text']);
        this.$http.get('/api/conversation/instructions').then(response => {
          this.push_bot_message(response.body['text']);
          this.next_semantize();
        })
      })
    },
    next_semantize: function () {
      if (this.correspondances['classes'].length > 0) {
        this.current_correspondance_type = 'classes'
        this.current_correspondance = this.correspondances['classes'].pop();
        this.$http.post('/api/conversation/question/class', this.current_correspondance).then(response => {
          this.push_bot_message(response.body['text']);
          this.awaiting_user = true;
        })
      } else {
        console.log(this);
      }
    },
    user_input_yes: function () {
      if (this.awaiting_user) {
        this.push_user_message("Yes.");
        this.awaiting_user = false;
        this.confirmed_correspondances[this.current_correspondance_type].push(this.current_correspondance);
        this.next_semantize();
      }
    },
    user_input_idk: function () {
      if (this.awaiting_user) {
        this.push_user_message("I don't know.");
        this.awaiting_user = false;
        this.awaiting_correspondances[this.current_correspondance_type].push(this.current_correspondance);
        this.next_semantize();
      }
    },
    user_input_no: function () {
      if (this.awaiting_user) {
        this.push_user_message("No.");
        this.awaiting_user = false;
        this.denied_correspondances[this.current_correspondance_type].push(this.current_correspondance);
        this.next_semantize();
      }
    },
  },
});

chat.correspondances = {"classes": [{"description": "Company", "field_name": "verif_who", "uri": "http://vivoweb.org/ontology/core#Company", "class": "Company"}, {"description": "Person", "field_name": "dynasty", "uri": "http://xmlns.com/foaf/0.1/Person", "class": "Person"}, {"description": "PopulatedPlace", "field_name": "birth_cty", "uri": "http://dbpedia.org/ontology/PopulatedPlace", "class": "PopulatedPlace"}, {"description": "Person", "field_name": "name", "uri": "http://xmlns.com/foaf/0.1/Person", "class": "Person"}], "properties": [{"field_name": "reign_start", "uri": "http://dbpedia.org/ontology/startReign", "description": "start reign"}, {"field_name": "index", "uri": "http://d-nb.info/standards/elementset/gnd#thematicIndexNumericDesignationOfMusicalWork", "description": "Thematic index numeric designation of musical work"}, {"field_name": "verif_who", "uri": "http://purl.org/healthcarevocab/v1#VerificationFlag", "description": "VerificationFlag"}, {"field_name": "death", "uri": "http://dbpedia.org/ontology/deathPlace", "description": "death place"}, {"field_name": "name", "uri": "http://purl.org/ontology/wo/name", "description": "name"}, {"field_name": "name_full", "uri": "http://www.w3.org/2000/10/swap/pim/contact#fullName", "description": "fullName"}, {"field_name": "birth", "uri": "http://dbpedia.org/ontology/birthPlace", "description": "birth place"}, {"field_name": "dynasty", "uri": "http://simile.mit.edu/2003/10/ontologies/vraCore3#dynasty", "description": "dynasty"}, {"field_name": "rise", "uri": "http://www.disit.org/km4city/schema#moonrise", "description": "moonrise"}, {"field_name": "birth_prv", "uri": "http://dbpedia.org/ontology/birthPlace", "description": "birth place"}, {"field_name": "reign_end", "uri": "http://dbpedia.org/ontology/endReign", "description": "end reign"}, {"field_name": "era", "uri": "http://dbpedia.org/ontology/era", "description": "era"}, {"field_name": "image", "uri": "http://dbpedia.org/ontology/picture", "description": "Une image de quelque chose."}, {"field_name": "cause", "uri": "http://openprovenance.org/model/opmo#cause", "description": "cause"}, {"field_name": "notes", "uri": "http://dbpedia.org/ontology/notes", "description": "notes"}, {"field_name": "birth_cty", "uri": "http://dbpedia.org/ontology/city", "description": "city"}]}
