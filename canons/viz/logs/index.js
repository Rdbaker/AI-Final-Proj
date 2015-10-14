$(document).ready(function() {
  logs = {};
  // a cumulative weight counter grouped by the thesaurus
  cumuSeries = {};
  // a weight counter grouped by the iteration
  seriesByIteration = [];
  [
    'logs/altervista.json',
    'logs/bighugelabs.json',
    'logs/stands4.json',
    'logs/watson.json',
    'logs/wordnet.json'
  ].forEach(function(elt, ind) {
    $.getJSON(elt, function(data) {
      // initialize the seriesByIteration data
      if(ind == 0) {
        for(var i=0; i < data.length; i++) {
          seriesByIteration.push({});
        }
      }
      var name = elt.split('/')[1].split('.')[0];
      logs[name] = data;
      // make the iteration distribution data
      var thes_total = 0;
      for(var i=0; i < seriesByIteration.length; i++) {
        seriesByIteration[i][name] = data[i].value + thes_total;
        thes_total += data[i].value;
      }
      if(Object.keys(logs).length === 5) {
        createNormalizedChart();

        for(var log in logs) {
          // make the cumulative series data
          cumuSeries[log] = logs[log].map(function(elt, ind, arr) { return _.sum(arr.map(function(e,i,a){ return e.value; }).slice(0, ind)) });
        }
        makeLineGraph();
      }
    });
  });

  function createNormalizedChart() {
    var margin = {top: 20, right: 100, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .rangeRound([height, 0]);

    var color = d3.scale.ordinal()
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56"]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(d3.format(".0%"));

    var svg = d3.select("#normalized-stacked-bar").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    color.domain(d3.keys(logs));

    // something here in the forEach loop
    seriesByIteration.forEach(function(iteration) {
      var y0 = 0;
      iteration.logs = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +iteration[name]}; });
      iteration.logs.forEach(function(elt) { elt.y0 /= y0; elt.y1 /= y0; });
    });

    x.domain(_.range(logs['wordnet'].length));

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    var iteration = svg.selectAll(".iteration")
        .data(seriesByIteration)
      .enter().append("g")
        .attr("class", "iteration")
        .attr("transform", function(d, i) { return "translate(" + x(i) + ",0)"; });

    iteration.selectAll("rect")
        .data(function(d) { return d.logs; })
      .enter().append("rect")
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .style("fill", function(d) { return color(d.name); });

    var legend = svg.select(".iteration:last-child").selectAll(".legend")
        .data(function(d) { return d.logs; })
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d) { return "translate(" + x.rangeBand() / 2 + "," + y((d.y0 + d.y1) / 2) + ")"; });

    legend.append("line")
        .attr("x2", 45);

    legend.append("text")
        .attr("x", 50)
        .attr("dy", ".35em")
        .text(function(d) { return d.name; });

  }


  function makeLineGraph() {
    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 80, bottom: 30, left: 50},
        width = 700 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;

    // Set the ranges
    var x = d3.scale.linear().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    var color = d3.scale.category10();

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return x(d.iteration); })
        .y(function(d) { return y(d.value); });

    var svg = d3.select("#line-series").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    color.domain(d3.keys(cumuSeries));

    var thesauri = color.domain().map(function(thes) {
      return {
        name: thes,
        values: cumuSeries[thes].map(function(elt, ind) {
          return {
            iteration: ind,
            value: elt
          }
        })
      };
    });

    x.domain([0, cumuSeries['stands4'].length]);
    y.domain([0, _.max(_.flatten(_.values(cumuSeries)))]);

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Preference");

    var thesaurus = svg.selectAll(".thesaurus")
        .data(thesauri)
      .enter().append("g")
        .attr("class", "thesaurus");

    thesaurus.append("path")
      .attr("class", "line")
      .attr("d", function(d) {return line(d.values)})
      .style("stroke", function(d) { return color(d.name); });

    thesaurus.append("text")
        .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
        .attr("transform", function(d) { return "translate(" + x(d.value.iteration) + "," + y(d.value.value) + ")"; })
        .attr("x", 3)
        .attr("dy", ".35em")
        .text(function(d) { return d.name; });
  }

});
