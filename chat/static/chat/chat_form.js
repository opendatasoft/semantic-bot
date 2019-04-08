// Overide jquery autocomplete format result to support domain favicon
$.Autocomplete.defaults.formatResult = function _formatResult(suggestion, currentValue) {
    // Do not replace anything if the current value is empty
    if (!currentValue) {
        return suggestion.value + ' [' + suggestion.data + ']';
    }

    var utils = $.Autocomplete.utils

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
};

var chat_form = new Vue({
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
                onSelect: function (suggestion) {
                    $('#textBar').val(suggestion.data);
                }
            });
            $('#textBar').focusout();
            $('#textBar').focus();
        }
    },
    methods: {
        dataset_exists: function (dataset) {
            this.$http.get(this.ods_catalog_url + dataset).then(response => {
                document.getElementById("textBar").classList.remove("is-invalid");
                window.location = "/chatbot/" + dataset;
            }, response => {
                document.getElementById("textBar").classList.add("is-invalid");
                return false;
            });
        },
        get_suggestions: function (query) {
            this.$http.get(this.ods_suggestion_url + query).then(response => {
                ods_suggestions = [];
                for (var i = 0; i < response.body['datasets'].length; i++) {
                    title = response.body['datasets'][i]['dataset']['metas']['default']['title'];
                    dataset_id = response.body['datasets'][i]['dataset']['dataset_id'];
                    favicon = response.body['datasets'][i]['dataset']['metas']['default']['source_domain_address'] + '/favicon.ico'
                    ods_suggestions.push({"favicon": favicon, "value": title, "data": dataset_id});
                }
                this.suggestions = ods_suggestions;
            }, response => {
                return false;
            });
        }
    }
});

$(function () {
    $('.Global-container').keypress(function (e) {
        if (e.which == 13) {
            dataset = document.getElementById("textBar").value;
            chat_form.dataset_exists(dataset);
        }
    })
});


var timeout = null;
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
