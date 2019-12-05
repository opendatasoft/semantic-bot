window.$ = window.jQuery = require('jquery');
require('bootstrap-sass');

import Vue from 'vue';
import VueResource from 'vue-resource';
import VueHighlightJS from 'vue-highlightjs';
import VueClipboard from 'vue-clipboard2';
import Intro from "./components/intro.vue";
import Headerapp from "./components/header.vue";
import Aboutapp from "./components/about.vue";
import Formchatapp from "./components/formchat.vue";
import Mainmappingapp from "./components/mainmapping.vue";
import Mainschemaapp from "./components/mainschema.vue";
import Messaging from "./components/messaging.vue";

const ODS_RECORD_DATASET = '/api/records/datasets/';

Vue.use(VueResource);
Vue.use(VueHighlightJS);
Vue.use(VueClipboard);

window.Vue = Vue;
const app = new Vue({
    el: '#app',
    components: {
        Intro,
        Headerapp,
        Aboutapp,
        Formchatapp,
        Mainmappingapp,
        Mainschemaapp,
        Messaging
    },
    data: function () {
        return {
            dataset: null,
            dataset_fields: {},
            dataset_records: null,
            dataset_language: 'en',
            correspondances: {'classes': [], 'properties': []},
            confirmed_correspondances: {'classes': [], 'properties': []},
            denied_correspondances: {'classes': [], 'properties': []},
            passed_correspondances: {'classes': [], 'properties': []},
            is_property_ready: false,
            confirmed_property_correspondances: null
        }
    },
    watch: {
        confirmed_correspondances: {
            handler: function (confirmed_correspondances) {
                this.$emit('newConfirmedCorrespondance', confirmed_correspondances);
            },
            deep: true
        },
        'confirmed_correspondances.classes': {
            handler: function (confirmed_classes_correspondances) {
                confirmed_classes_correspondances.forEach(class_correspondance => {
                    this.dataset_fields[class_correspondance.field_name].class = class_correspondance.class
                });
            },
            deep: true
        }
    },
    created() {
        console.log('Component has been created');
    },
    methods: {
        /** Start the semantization. This method is called in formchat component when the dataset is selected */
        start_semantization: function () {
            this.$emit('isWaiting', true);
            this.dataset_language = this.dataset.metas.language;
            Promise.all([this.retrieve_dataset_fields(), this.retrieve_dataset_records()]).then(results => {
                const dataset_fields = results[0];
                const dataset_records = results[1];
                let data = {'records': dataset_records, 'fields': dataset_fields};
                // Retrieve class correspondances
                // Should be processed before properties
                let promises = [];
                for (let field_name in this.dataset_fields) {
                    promises.push(this.retrieve_class_correspondance(field_name, data));
                }
                Promise.all(promises).then(() => {
                    if (this.correspondances.classes.length > 0){
                        this.$emit('classFoundEvent', true);
                        this.$emit('switchSelectorEvent', 'class');
                        this.$emit('isWaiting', false);
                    }
                    // Retrieve preoperties correspondances
                    promises = [];
                    for (let field_name in this.dataset_fields) {
                        promises.push(this.retrieve_property_correspondance(field_name, data));
                    }
                    Promise.all(promises).then(() => {
                        this.is_property_ready = true;
                        if (this.correspondances.classes.length <= 0) {
                            this.$emit('isWaiting', false);
                            if (this.correspondances.properties.length > 0) {
                                this.$emit('propertyFoundEvent', true);
                                this.$emit('switchSelectorEvent', 'property');
                            } else {
                                this.finish_semantization();
                            }
                        }
                    });
                });
            });
        },
        /** Retrieve the property correspondance for a field of the dataset */
        retrieve_property_correspondance: function (field_name, data) {
            return new Promise( (resolve, reject) => {
                this.$http.post("/api/" + this.dataset.datasetid + "/correspondances/field/property?field=" + field_name + "&lang=" + this.dataset_language, data).then(response => {
                    if (response.body) {
                        this.correspondances['properties'].push(response.body);
                        resolve(true);
                    }else{resolve(false);}
                }, response => {
                    reject();
                });
            })
        },
        /** Retrieve the class correspondance for a field of the dataset */
        retrieve_class_correspondance: function (field_name, data) {
            return new Promise( (resolve, reject) => {
                this.$http.post("/api/" + this.dataset.datasetid + "/correspondances/field/class?field=" + field_name + "&lang=" + this.dataset_language, data).then(response => {
                    if (response.body) {
                        this.correspondances['classes'].push(response.body);
                        resolve(true);
                    } else {resolve(false);}
                }, response => {
                    reject();
                });
            });
        },
        /** Retrieve records of the dataset from the catalog api v2 of OpenDataSoft DATA Network */
        retrieve_dataset_records: function () {
            return this.$http.get(ODS_RECORD_DATASET + this.dataset.datasetid)
                .then(response => response.json())
                .then(json => {
                    this.dataset_records = json.records;
                    return json.records;
                });
        },
        /** Retrieve dataset fields from dataset object */
        retrieve_dataset_fields: function () {
            return new Promise((resolve, reject) => {
                let dataset_fields = {};
                this.dataset.fields.forEach( field => {
                    field['class'] = null;
                    dataset_fields[field.name] = field;
                });
                this.dataset_fields = dataset_fields;
                resolve(dataset_fields);
            });
        },
        /**
         * Get the url where RDF mapping of the dataset can be updated on ods platform
         *
         * @returns {String} message - The url where RDF mapping of the dataset can be updated
         */
        get_mapping_set_url: function () {
            let dataset_id = this.dataset.datasetid.split('@')[0];
            let dataset_domain_adress = this.dataset.metas.source_domain_address;
            return "https://" + dataset_domain_adress + "/publish/" + dataset_id + "/#information";
        },
        /** Find and Confirm class correspondances using an array of field_name */
        confirm_class_correspondance: function (field_names) {
            let confirmed_class_correspondances = this.correspondances.classes.filter(correspondance => {
                return field_names.includes(correspondance.field_name);
            });
            confirmed_class_correspondances.forEach(confirmed_class_correspondance =>
                this.confirmed_correspondances.classes.push(confirmed_class_correspondance));
            this.correspondances.classes.forEach(denied_class_correspondance =>
                this.denied_correspondances.classes.push(denied_class_correspondance));
            this.correspondances.classes = [];
            if (this.is_property_ready) {
                this.$emit('isWaiting', false);
                if (this.correspondances.properties.length > 0) {
                    this.$emit('propertyFoundEvent', true);
                    this.$emit('switchSelectorEvent', 'property');
                }
            }
        },
        /** Pass class correspondances */
        pass_class_correspondance: function () {
            this.correspondances.classes.forEach(passed_class_correspondance =>
                this.passed_correspondances.classes.push(passed_class_correspondance));
            this.correspondances.classes = [];
            if (this.is_property_ready) {
                this.$emit('isWaiting', false);
                if (this.correspondances.properties.length > 0) {
                    this.$emit('propertyFoundEvent', true);
                    this.$emit('switchSelectorEvent', 'property');
                }
            }
        },
        /** Find and Confirm property correspondances using an array of field_name */
        confirm_property_correspondance: function (field_names) {
            this.confirmed_property_correspondances = this.correspondances.properties.filter(correspondance => {
                return field_names.includes(correspondance.field_name);
            });
            this.correspondances.properties.forEach(denied_property_correspondance =>
                this.denied_correspondances.properties.push(denied_property_correspondance));
            this.correspondances.properties = [];
            this.confirm_property_range_correspondance();
            this.select_domain_property();
        },
        /** Pass property correspondances */
        pass_property_correspondance: function () {
            this.correspondances.properties.forEach(passed_property_correspondance =>
                this.passed_correspondances.properties.push(passed_property_correspondance));
            this.correspondances.properties = [];
            this.finish_semantization();
        },
        /** Add range of confirmed property as confirmed class correspondances */
        confirm_property_range_correspondance: function () {
            this.confirmed_property_correspondances.forEach(confirmed_property_correspondance => {
                if (confirmed_property_correspondance.range) {
                    confirmed_property_correspondance.range.field_name = confirmed_property_correspondance.field_name;
                    confirmed_property_correspondance.range.label = confirmed_property_correspondance.label;
                    this.confirmed_correspondances.classes.push(confirmed_property_correspondance.range);
                }
            });
        },
        /** Find a domain for the next confirmed property correspondance */
        select_domain_property: function () {
            if (this.confirmed_property_correspondances.length > 0) {
                let confirmed_property_correspondance = this.confirmed_property_correspondances.shift();
                this.$emit('selectFieldEvent', confirmed_property_correspondance);
            } else {
                this.finish_semantization();
            }
        },
        /** Confirm the domain field of a confirmed property */
        confirm_field_property_correspondance: function (property_correspondance, field) {
            property_correspondance.associated_field = field.name;
            property_correspondance.domain.field_name = field.name;
            property_correspondance.domain.label = field.label;
            if (field.class && field.class !== 'Thing') {
                property_correspondance.associated_class = field.class;
                //
            } else {
                let field_new_class = property_correspondance.domain.class;
                this.dataset_fields[field.name].class = field_new_class;
                property_correspondance.associated_class = field_new_class;
                this.update_confirmed_class_correspondances(property_correspondance.domain);
            }
            this.confirmed_correspondances.properties.push(property_correspondance);
            this.select_domain_property();
        },
        /** update a class correspondance (if existing... or creates a new one) using the domain of the property */
        update_confirmed_class_correspondances: function (domain_class_correspondance) {
            this.confirmed_correspondances.classes = this.confirmed_correspondances.classes.filter((correspondance) => {
                return correspondance.field_name !== domain_class_correspondance.field_name;
            });
            this.confirmed_correspondances.classes.push(domain_class_correspondance);
        },
        /** Confirm the domain field of a confirmed property */
        finish_semantization: function () {
            if (this.confirmed_correspondances.classes.length > 0) {
                this.$emit('finishSemantizationEvent', true);
                this.$emit('switchSelectorEvent', 'finish');
            } else {
                this.$emit('finishSemantizationEvent', false);
                this.$emit('switchSelectorEvent', 'finish');
            }
            // Send results for log purpose
            this.confirmed_correspondances['fields'] = this.dataset_fields;
            this.passed_correspondances['fields'] = this.dataset_fields;
            this.denied_correspondances['fields'] = this.dataset_fields;
            this.$http.post('/api/' + this.dataset.datasetid + '/correspondances/confirmed', this.confirmed_correspondances).then(() => {
                this.$http.post('/api/' + this.dataset.datasetid + '/correspondances/awaiting', this.passed_correspondances).then(() => {
                    this.$http.post('/api/' + this.dataset.datasetid + '/correspondances/denied', this.denied_correspondances).then(() => {});
                });
            });
        }
    }
});