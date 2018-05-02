var chat_form = new Vue({
  el: '#chat-form',
  data: {
    ods_catalog_url: "https://data.opendatasoft.com/api/datasets/1.0/"
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
})
