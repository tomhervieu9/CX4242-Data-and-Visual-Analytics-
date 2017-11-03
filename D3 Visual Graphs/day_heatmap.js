var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 1000 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

var x = d3.scale.linear( )
    .domain([0,7])
    .rangeRound([0, width]);

var y = d3.scale.linear()
    .domain([0, 400])
    .rangeRound([height, 0]);

var z = d3.scale.linear()
    .domain([0, 150])
    .range(["white", "green"])
    .interpolate(d3.interpolateLab);
        
var week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickPadding(5) 
    .tickFormat(function(d) {return week[d];} );

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickFormat(d3.format("d"));

var svg2 = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json("day_heatmap.json", function(error, data) {

  var glucose = svg2.selectAll(".glucose")
      .data(data)
      .enter( ).append("g")
      .attr("class", "glucose");
      
  glucose.selectAll(".bin")
      .data(function (d) { return d.values; })
      .enter( ).append("rect")
      .attr("class", "bin")
      .attr("x", function (d, i) { return x(i); })
      .attr("width", function (d, i) { return  x(i+1) - x(i); })
      .style("fill", function(d) { return z(d); });
  glucose.each(function (d) {
    d3.select(this).selectAll(".bin")
        .attr("y", y(d.key) )
        .attr("height", 11 );
  });

  svg2.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg2.append("g")
      .attr("class", "y axis")
      .call(yAxis);
});
