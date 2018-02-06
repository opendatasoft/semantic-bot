var chat = new Vue({
  el: '#chat-app',
  data: {
    dataset_id: get_dataset_id(),
    messages: [],
    correspondances: {},
    confirmed_correspondances: {'classes': [], 'properties': []},
    denied_correspondances: {'classes': [], 'properties': []},
    awaiting_correspondances: {'classes': [], 'properties': []},
    current_correspondance: {},
    current_correspondance_type: 'classes',
    awaiting_user: false,
    yes_no_questions: true,
  },
  mounted: function(){
      this.bot_introduction();

  },
  methods: {
    push_user_message: function (message) {
      this.messages.push({
       text: message,
       type: 'user'
     });
    setTimeout(scroll_chat_to_bottom, 100);
    },
    push_bot_message: function (message) {
      setTimeout(function(){
       chat.messages.push({
       text: message,
       type: 'bot'
      });
      setTimeout(scroll_chat_to_bottom, 100);
    }, 1000);
    },
    bot_introduction: function () {
      this.$http.get('/api/conversation/greeting').then(response => {
        this.push_bot_message(response.body['text']);
        this.$http.get('/api/conversation/instructions').then(response => {
          this.push_bot_message(response.body['text']);
          this.$http.get('/api/'+ this.dataset_id +'/correspondances').then(response => {
            this.correspondances = response.body;
            this.next_semantize();
          });
        });
      });
    },
    next_semantize: function () {
      if (this.correspondances['classes'].length > 0) {
        this.current_correspondance_type = 'classes'
        this.current_correspondance = this.correspondances['classes'].pop();
        this.$http.post('/api/conversation/question/class', this.current_correspondance).then(response => {
          this.push_bot_message(response.body['text']);
          this.awaiting_user = true;
        });
      } else if (this.correspondances['properties'].length > 0) {
        this.current_correspondance_type = 'properties'
        this.current_correspondance = this.correspondances['properties'].pop();
        this.$http.post('/api/conversation/question/property', this.current_correspondance).then(response => {
          this.push_bot_message(response.body['text']);
          this.awaiting_user = true;
        });
      } else {
        this.$http.post('/api/' + this.dataset_id +'/correspondances/mapping', this.confirmed_correspondances).then(response => {
          this.$http.get('/api/conversation/salutation').then(response => {
            this.push_bot_message(response.body['text']);
          });
        });
      }
    },
    user_input_yes: function () {
      if (this.awaiting_user) {
        this.push_user_message("Yes.");
        this.$http.get('/api/conversation/answer/positive').then(response => {
          this.push_bot_message(response.body['text']);
          this.awaiting_user = false;
          if ((this.current_correspondance_type == 'properties') && (this.confirmed_correspondances['classes'].length > 0)) {
            this.$http.post('/api/conversation/question/property-class', this.current_correspondance).then(response => {
              this.push_bot_message(response.body['text']);
              this.yes_no_questions = false;
              this.awaiting_user = true;
            });
          } else {
            this.confirmed_correspondances[this.current_correspondance_type].push(this.current_correspondance);
            setTimeout(function(){chat.next_semantize()},1500);
          }
        })
      }
    },
    user_input_idk: function () {
      if (this.awaiting_user) {
        this.push_user_message("I don't know.");
        this.$http.get('/api/conversation/answer/neutral').then(response => {
          this.push_bot_message(response.body['text']);
          this.awaiting_user = false;
          this.awaiting_correspondances[this.current_correspondance_type].push(this.current_correspondance);
          setTimeout(function(){chat.next_semantize()},1500);
        });
      }
    },
    user_input_no: function () {
      if (this.awaiting_user) {
        this.push_user_message("No.");
        this.$http.get('/api/conversation/answer/negative').then(response => {
          this.push_bot_message(response.body['text']);
          this.awaiting_user = false;
          this.denied_correspondances[this.current_correspondance_type].push(this.current_correspondance);
          setTimeout(function(){chat.next_semantize()},1500);
        });
      }
    },
    user_input_property_class: function (associated_class) {
      if ((this.awaiting_user) && (!this.yes_no_questions)) {
        if (associated_class == null){
          this.push_user_message('None of those');
          this.$http.get('/api/conversation/answer/negative').then(response => {
            this.push_bot_message(response.body['text']);
            this.awaiting_user = false;
            this.current_correspondance['associated_class'] = [];
            this.current_correspondance['associated_field'] = [];
            this.denied_correspondances[this.current_correspondance_type].push(this.current_correspondance);
            this.yes_no_questions = true;
            setTimeout(function(){chat.next_semantize()},1500);
          });
        } else {
          this.push_user_message(associated_class['class']);
          this.$http.get('/api/conversation/answer/positive').then(response => {
            this.push_bot_message(response.body['text']);
            this.awaiting_user = false;
            this.current_correspondance['associated_class'] = associated_class['class'];
            this.current_correspondance['associated_field'] = associated_class['field_name'];
            this.confirmed_correspondances[this.current_correspondance_type].push(this.current_correspondance);
            this.yes_no_questions = true;
            setTimeout(function(){chat.next_semantize()},1500);
          });
        }
      }
    },
  },
});
