// -----------------------
// Graph parameters
// -----------------------
// nodes are growing proportionally to its number of predicates
const node_growing_factor = 2;
const node_init_radius = 30;
const link_color = '#999';
const node_resource_color = '#007fa4';
const node_value_color = '#E8E8E8';

let chat = new Vue({
    el: '#chat-app',
    data: {
        dataset_id: get_dataset_id(),
        dataset_fields: {},
        messages: [],
        correspondances: {},
        confirmed_correspondances: {'classes': [], 'properties': []},
        denied_correspondances: {'classes': [], 'properties': []},
        awaiting_correspondances: {'classes': [], 'properties': []},
        current_correspondance: {},
        current_correspondance_type: 'classes',
        awaiting_user: false,
        // Show or hide selector to interact with user
        yes_no_selector: true,
        class_selector: false,
        field_selector: false,
        get_mapping_selector: false,
        // autocomplete on fields
        suggestions: [],
        selected_field: null,
        is_finished: false,
        rml_mapping: null,
        source_domain_address: null,
        language: "en",
        // time to compute correspondances (user waiting)
        server_time: Date.now(),
        // time to answer correspondances (user interacting)
        client_time: null
    },
    mounted: function () {
        this.bot_introduction();
        this.init_field_selector();
    },
    methods: {
        init_field_selector: function () {
            $('#fieldTextBar').autocomplete({
                lookup: this.suggestions,
                /**
                 * Updates the 'selected_field' variable with the field_name when a suggested field is selected
                 *
                 * @param {{value: String, data: String, class: String}} suggestion -
                 * The selected field object from suggestions array
                 */
                onSelect: function (suggestion) {
                    chat.selected_field = suggestion;
                },
                minChars: 0,
                maxHeight: 200,
                /**
                 * Format field suggestion in the 'autocomplete #textBar' listbox
                 *
                 * @param {{value: String, data: String, class: String}} suggestion -
                 * A field suggestion from suggestions array
                 * @param {String} currentValue - The current value typed in #fieldTextBar
                 *
                 * @returns {String} Returns the HTML representation of the suggestion
                 */
                formatResult: function _formatResult(suggestion, currentValue) {

                    let utils = $.Autocomplete.utils;

                    let pattern = '(' + utils.escapeRegExChars(currentValue) + ')';

                    if (suggestion.class) {
                        return '<b>' + suggestion.value
                                .replace(new RegExp(pattern, 'gi'), '<strong>$1<\/strong>')
                                .replace(/&/g, '&amp;')
                                .replace(/</g, '&lt;')
                                .replace(/>/g, '&gt;')
                                .replace(/"/g, '&quot;')
                                .replace(/&lt;(\/?strong)&gt;/g, '<$1>') + '</b>'
                            + ' (' + suggestion.class + ')';
                    } else {
                        return '<b>' + suggestion.value
                            .replace(new RegExp(pattern, 'gi'), '<strong>$1<\/strong>')
                            .replace(/&/g, '&amp;')
                            .replace(/</g, '&lt;')
                            .replace(/>/g, '&gt;')
                            .replace(/"/g, '&quot;')
                            .replace(/&lt;(\/?strong)&gt;/g, '<$1>') + '</b>';
                    }
                }
            });
        },
        /**
         * Sends a message from the user to the chat
         *
         * @param {String} message - The message of the user
         */
        push_user_message: function (message) {
            this.messages.push({
                text: message,
                type: 'user'
            });
            setTimeout(scroll_chat_to_bottom, 100);
        },
        /**
         * Sends a message from the bot to the chat
         *
         * @param {String} message - The message of the bot
         */
        push_bot_message: function (message) {
            chat.messages.push({
                text: message,
                type: 'bot'
            });
            setTimeout(scroll_chat_to_bottom, 100);
        },
        /** Retrieve dataset metadatas from the catalog api v2 of OpenDataSoft DATA Network */
        get_dataset_metas: function () {
            this.$http.get('https://data.opendatasoft.com/api/v2/catalog/datasets/' + this.dataset_id).then(response => {
                // domain url
                this.source_domain_address = response.body['dataset']['metas']['default']['source_domain_address'];
                // dataset language
                this.language = response.body['dataset']['metas']['default']['language'];
                // Compute url to mapping form
                mapping_set_url = this.get_mapping_set_url();
                $('#urlSetMapping').append("<a href=\"" + mapping_set_url + "\" target=\"_blank\">" + mapping_set_url + "</a>");
                // dataset fields
                for (i = 0; i < response.body['dataset']['fields'].length; i++) {
                    response.body['dataset']['fields'][i]['class'] = null;
                    this.dataset_fields[response.body['dataset']['fields'][i]['name']] = response.body['dataset']['fields'][i];
                    this.suggestions.push({"value": response.body['dataset']['fields'][i]['label'],
                                           "data": response.body['dataset']['fields'][i]['name'],
                                           "class": null});
                }
            }, response => {
                this.$http.get('/api/conversation/error/lov-unavailable').then(response => {
                    this.push_bot_message(response.body['text']);
                    this.is_finished = true;
                });
            });
        },
        /**
         * Get the url where RDF mapping of the dataset can be updated
         *
         * @returns {String} message - The url where RDF mapping of the dataset can be updated
         */
        get_mapping_set_url: function () {
            dataset_id = this.dataset_id.split('@')[0];
            return "https://" + this.source_domain_address + "/publish/" + dataset_id + "/#information";
        },
        /** Sends welcome messages, Retrieve dataset correspondances and Initialize semantization */
        bot_introduction: function () {
            // Welcome messages
            this.$http.get('/api/conversation/greeting').then(response => {
                this.push_bot_message(response.body['text']);
                this.$http.get('/api/conversation/instructions').then(response => {
                    this.push_bot_message(response.body['text']);
                    // Retrieve all correspondances (classes and properties)
                    this.$http.get('/api/' + this.dataset_id + '/correspondances').then(response => {
                        this.correspondances = response.body;
                        this.get_dataset_metas();
                        if (! this.is_finished) {
                            this.next_semantize();
                            // start client time
                            this.client_time = Date.now();
                        }
                        // compute server time
                        this.server_time = Math.floor((Date.now() - this.server_time)/1000);
                    }, response => {
                        this.$http.get('/api/conversation/error/lov-unavailable').then(response => {
                            this.push_bot_message(response.body['text']);
                            this.is_finished = true;
                        });
                    });
                });
            });
        },
        /** Processes the next correspondance or finish the semantization and returns the RDF mapping */
        next_semantize: function () {
            if (this.correspondances['classes'].length > 0) {
                // 1. Process class correspondances
                this.current_correspondance_type = 'classes';
                this.current_correspondance = this.correspondances['classes'].pop();
                this.$http.post('/api/conversation/question/class', this.current_correspondance).then(response => {
                    this.push_bot_message(response.body['text']);
                    this.awaiting_user = true;
                });
            } else if (this.correspondances['properties'].length > 0) {
                // 2. Process properties correspondances
                this.current_correspondance_type = 'properties';
                this.current_correspondance = this.correspondances['properties'].pop();
                this.$http.post('/api/conversation/question/property', this.current_correspondance).then(response => {
                    this.push_bot_message(response.body['text']);
                    this.awaiting_user = true;
                });
            } else if (this.confirmed_correspondances['classes'].length < 1) {
                // 3. Check if at least one class correspondance is confirmed
                this.$http.get('/api/conversation/error/no-classes').then(response => {
                    this.push_bot_message(response.body['text']);
                    this.is_finished = true;
                });
            } else {
                // 4. Return the rml mapping
                // compute client time
                this.client_time = Math.floor((Date.now() - this.client_time)/1000);
                // Sends fields metas along correspondance to log it
                this.confirmed_correspondances['fields'] = this.dataset_fields;
                this.confirmed_correspondances['server_time'] = this.server_time;
                this.confirmed_correspondances['client_time'] = this.client_time;
                this.awaiting_correspondances['fields'] = this.dataset_fields;
                this.denied_correspondances['fields'] = this.dataset_fields;
                this.$http.post('/api/' + this.dataset_id + '/correspondances/confirmed', this.confirmed_correspondances).then(response => {
                    this.$http.post('/api/' + this.dataset_id + '/correspondances/awaiting', this.awaiting_correspondances).then(response => {
                        this.$http.post('/api/' + this.dataset_id + '/correspondances/denied', this.denied_correspondances).then(response => {
                            this.$http.post('/api/' + this.dataset_id + '/correspondances/mapping', this.confirmed_correspondances).then(response => {
                                this.rml_mapping = response.body;
                                this.$http.get('/api/conversation/salutation').then(response => {
                                    this.push_bot_message(response.body['text']);
                                    this.is_finished = true;
                                    // switch selector
                                    this.hide_selectors();
                                    this.get_mapping_selector = true;
                                    $('#resultModal').modal(show = true);
                                    $('#rmlMapping').append(Prism.highlight(this.rml_mapping, Prism.languages.yaml));
                                });
                            });
                        });
                    });
                });
            }
        },
        /** Hides all selectors (for user interaction with bot) */
        hide_selectors: function () {
            this.yes_no_selector = false;
            this.class_selector = false;
            this.field_selector = false;
            this.get_mapping_selector = false;
        },
        /** Processes a positive response (Yes) from the user */
        user_input_yes: function () {
            if (this.awaiting_user) {
                this.awaiting_user = false;
                this.push_user_message("Yes.");
                if (this.current_correspondance_type === 'properties') {
                    this.$http.post('/api/conversation/question/property-class', this.current_correspondance).then(response => {
                        this.push_bot_message(response.body['text']);
                        //update selector
                        this.hide_selectors();
                        this.field_selector = true;
                        this.awaiting_user = true;
                    });
                } else {
                    // class correspondance
                    this.confirmed_correspondances['classes'].push(this.current_correspondance);
                    this.dataset_fields[this.current_correspondance['field_name']]['class'] = this.current_correspondance['class'];
                    this.update_class_suggestions(this.current_correspondance['class'], this.current_correspondance['field_name']);
                    update_graph(this.current_correspondance, this.current_correspondance_type);
                    setTimeout(function () {
                        chat.next_semantize()
                    }, 1000);
                }
            }
        },
        /** Processes a neutral response (I don't know) from the user */
        user_input_idk: function () {
            if (this.awaiting_user) {
                this.awaiting_user = false;
                this.push_user_message("I don't know.");
                this.awaiting_correspondances[this.current_correspondance_type].push(this.current_correspondance);
                setTimeout(function () {
                    chat.next_semantize()
                }, 1000);
            }
        },
        /** Processes a negative response (No) from the user */
        user_input_no: function () {
            if (this.awaiting_user) {
                this.awaiting_user = false;
                this.push_user_message("No.");
                this.denied_correspondances[this.current_correspondance_type].push(this.current_correspondance);
                setTimeout(function () {
                    chat.next_semantize()
                }, 1000);
            }
        },
        /**
         * Processes a class as a response from the user
         *
         * @param {{uri: String, class: String, description: String, sub: Array, eq: Array}} associated_class -
         * An accepted class correspondance that will be the domain of the current property correspondance.
         */
        user_input_property_class: function (associated_class) {
            if (this.awaiting_user) {
                if (associated_class == null) {
                    this.awaiting_user = false;
                    this.push_user_message('None of those');
                    this.current_correspondance['associated_class'] = [];
                    this.current_correspondance['associated_field'] = [];
                    this.denied_correspondances[this.current_correspondance_type].push(this.current_correspondance);
                    //update selector
                    this.hide_selectors();
                    this.yes_no_selector = true;
                    setTimeout(function () {
                        chat.next_semantize()
                    }, 1000);
                } else {
                    this.awaiting_user = false;
                    this.push_user_message(associated_class['class']);
                    this.current_correspondance['associated_class'] = associated_class['class'];
                    this.current_correspondance['associated_field'] = associated_class['field_name'];
                    this.confirmed_correspondances[this.current_correspondance_type].push(this.current_correspondance);
                    //update selector
                    this.hide_selectors();
                    this.yes_no_selector = true;
                    update_graph(this.current_correspondance, this.current_correspondance_type);
                    setTimeout(function () {
                        chat.next_semantize()
                    }, 1000);
                }
            }
        },
        /**
         * Processes a field of the dataset as a response from the user.
         * If property have a domain, selected field is converted as an accepted class correspondance
         * and become the domain of that property. Same for the range (but with the field that represents the property).
         *
         * @param {{value: String, data: String, class: String}} associated_field -
         * A field that will be the domain of the current property correspondance.
         */
        user_input_property_field: function (associated_field) {
            if (this.awaiting_user) {
                if (associated_field == null) {
                    this.awaiting_user = false;
                    this.push_user_message('None of those');
                    this.current_correspondance['associated_class'] = [];
                    this.current_correspondance['associated_field'] = [];
                    this.denied_correspondances[this.current_correspondance_type].push(this.current_correspondance);
                    //update selector
                    this.hide_selectors();
                    this.yes_no_selector = true;
                    setTimeout(function () {
                        chat.next_semantize()
                    }, 1000);
                } else {
                    this.awaiting_user = false;
                    this.push_user_message(associated_field.value);
                    // update domain and range class correspondances
                    this.current_correspondance['domain']['label'] = associated_field.value;
                    this.current_correspondance['domain']['field_name'] = associated_field.data;
                    if (this.current_correspondance['range']) {
                        this.current_correspondance['range']['label'] = this.current_correspondance['label'];
                        this.current_correspondance['range']['field_name'] = this.current_correspondance['field_name'];
                        this.confirmed_correspondances['classes'].push(this.current_correspondance['range']);
                        this.update_class_suggestions(this.current_correspondance['range']['class'], this.current_correspondance['range']['field_name']);
                        update_graph(this.current_correspondance['range'], 'classes');
                    }
                    this.current_correspondance['associated_class'] = this.current_correspondance['domain']['class'];
                    this.current_correspondance['associated_field'] = associated_field.data;
                    this.confirmed_correspondances['classes'].push(this.current_correspondance['domain']);
                    this.update_class_suggestions(this.current_correspondance['domain']['class'], this.current_correspondance['domain']['field_name']);
                    update_graph(this.current_correspondance['domain'], 'classes');
                    this.confirmed_correspondances[this.current_correspondance_type].push(this.current_correspondance);
                    //update selector
                    this.hide_selectors();
                    this.yes_no_selector = true;
                    update_graph(this.current_correspondance, this.current_correspondance_type);
                    setTimeout(function () {
                        chat.next_semantize();
                    }, 1000);
                }
            }
        },
        /** Shows the mapping modal */
        get_mapping_btn: function () {
            $('#resultModal').modal(show = true);
        },
        /**
         * Update a field suggestion in the suggestions array with its accepted class correspondance
         *
         * @param {String} clss - The class of the field
         *
         * @param {String} field_name - The field_name of the field
         */
        update_class_suggestions: function (clss, field_name) {
            for (i = 0; i < this.suggestions.length; i++) {
                if (this.suggestions[i]['data'] === field_name) {
                    if ((! this.suggestions[i]['class']) || (this.suggestions[i]['class'] === 'Thing')){
                        this.suggestions[i]['class'] = clss;
                    }
                }
            }
        },
    },
});

/** Executed when Enter Key (13) is pressed and field selector is shown */
$(function () {
    $('.Global-container').keypress(function (e) {
        if (chat.field_selector && e.which === 13) {
            if (chat.selected_field.data in chat.dataset_fields) {
                document.getElementById("fieldTextBar").classList.remove("is-invalid");
                chat.user_input_property_field(chat.selected_field);
                document.getElementById("fieldTextBar").value = '';
            } else {
                document.getElementById("fieldTextBar").classList.add("is-invalid");
            }
        }
    })
});

new ClipboardJS('.btn-rml', {
    container: document.getElementById('resultModal')
});


// -----------------------
// D3JS part for the graph
// -----------------------
let nodes = [];
let links = [];
let edgepaths;
let edgelabels;

let colors = d3.scaleOrdinal(d3.schemeCategory10);

let svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    node,
    link;

let simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {
        return d.id;
    }).distance(150).strength(1))
    .force("charge", d3.forceManyBody().strength(-25).distanceMax(100))
    .force("center", d3.forceCenter(0, 0));

update(links, nodes);

/**
 * Re-Instantiates the graph of the mapping
 *
 * @param {Array} links - All the links between nodes (properties/predicates)
 *
 * @param {Array} nodes - All the nodes of the graph (resources and values/subjects and objects)
 */
function update(links, nodes) {
    svg.selectAll("*").remove();

    svg.append('defs').append('marker')
        .attrs({
            'id': 'arrowhead',
            'viewBox': '-0 -5 10 10',
            'refX': function (d) {
                if (d) {
                    return d.target.radius;
                } else {
                    return node_init_radius;
                }
            },
            'refY': 0,
            'orient': 'auto',
            'markerWidth': 13,
            'markerHeight': 13,
            'xoverflow': 'visible'
        })
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', link_color)
        .style('stroke', 'none');

    link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr('marker-end', 'url(#arrowhead)')

    link.append("title")
        .text(function (d) {
            return d.type;
        });

    edgepaths = svg.selectAll(".edgepath")
        .data(links)
        .enter()
        .append('path')
        .attrs({
            'class': 'edgepath',
            'fill-opacity': 0,
            'stroke-opacity': 0,
            'id': function (d, i) {
                return 'edgepath' + i
            }
        })
        .style("pointer-events", "none");

    edgelabels = svg.selectAll(".edgelabel")
        .data(links)
        .enter()
        .append('text')
        .style("pointer-events", "none")
        .attrs({
            'class': 'edgelabel',
            'id': function (d, i) {
                return 'edgelabel' + i
            },
            'font-size': 12,
            'fill': link_color
        });

    edgelabels.append('textPath')
        .attr('xlink:href', function (d, i) {
            return '#edgepath' + i
        })
        .style("text-anchor", "middle")
        .attr("class", "noselect")
        .attr("startOffset", "50%")
        .text(function (d) {
            return d.label
        });

    node = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
        );

    node.append("circle")
        .attr("r", function (d) {
            return (d.radius);
        })
        .style("fill", function (d) {
            return (d.group === "resource") ? node_resource_color : node_value_color;
        });

    node.append("title")
        .text(function (d) {
            return d.id;
        });

    node.append("text")
        .attr("font-size", "10")
        .attr("class", "noselect")
        .attr("text-anchor", "middle")
        .attr("dy", 0)
        .append("tspan")
        .text(function (d) {
            return d.field_label;
        });
    node.select("text").append("tspan")
        .attr("x", "0")
        .attr("dy", "1em")
        .text(function (d) {
            return "(" + d.label + ")";
        });

    simulation
        .nodes(nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(links);
}

/** Controls the positions of the nodes, links and labels */
function ticked() {
    link
        .attr("x1", function (d) {
            return d.source.x;
        })
        .attr("y1", function (d) {
            return d.source.y;
        })
        .attr("x2", function (d) {
            return d.target.x;
        })
        .attr("y2", function (d) {
            return d.target.y;
        });
    node
        .attr("transform", function (d) {
            return "translate(" + d.x + ", " + d.y + ")";
        });

    edgepaths.attr('d', function (d) {
        return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
    });

    edgelabels.attr('transform', function (d) {
        if (d.target.x < d.source.x) {
            var bbox = this.getBBox();

            let rx = bbox.x + bbox.width / 2;
            let ry = bbox.y + bbox.height / 2;
            return 'rotate(180 ' + rx + ' ' + ry + ')';
        } else {
            return 'rotate(0)';
        }
    });
}

/** Enables drag and drop of nodes in the graph */
function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

/** Controls position of nodes when drag and drop action is finished*/
function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

/**
 * Adds a new class or property correspondance to nodes and links graph arrays
 *
 * @param {Object} correspondance - A class or property correspondance
 *
 * @param {String} correspondance_type - the type of the correspondance ('classes' or 'properties')
 */
function update_graph(correspondance, correspondance_type) {
    let existing_node_id = get_node_id(correspondance.field_name);
    if (correspondance_type === "classes") {
        if (existing_node_id) {
            // Update the class of the corresponding field
            if (! nodes[existing_node_id]['label'] || nodes[existing_node_id]['label'] === 'Thing') {
                nodes[existing_node_id]['label'] = correspondance.class;
            }
        }else {
            nodes.push({
                id: correspondance.field_name,
                field_name: correspondance.field_name,
                field_label: correspondance.label,
                label: correspondance.class,
                group: 'resource',
                radius : node_init_radius
            });
        }
    } else {
        if (existing_node_id == null || nodes[existing_node_id].id === correspondance.associated_field) {
            let id = correspondance.field_name + "_value";
            nodes.push({
                id: id,
                field_name: correspondance.field_name,
                field_label: correspondance.label,
                radius : node_init_radius,
                label: 'Dataset Field',
                group: 'value'
            });
            links.push({source: correspondance.associated_field, target: id, label: correspondance.description});
        } else {
            links.push({
                source: correspondance.associated_field,
                target: correspondance.field_name,
                label: correspondance.description
            });
        }
        // Node is growing proportionally to its number of predicates
        let source_node_id = get_node_id(correspondance.associated_field);
        nodes[source_node_id].radius += node_growing_factor;
    }
    update(links, nodes);
    simulation.alphaTarget(0.3).restart();
}

/**
 * Gets the index of the node corresponding to a specific field in the nodes array
 *
 * @param {String} field_name - the field_name of the field
 *
 * @returns {Number} - the index of the corresponding field in the nodes array
 */
function get_node_id(field_name) {
    for (i in nodes) {
        if (field_name === nodes[i].id) {
            return i;
        }
    }
    return null
}

let chart = $("#chart"),
    aspect = chart.width() / chart.height(),
    container = chart.parent();
$(window).on("resize", function () {
    var targetWidth = container.width();
    chart.attr("width", targetWidth);
    chart.attr("height", Math.round(targetWidth / aspect));
}).trigger("resize");