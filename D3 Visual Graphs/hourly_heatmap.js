var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 1000 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

var hx = d3.scale.linear( )
    .domain([0, 23])
    .rangeRound([0 , width]);

var hy = d3.scale.linear()
    .domain([0, 400])
    .rangeRound([height, 0]);

var hz = d3.scale.linear()
    .domain([0, 100])
    .range(["white", "green"])
    .interpolate(d3.interpolateLab);

var formatTime = d3.time.format("%I %p"),
    formatHour = function (d) {
        return formatTime(new Date(2013, 2, 9, d, 00));
    };

var hxAxis = d3.svg.axis()
    .scale(hx)
    .orient("bottom")
    .ticks(24)
    .tickFormat(formatHour);

var hyAxis = d3.svg.axis()
    .scale(hy)
    .orient("left")
    .tickFormat(d3.format("d"));

var hsvg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json("hourly_heatmap.json", function(error, data) {

  var hglucose = hsvg.selectAll(".glucose")
      .data(data)
      .enter( ).append("g")
      .attr("class", "glucose");
      
  hglucose.selectAll(".bin")
      .data(function (d) {
          return d.values;
      })
      .enter( ).append("rect")
      .attr("class", "bin")
      .attr("x", function (d, i) {
          return hx(i);
      })
      .attr("width", function (d, i) {
          return  hx(i+1) - hx(i);
      })
      .style("fill", function(d) {
          return hz(d);
      });
  
  hglucose.each(function (d) {
    d3.select(this).selectAll(".bin")
        .attr("y", hy(d.key) )
        .attr("height", 11 );
  });

  hsvg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(hxAxis);

  hsvg.append("g")
      .attr("class", "y axis")
      .call(hyAxis);
});
