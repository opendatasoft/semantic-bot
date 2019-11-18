<template>
  <div class="formchat animated fadeIn delay-1s"  v-if="appstarted">
    <div class="dialogmss">
    </div>
    <classselector v-if="is_visible_class_selector"></classselector>
    <propertyselector  v-if="is_visible_property_selector"></propertyselector>
    <div class="input-chatbot" v-on:keyup.enter="onEnterField"  v-if="is_visible_fields_selector">
      <vue-simple-suggest
              autocomplete="off"
              v-model="selected_field"
              display-attribute="name"
              value-attribute="name"
              placeholder="Search a field"
              :id="'textBar2'"
              :list="getSuggestionListFields"
              :styles="simple_suggest_style"
              :filter-by-query="true"
              :min-length="0"
              :max-suggestions="7"
      >
        <div class="suggestion-item" slot="suggestion-item" slot-scope="{ suggestion, query }">
          <span class="suggestion-item-name">{{ suggestion.label }}</span>
          <span class="suggestion-item-id">{{ suggestion.class }}</span>
        </div>
      </vue-simple-suggest>
    </div>
    <div class="input-chatbot" v-on:keyup.enter="onEnterDataset" v-if="is_visible_dataset_selector">
      <vue-simple-suggest
              autocomplete="off"
              v-model="selected_dataset_id"
              display-attribute="dataset.dataset_id"
              value-attribute="dataset.dataset_id"
              placeholder="dataset-id@domain-id"
              :id="'textBar'"
              :list="getSuggestionList"
              :styles="simple_suggest_style"
              :min-length="3"
              :max-suggestions="7"
              :debounce="300"
      >
        <div class="suggestion-item" slot="suggestion-item" slot-scope="{ suggestion, query }">
          <span class="suggestion-item-name">{{ suggestion.dataset.metas.default.title }}</span>
          <span class="suggestion-item-id">{{ suggestion.dataset.dataset_id }}</span>
        </div>
      </vue-simple-suggest>
    </div>
    <div class="input-chatbot" v-if="is_visible_waiting_selector">
      Please wait...
    </div>
    <div class="input-chatbot input-chatbot-btn" v-show="is_visible_finish_selector">
      <button class="btn btn-secondary" onClick="window.location.reload();">New mapping</button>
      <getmappingbtn></getmappingbtn>
    </div>
  </div>
</template>

<script>
  import VueSimpleSuggest from 'vue-simple-suggest'
  import Classselector from "./classselector.vue";
  import Propertyselector from "./propertyselector.vue";
  import Getmappingbtn from "./getmappingbtn.vue";

  const ODS_SUGGESTIONS_URL = '/api/catalog?rows=20&sort=explore.popularity_score&search=';
  const ODS_DATASET_LOOKUP_URL = '/api/catalog/datasets/';

  export default {
      name: 'Formchat',
      components: {
        VueSimpleSuggest,
        Classselector,
        Propertyselector,
        Getmappingbtn
      },
      data: function () {
          return {
              appstarted: false,
              selected_dataset_id: '',
              selected_field: '',
              viewsubselect: false,
              datasets_suggestion: [],
              is_visible_dataset_selector: true,
              is_visible_class_selector: false,
              is_visible_property_selector: false,
              is_visible_fields_selector: false,
              is_visible_waiting_selector: false,
              is_visible_finish_selector: false,
              current_property_correspondance: null,
              simple_suggest_style: {
                defaultInput : 'form-control form-control-lg'
              }
          }
      },
      mounted: function () {
          this.$root.$on('appstartedEvent', (appstartedstate) => {
            this.appstarted = appstartedstate;
          });
        this.$root.$on('switchSelectorEvent', (new_selector) => {
          this.is_visible_dataset_selector = false;
          this.is_visible_class_selector = false;
          this.is_visible_property_selector = false;
          this.is_visible_fields_selector = false;
          this.is_visible_waiting_selector = false;
          switch(new_selector) {
            case 'dataset':
              this.is_visible_dataset_selector = true;
              break;
            case 'class':
              this.is_visible_class_selector = true;
              break;
            case 'property':
              this.is_visible_property_selector = true;
              break;
            case 'field':
              this.is_visible_fields_selector = true;
              break;
            case 'waiting':
              this.is_visible_waiting_selector = true;
              break;
            case 'finish':
              this.is_visible_finish_selector = true;
              break;
            default:
              this.is_visible_dataset_selector = true;
          }
        });
        this.$root.$on('isWaiting', (is_waiting) => {
          if (is_waiting) {
            this.$root.$emit('switchSelectorEvent', 'waiting');
          }
        });
        this.$root.$on('selectFieldEvent', (confirmed_property_correspondance) => {
          this.current_property_correspondance = confirmed_property_correspondance;
          this.$root.$emit('switchSelectorEvent', 'field');
        });
        this.$root.$on('newConfirmedCorrespondance', (confirmed_correspondances) => {
          this.$http.post('/api/' + this.$root.dataset.datasetid + '/correspondances/mapping', confirmed_correspondances).then(response => {
          this.mapping = response.body;
        });
        });
      },
      methods: {
        getSuggestionListFields() {
          return Object.values(this.$root.dataset_fields);
        },
        getSuggestionList() {
          this.datasets_suggestion = this.$http.get(ODS_SUGGESTIONS_URL + this.selected_dataset_id)
                  .then(response => response.json())
                  .then(json => json.datasets);
          return this.datasets_suggestion;
        },
        onEnterDataset() {
          this.$http.get(ODS_DATASET_LOOKUP_URL + this.selected_dataset_id).then(response => {
            document.getElementById("textBar").classList.remove("is-invalid");
            return response.json()
          }).then(json => {
            // Dataset is selected. Semantization starts
            this.$root.dataset = json;
            this.$root.$emit('datasetID', json.datasetid);
            this.$root.start_semantization();
          }, function () {
            document.getElementById("textBar").classList.add("is-invalid");
          });
        },
        onEnterField() {
          if (this.selected_field in this.$root.dataset_fields) {
            document.getElementById("textBar2").classList.remove("is-invalid");
            let field = this.$root.dataset_fields[this.selected_field];
            this.$root.$emit('fieldSelectedEvent', field);
            this.$root.confirm_field_property_correspondance(this.current_property_correspondance, field);
          } else {
            document.getElementById("textBar2").classList.add("is-invalid");
          }
        }
      }
  }
</script>

<style lang="scss">

</style>