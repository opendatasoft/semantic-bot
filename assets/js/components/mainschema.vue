<template>
    <div class="mainschema animated fadeIn" v-bind:class="{ 'graphstarted': graphstarted}" v-show="appstarted && !switchmainapp">
        <mainheaderapp></mainheaderapp>
        <div class="innerapp">
            <div class="schema">
                <div class="graph" id="graph">
                    <svg id="mapping_graph" width="600" height="600"
                         viewBox="-300 -300 600 600">
                    </svg>
                </div>
            </div>
            <div class="mainfooter">
                <ul>
                    <li>
                        LEGEND:
                    </li>
                    <li>
                        <img src="static/img/legend_resource.svg" />
                        Resource
                    </li>
                    <li>
                        <img src="static/img/legend_literal.svg" />
                        Literal
                    </li>
                    <li>
                        <img src="static/img/legend_property.svg" />
                        Property
                    </li>
                </ul>
        </div>
        </div>

    </div>
</template>

<script>

import Mainheaderapp from "./mainheader.vue";
import * as d3 from 'd3';
import {attrs} from "d3-selection-multi";

export default {
    name: 'Mainschema',
    components: {
        Mainheaderapp
    },
    data: function () {
        return {
            appstarted: false,
            switchmainapp: false,
            graphstarted: false,
        }
    },
    mounted: function () { 
        this.$root.$on('appstartedEvent', (appstartedstate) => { 
            this.appstarted = appstartedstate;
        });
        this.$root.$on('switchmainappEvent', (switchmainappstate) => { 
            this.switchmainapp = switchmainappstate;
        });
        this.$root.$on('newConfirmedCorrespondance', (confirmed_correspondances) => {
            if (!this.graphstarted) {
                this.graphstarted = true;
                simulation = d3.forceSimulation()
                    .force("link", d3.forceLink().id(function (d) {
                        return d.id;
                    }).distance(200).strength(1))
                    .force("charge", d3.forceManyBody().strength(-50).distanceMax(100))
                    .force("center", d3.forceCenter(0, 0));

                svg = d3.select("svg");
                width = +svg.attr("width");
                height = +svg.attr("height");

                chart = $("#chart");
                aspect = chart.width() / chart.height();
                container = chart.parent();
                $(window).on("resize", function () {
                    let targetWidth = container.width();
                    chart.attr("width", targetWidth);
                    chart.attr("height", Math.round(targetWidth / aspect));
                }).trigger("resize");
            }
            this.draw_graph(confirmed_correspondances);
        });
    },
    methods: {
        /** Updates links and nodes arrays according to confirmed correspondances */
        draw_graph: function (confirmed_correspondances) {
            confirmed_correspondances.classes.forEach( correspondance => {
                let existing_node_id = get_node_id(correspondance.field_name);
                if (existing_node_id) {
                    // Update the class of the corresponding field
                    if (!nodes[existing_node_id]['label'] || nodes[existing_node_id]['label'] === 'Thing') {
                        nodes[existing_node_id]['label'] = correspondance.class;
                    }
                } else {
                    nodes.push({
                        id: correspondance.field_name,
                        field_name: correspondance.field_name,
                        field_label: correspondance.label,
                        label: correspondance.class,
                        group: 'resource',
                        width: node_init_width,
                        height: node_init_height
                    });
                }
            });
            confirmed_correspondances.properties.forEach( correspondance => {
                let existing_node_id = get_node_id(correspondance.field_name);
                if (existing_node_id == null || nodes[existing_node_id].id === correspondance.associated_field) {
                    let id = correspondance.field_name + "_value";
                    if (!get_node_id(id)) {
                        nodes.push({
                            id: id,
                            field_name: correspondance.field_name,
                            field_label: correspondance.label,
                            width: node_init_width,
                            height: node_init_height,
                            label: 'Dataset Field',
                            group: 'value'
                        });
                    }
                    links.push({source: correspondance.associated_field, target: id, label: correspondance.description});
                } else {
                    links.push({
                        source: correspondance.associated_field,
                        target: correspondance.field_name,
                        label: correspondance.description
                    });
                }
            });
            update(links, nodes);
            simulation.alphaTarget(0.3).restart();
        }
    }
}

const node_init_width = 100;
const node_init_height = 70;

// -----------------------
// D3JS part for the graph
// -----------------------
let nodes = [];
let links = [];
let simulation = null;
let svg = null;
let edgepaths;
let edgelabels;
let width;
let height;
let node;
let link;
let chart;
let aspect;
let container;
let marker;

/**
 * Re-Instantiates the graph of the mapping
 *
 * @param {Array} links - All the links between nodes (properties/predicates)
 *
 * @param {Array} nodes - All the nodes of the graph (resources and values/subjects and objects)
 */
function update(links, nodes) {
    svg.selectAll("*").remove();

    marker = svg.append('defs').append('marker')
        .attrs({
            'id': 'arrowhead',
            'class': 'arrowhead',
            'viewBox': '0 0 10 10',
            'refX': function (d) {
                if (d) {
                    return d.target.radius;
                } else {
                    return 0;
                }
            },
            'refY': 0,
            'orient': 'auto',
            'markerWidth': 13,
            'markerHeight': 13,
            'xoverflow': 'visible'
        })
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5');

    link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr('marker-end', 'url(#arrowhead)');

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
        });

    edgelabels = svg.selectAll(".edgelabel")
        .data(links)
        .enter()
        .append('text')
        .attrs({
            'class': 'edgelabel',
            'id': function (d, i) {
                return 'edgelabel' + i
            },
        });

    edgelabels.append('textPath')
        .attr('xlink:href', function (d, i) {
            return '#edgepath' + i
        })
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
            .on("end", dragended)
        );

    node.append("rect")
        .attr("width", function (d) {
            return (d.width);
        })
        .attr("height", function (d) {
            return (d.height);
        })
        .attr("rx", function (d) {
            return (d.group === "resource") ? 31 : 0;
        })
        .attr("ry", function (d) {
            return (d.group === "resource") ? 31 : 0;
        })
        .attr("class", function (d) {
            return (d.group === "resource") ? 'node-resource' : 'node-value';
        });

    node.append("title")
        .text(function (d) {
            return d.id;
        });

    node.append("text")
        .attr("class", function (d) {
            return (d.group === "resource") ? 'node-text-resource' : 'node-text-value';
        })
        .attr("dx", node_init_width/2)
        .attr("dy", node_init_height/2 - 1)
        .append("tspan")
        .text(function (d) {
            return d.field_label;
        });

    node.select("text").append("tspan")
        .attr("class", function (d) {
            return (d.group === "resource") ? 'node-text-under-resource' : 'node-text-under-value';
        })
        .attr("x", node_init_width/2)
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
            return d.source.x + (node_init_width/2);
        })
        .attr("y1", function (d) {
            return d.source.y + (node_init_height/2);
        })
        .attr("x2", function (d) {
            return d.target.x + (node_init_width/2);
        })
        .attr("y2", function (d) {
            return d.target.y + (node_init_height/2);
        });
    node
        .attr("transform", function (d) {
            return "translate(" + d.x + ", " + d.y + ")";
        });

    edgepaths.attr('d', function (d) {
        return 'M ' + (d.source.x + (node_init_width/2)) + ' ' + (d.source.y + (node_init_height/2)) + ' L ' + (d.target.x + (node_init_width/2)) + ' ' + (d.target.y + (node_init_height/2));
    });

    edgelabels.attr('transform', function (d) {
        if (d.target.x < d.source.x) {
            let bbox = this.getBBox();

            let rx = bbox.x + bbox.width / 2;
            let ry = bbox.y + bbox.height / 2;
            return 'rotate(180 ' + rx + ' ' + ry + ')';
        } else {
            return 'rotate(0)';
        }
    });

    marker.attr('refX',  function (d) {
        return 0; //TODO compute the distance of the marker from the target node center
    });


}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

/**
 * Gets the index of the node corresponding to a specific field in the nodes array
 *
 * @param {String} field_name - the field_name of the field
 *
 * @returns {Number} - the index of the corresponding field in the nodes array
 */
function get_node_id(field_name) {
    for (let i in nodes) {
        if (field_name === nodes[i].id) {
            return i;
        }
    }
    return null
}

</script>

<style lang="scss">

</style>
