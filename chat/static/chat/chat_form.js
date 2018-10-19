var chat_form = new Vue({
  el: '#chat-form',
  data: {
    ods_catalog_url: "https://data.opendatasoft.com/api/datasets/1.0/",
    ods_suggestion_url: "https://data.opendatasoft.com/api/v2/catalog/datasets?rows=5&pretty=false&timezone=UTC&include_app_metas=false&where=datasetid%09%20like%20",
    suggestions: [],
    minimum_char_to_suggest: 2,
    suggestion_timeout_ms: 1000
  },
  watch: {
    suggestions: function (val) {
      $('#textBar').autocomplete({
          lookup: chat_form.suggestions
      });
      $('#textBar').focusout()
      $('#textBar').focus()
    }
  },
  methods: {
    dataset_exists: function (dataset) {
      this.$http.get(this.ods_catalog_url + dataset).then(response => {
        document.getElementById("textBar").classList.remove("is-invalid")
        window.location = "/chatbot/" + dataset;
      },response => {
        document.getElementById("textBar").classList.add("is-invalid")
        return false
      });
    },
    get_suggestions: function (query) {
      this.$http.get(this.ods_suggestion_url + "%22" + query +"%22").then(response => {
        ods_suggestions = []
        for (var i = 0; i < response.body['datasets'].length; i++){
          ods_suggestions.push({"value": response.body['datasets'][i]['dataset']['dataset_id']});
        }
        this.suggestions = ods_suggestions;
      },response => {
        return false;
      });
    }
  }
});

$(function(){
  $('.Global-container').keypress(function(e){
    if(e.which == 13) {
      dataset = document.getElementById("textBar").value;
      chat_form.dataset_exists(dataset)
    }
  })
});


var timeout = null;
$('#textBar').on('input',function(e){
  if (timeout !== null) {
        clearTimeout(timeout);
  }
  timeout = setTimeout(function () {
    var textbar_value = $("#textBar").val()
    if (textbar_value.length > chat_form.minimum_char_to_suggest){
      chat_form.get_suggestions(textbar_value);
    }
  }, chat_form.suggestion_timeout_ms);
});
