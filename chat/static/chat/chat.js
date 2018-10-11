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
    is_finished: false,
    rml_mapping: null
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
      chat.messages.push({
       text: message,
       type: 'bot'
      });
      setTimeout(scroll_chat_to_bottom, 100);
    },
    bot_introduction: function () {
      // Welcome messages
      this.$http.get('/api/conversation/greeting').then(response => {
        this.push_bot_message(response.body['text']);
        this.$http.get('/api/conversation/instructions').then(response => {
          this.push_bot_message(response.body['text']);
          // Retrieve all correspondances (classes and properties)
          this.$http.get('/api/'+ this.dataset_id +'/correspondances').then(response => {
            this.correspondances = response.body;
            this.next_semantize();
          },response => {
            this.$http.get('/api/conversation/error/lov-unavailable').then(response => {
              this.push_bot_message(response.body['text']);
              this.is_finished = true;
            });
          });
        });
      });
    },
    next_semantize: function () {
      // 1. Confirm class correspondances
      if (this.correspondances['classes'].length > 0) {
        this.current_correspondance_type = 'classes'
        this.current_correspondance = this.correspondances['classes'].pop();
        this.$http.post('/api/conversation/question/class', this.current_correspondance).then(response => {
          this.push_bot_message(response.body['text']);
          this.awaiting_user = true;
        });
      // 2. Confirm properties correspondances
      } else if (this.correspondances['properties'].length > 0) {
        this.current_correspondance_type = 'properties';
        if (this.confirmed_correspondances['classes'].length > 0){
          this.current_correspondance = this.correspondances['properties'].pop();
          this.$http.post('/api/conversation/question/property', this.current_correspondance).then(response => {
            this.push_bot_message(response.body['text']);
            this.awaiting_user = true;
          });
        } else {
          //There is no class to link properties with
          this.$http.get('/api/conversation/error/no-classes').then(response => {
            this.push_bot_message(response.body['text']);
            this.is_finished = true;
          });
        }
      // 3. Return the rml mapping
      } else {
        this.$http.post('/api/' + this.dataset_id +'/correspondances/confirmed', this.confirmed_correspondances).then(response => {
          this.$http.post('/api/' + this.dataset_id +'/correspondances/awaiting', this.awaiting_correspondances).then(response => {
            this.$http.post('/api/' + this.dataset_id +'/correspondances/denied', this.denied_correspondances).then(response => {
              this.$http.post('/api/' + this.dataset_id +'/correspondances/mapping', this.confirmed_correspondances).then(response => {
                this.rml_mapping = response.body
                this.$http.get('/api/conversation/salutation').then(response => {
                  this.push_bot_message(response.body['text']);
                  this.is_finished = true;
                });
              });
            });
          });
        });
      }
    },
    user_input_yes: function () {
      if (this.awaiting_user) {
        this.awaiting_user = false;
        this.push_user_message("Yes.");
        /*
        this.$http.get('/api/conversation/answer/positive').then(response => {
          this.push_bot_message(response.body['text']);
        */
          if ((this.current_correspondance_type == 'properties') && (this.confirmed_correspondances['classes'].length > 0)) {
            this.$http.post('/api/conversation/question/property-class', this.current_correspondance).then(response => {
              this.push_bot_message(response.body['text']);
              this.yes_no_questions = false;
              this.awaiting_user = true;
            });
          } else {
            this.confirmed_correspondances[this.current_correspondance_type].push(this.current_correspondance);
            update_graph(this.current_correspondance, this.current_correspondance_type);
            setTimeout(function(){chat.next_semantize()},1000);
          }
        /*
        })
        */
      }
    },
    user_input_idk: function () {
      if (this.awaiting_user) {
        this.awaiting_user = false;
        this.push_user_message("I don't know.");
        /*
        this.$http.get('/api/conversation/answer/neutral').then(response => {
          this.push_bot_message(response.body['text']);
        */
          this.awaiting_correspondances[this.current_correspondance_type].push(this.current_correspondance);
          setTimeout(function(){chat.next_semantize()},1000);
          /*
        });
        */
      }
    },
    user_input_no: function () {
      if (this.awaiting_user) {
        this.awaiting_user = false;
        this.push_user_message("No.");
        /*
        this.$http.get('/api/conversation/answer/negative').then(response => {
          this.push_bot_message(response.body['text']);
        */
          this.denied_correspondances[this.current_correspondance_type].push(this.current_correspondance);
          setTimeout(function(){chat.next_semantize()},1000);
        /*
        });
        */
      }
    },
    user_input_property_class: function (associated_class) {
      if ((this.awaiting_user) && (!this.yes_no_questions)) {
        if (associated_class == null){
          this.awaiting_user = false;
          this.push_user_message('None of those');
          /*
          this.$http.get('/api/conversation/answer/negative').then(response => {
            this.push_bot_message(response.body['text']);
          */
            this.current_correspondance['associated_class'] = [];
            this.current_correspondance['associated_field'] = [];
            this.denied_correspondances[this.current_correspondance_type].push(this.current_correspondance);
            this.yes_no_questions = true;
            setTimeout(function(){chat.next_semantize()},1000);
          /*
          });
          */
        } else {
          this.awaiting_user = false;
          this.push_user_message(associated_class['class']);
          /*
          this.$http.get('/api/conversation/answer/positive').then(response => {
            this.push_bot_message(response.body['text']);
          */
            this.current_correspondance['associated_class'] = associated_class['class'];
            this.current_correspondance['associated_field'] = associated_class['field_name'];
            this.confirmed_correspondances[this.current_correspondance_type].push(this.current_correspondance);
            this.yes_no_questions = true;
            update_graph(this.current_correspondance, this.current_correspondance_type);
            setTimeout(function(){chat.next_semantize()},1000);
          /*
          });
          */
        }
      }
    },
  },
});

// D3JS part for the graph
var nodes = [];
var links = [];

var colors = d3.scaleOrdinal(d3.schemeCategory10);

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    node,
    link;

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {return d.id;}).distance(150).strength(1))
    .force("charge", d3.forceManyBody().strength(-25).distanceMax(100))
    .force("center", d3.forceCenter(0, 0));

update(links, nodes);

function update(links, nodes) {
    svg.selectAll("*").remove();

    svg.append('defs').append('marker')
        .attrs({'id':'arrowhead',
            'viewBox':'-0 -5 10 10',
            'refX':30,
            'refY':0,
            'orient':'auto',
            'markerWidth':13,
            'markerHeight':13,
            'xoverflow':'visible'})
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke','none');

    link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr('marker-end','url(#arrowhead)')

    link.append("title")
        .text(function (d) {return d.type;});

    edgepaths = svg.selectAll(".edgepath")
        .data(links)
        .enter()
        .append('path')
        .attrs({
            'class': 'edgepath',
            'fill-opacity': 0,
            'stroke-opacity': 0,
            'id': function (d, i) {return 'edgepath' + i}
        })
        .style("pointer-events", "none");

    edgelabels = svg.selectAll(".edgelabel")
        .data(links)
        .enter()
        .append('text')
        .style("pointer-events", "none")
        .attrs({
            'class': 'edgelabel',
            'id': function (d, i) {return 'edgelabel' + i},
            'font-size': 12,
            'fill': '#aaa'
        });

    edgelabels.append('textPath')
        .attr('xlink:href', function (d, i) {return '#edgepath' + i})
        .style("text-anchor", "middle")
        .attr("class", "noselect")
        .attr("startOffset", "50%")
        .text(function (d) {return d.label});

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
        .attr("r", 30)
        .style("fill", function(d) { return (d.group == "resource") ? "#007fa4" : "#E8E8E8"; })

    node.append("title")
        .text(function (d) {return d.id;});

    node.append("text")
        .attr("font-size","10")
        .attr("class", "noselect")
        .attr("text-anchor", "middle")
        .attr("dy", 0)
        .append("tspan")
          .text(function (d) {return d.label;});
    node.select("text").append("tspan")
      .attr("x", "0")
      .attr("dy", "1em")
      .text(function (d) {return "(" + d.field_name + ")";});

    simulation
        .nodes(nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(links);
}

function ticked() {
    link
        .attr("x1", function (d) {return d.source.x;})
        .attr("y1", function (d) {return d.source.y;})
        .attr("x2", function (d) {return d.target.x;})
        .attr("y2", function (d) {return d.target.y;});

    node
        .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});

    edgepaths.attr('d', function (d) {
        return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
    });

    edgelabels.attr('transform', function (d) {
        if (d.target.x < d.source.x) {
            var bbox = this.getBBox();

            rx = bbox.x + bbox.width / 2;
            ry = bbox.y + bbox.height / 2;
            return 'rotate(180 ' + rx + ' ' + ry + ')';
        }
        else {
            return 'rotate(0)';
        }
    });
}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart()
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function update_graph(correspondance, correspondance_type){
  if (correspondance_type == "classes"){
    nodes.push({id: correspondance.field_name, field_name: correspondance.field_name, label: correspondance.class, group: 'resource'});
  } else {
    existing_node = get_node_id(correspondance.field_name, correspondance);
    if (existing_node == null){
      id = correspondance.field_name + "_value"
      nodes.push({id: id, field_name: correspondance.field_name, label: 'Dataset Field', group: 'value'});
      links.push({source: correspondance.associated_field, target: id, label: correspondance.description})
    } else {
      links.push({source: correspondance.associated_field, target: existing_node, label: correspondance.description})
    }
  }
  update(links, nodes);
  simulation.alphaTarget(0.3).restart();
}

function get_node_id(field_name, correspondance){
  for (i in nodes){
    if (field_name == nodes[i].id) {
      if (nodes[i].id != correspondance.associated_field){
        return nodes[i].id;
      }
    }
  }
  return null
}

var chart = $("#chart"),
  aspect = chart.width() / chart.height(),
  container = chart.parent();
$(window).on("resize", function() {
  var targetWidth = container.width();
  chart.attr("width", targetWidth);
  chart.attr("height", Math.round(targetWidth / aspect));
}).trigger("resize");
