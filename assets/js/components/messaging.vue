<template>
  <div id="inersidepanel"  class="messaging animated fadeIn" v-if="appstarted">
        <ul id="messagesContainer">
          <li class=" animated fadeInUp delay-1s">
            Hi!
          </li>
          <li  class=" animated fadeInUp delay-2s">
            Semantic description of dataset can significantly improve data quality.<br />
            I will assist you during this process by asking you questions about your dataset.<br />
            You can answer with the buttons in the bottom.<br />
            You can also check the progression of the process with the Toggle mapping button
          </li>
          <li  class=" animated fadeInUp delay-3s">
            Please choose a dataset from <a href="https://data.opendatasoft.com" target="_blank">Opendatasoft's data network</a>
          </li>
          <li class=" data-response  animated fadeInUp " v-show="dataset_id">
            {{ dataset_id }}
          </li>
          <li class="data-info animated fadeInUp " v-show="is_class_found">
            I found some classes in your dataset,<br />
            please check them to continue.
          </li>
          <li class=" data-response  animated fadeInUp " v-show="processed_class_correspondances.length > 0">
            <ul>
              <li v-for="{field_name, label, description, checked} in processed_class_correspondances">
                <div v-if="checked">
                  Field {{ label }} contains {{ description }}
                </div>
                <div v-else>
                  <s>
                    Field {{ label }} contains {{ description }}
                  </s>
                </div>
              </li>
            </ul>
          </li>
          <li class=" data-response  animated fadeInUp " v-show="pass_class_correspondances">
            I don't know.
          </li>
          <li class=" data-info animated fadeInUp " v-show="is_property_found">
            I found some properties in your dataset,<br />
            please check them to continue.
          </li>
          <li class=" data-response  animated fadeInUp " v-show="processed_property_correspondances.length > 0">
            <ul>
              <li v-for="{field_name, label, description, domain, checked} in processed_property_correspondances">
                <div v-if="checked">
                  Field {{ label }} is {{ description }} of {{ domain.description }}
                </div>
                <div v-else>
                  <s>
                    Field {{ label }} is {{ description }} of {{ domain.description }}
                  </s>
                </div>
              </li>
            </ul>
          </li>
          <li class=" data-response  animated fadeInUp " v-show="pass_property_correspondances">
            I don't know.
          </li>
          <ul id="field_messages">
          </ul>
          <li class="data-info  animated fadeInUp " v-show="is_semantization_success">
            I have no more questions to ask.<br />
            You will find your mapping on the right.<br />
            Feel free to improve the quality of the mapping using <a href="https://help.opendatasoft.com/apis/tpf/#rml-mapping" target="_blank">YARRRML.</a>
            Have a good day!
          </li>
          <li class="data-info  animated fadeInUp " v-show="is_semantization_failure">
            Sorry, I was not able to semantize your dataset.<br />
            You can still create your mapping using <a href="https://help.opendatasoft.com/apis/tpf/#rml-mapping" target="_blank">YARRRML.</a>
            Have a good day!
          </li>
        </ul>
        <ul  v-show="is_waiting">
          <li class="data-load  animated fadeInUp ">
            <img src="static/img/loading.svg" />
          </li>
        </ul>
  </div>
</template>

<script>

export default {
  name: 'Messaging',
  data: function () {
    return {
      appstarted: false,
      is_waiting: false,
      dataset_id: null,
      is_class_found: false,
      is_property_found: false,
      processed_class_correspondances: [],
      pass_class_correspondances: false,
      processed_property_correspondances: [],
      pass_property_correspondances: false,
      is_semantization_success: false,
      is_semantization_failure: false
    }
  },
  methods: {
    startApp: function (event) {
      this.$root.$emit('appstartedEvent', true);
    },
    scrollToEnd() {
      setTimeout(() => {
        let container = this.$el.querySelector("#messagesContainer");
        container.scrollTop = container.scrollHeight;
      }, 50);
    }
  },
  mounted: function () { 
    this.$root.$on('appstartedEvent', (appstartedstate) => {
      this.appstarted = appstartedstate;
    });
    this.$root.$on('isWaiting', (is_waiting) => {
      this.is_waiting = is_waiting;
    });
    this.$root.$on('datasetID', (dataset_id) => {
      this.dataset_id = dataset_id;
      this.scrollToEnd();
    });
    this.$root.$on('classFoundEvent', (is_class_found) => {
      this.is_class_found = is_class_found;
      this.scrollToEnd();
    });
    this.$root.$on('propertyFoundEvent', (is_property_found) => {
      this.is_property_found = is_property_found;
      this.scrollToEnd();
    });
    this.$root.$on('confirmedClassCorrespondancesEvent', (checked_fields) => {
      this.processed_class_correspondances = this.$root.correspondances.classes;
      this.processed_class_correspondances.forEach(class_correspondance =>
              class_correspondance.checked = checked_fields.includes(class_correspondance.field_name));
      this.scrollToEnd();
    });
    this.$root.$on('passClassCorrespondancesEvent', () => {
      this.pass_class_correspondances = true;
      this.scrollToEnd();
    });
    this.$root.$on('confirmedPropertyCorrespondancesEvent', (checked_fields) => {
      this.processed_property_correspondances = this.$root.correspondances.properties;
      this.processed_property_correspondances.forEach(property_correspondance =>
              property_correspondance.checked = checked_fields.includes(property_correspondance.field_name));
      this.scrollToEnd();
    });
    this.$root.$on('passPropertyCorrespondancesEvent', () => {
      this.pass_property_correspondances = true;
      this.scrollToEnd();
    });
    this.$root.$on('selectFieldEvent', (confirmed_property_correspondance) => {
      let message = document.createElement('li');
      message.classList.add('data-info');
      message.classList.add('animated');
      message.classList.add('fadeInUp');
      message.classList.add('delay-1s');
      message.innerHTML = 'Which field contains' +
              '<a href=\"' + confirmed_property_correspondance.domain.uri + '\" target=\"_blank\">' +
              confirmed_property_correspondance.domain.description + '</a>' +
              'with' +
              '<a href=\"' + confirmed_property_correspondance.uri + '\" target=\"_blank\">' +
              confirmed_property_correspondance.description + '</a>' + '?';
      document.getElementById('field_messages').appendChild(message);
      this.scrollToEnd();
    });
    this.$root.$on('fieldSelectedEvent', (field) => {
      let message = document.createElement('li');
      message.classList.add('data-response');
      message.classList.add('animated');
      message.classList.add('fadeInUp');
      message.innerHTML = field.label;
      document.getElementById('field_messages').appendChild(message);
      this.scrollToEnd();
    });
    this.$root.$on('finishSemantizationEvent', (success) => {
      this.is_semantization_success = success;
      this.is_semantization_failure = !success;
      this.scrollToEnd();
    });
  }
}
</script>

<style lang="scss">

</style>
