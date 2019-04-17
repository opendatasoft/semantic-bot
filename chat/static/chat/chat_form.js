let chat_form = new Vue({
    el: '#chat-form',
    data: {
        ods_catalog_url: "https://data.opendatasoft.com/api/datasets/1.0/",
        ods_suggestion_url: "https://data.opendatasoft.com/api/v2/catalog/datasets?rows=20&pretty=false&timezone=UTC&include_app_metas=false&sort=explore.popularity_score&search=",
        suggestions: [],
        minimum_char_to_suggest: 2,
        suggestion_timeout_ms: 600
    },
    watch: {
        suggestions: function (val) {
            $('#textBar').autocomplete({
                lookup: chat_form.suggestions,
                /**
                 * Fills the 'autocomplete #textBar' with the dataset-id when a suggested dataset is selected
                 *
                 * @param {{favicon: String, value: String, data: String}} suggestion -
                 * The selected dataset object from suggestions array
                 */
                onSelect: function (suggestion) {
                    $('#textBar').val(suggestion.data);
                },
                /**
                 * Format dataset suggestion in the 'autocomplete #textBar' listbox
                 *
                 * @param {{favicon: String, value: String, data: String}} suggestion -
                 * A dataset suggestion from suggestions array
                 * @param {String} currentValue - The current value typed in #textBar
                 *
                 * @returns {String} Returns the HTML representation of the suggestion
                 */
                formatResult: function _formatResult(suggestion, currentValue) {
                    // Do not replace anything if the current value is empty
                    if (!currentValue) {
                        return suggestion.value + ' [' + suggestion.data + ']';
                    }

                    var utils = $.Autocomplete.utils;

                    var pattern = '(' + utils.escapeRegExChars(currentValue) + ')';

                    return '<img src="http://' + suggestion.favicon + '" class="portal-icon"> ' + suggestion.value
                            .replace(new RegExp(pattern, 'gi'), '<strong>$1<\/strong>')
                            .replace(/&/g, '&amp;')
                            .replace(/</g, '&lt;')
                            .replace(/>/g, '&gt;')
                            .replace(/"/g, '&quot;')
                            .replace(/&lt;(\/?strong)&gt;/g, '<$1>')
                        + ' [<b>' + suggestion.data
                            .replace(new RegExp(pattern, 'gi'), '<strong>$1<\/strong>')
                            .replace(/&/g, '&amp;')
                            .replace(/</g, '&lt;')
                            .replace(/>/g, '&gt;')
                            .replace(/"/g, '&quot;')
                            .replace(/&lt;(\/?strong)&gt;/g, '<$1>') + '</b>]';
                }
            });
            // To refresh visualisation
            $('#textBar').focusout();
            $('#textBar').focus();
        }
    },
    methods: {
        /**
         * Checks if a dataset exist on OpenDataSoft DATA network https://data.opendatasoft.com
         *
         * @param {String} dataset - The dataset-id of the dataset on DATA network
         *
         * @returns {Boolean} Returns HTML feedback and false if the dataset does not exist
         * Redirect to semantization if dataset exists.
         */
        dataset_exists: function (dataset) {
            this.$http.get(this.ods_catalog_url + dataset).then(response => {
                document.getElementById("textBar").classList.remove("is-invalid");
                window.location = "/chatbot/" + dataset;
            }, response => {
                document.getElementById("textBar").classList.add("is-invalid");
                return false;
            });
        },
        /**
         * Updates dataset suggestions using search api v2 of DATA network
         *
         * @param {String} query - The current value typed in the #textBar
         *
         * @returns {Boolean} Returns false if dataset is not found. Otherwise, updates ods_suggestions object with
         * new datasets.
         */
        get_suggestions: function (query) {
            this.$http.get(this.ods_suggestion_url + query).then(response => {
                ods_suggestions = [];
                for (var i = 0; i < response.body['datasets'].length; i++) {
                    title = response.body['datasets'][i]['dataset']['metas']['default']['title'];
                    dataset_id = response.body['datasets'][i]['dataset']['dataset_id'];
                    favicon = response.body['datasets'][i]['dataset']['metas']['default']['source_domain_address'] + '/favicon.ico';
                    ods_suggestions.push({"favicon": favicon, "value": title, "data": dataset_id});
                }
                this.suggestions = ods_suggestions;
            }, response => {
                return false;
            });
        }
    }
});

/** Executed when Enter Key (13) is pressed */
$(function () {
    $('.Global-container').keypress(function (e) {
        if (e.which === 13) {
            dataset = document.getElementById("textBar").value;
            chat_form.dataset_exists(dataset);
        }
    })
});

/** Executed when autocomplete #textBar is updated */
let timeout = null;
$('#textBar').on('input', function (e) {
    if (timeout !== null) {
        clearTimeout(timeout);
    }
    timeout = setTimeout(function () {
        var textbar_value = $("#textBar").val();
        if (textbar_value.length > chat_form.minimum_char_to_suggest) {
            chat_form.get_suggestions(textbar_value);
        }
    }, chat_form.suggestion_timeout_ms);
});
