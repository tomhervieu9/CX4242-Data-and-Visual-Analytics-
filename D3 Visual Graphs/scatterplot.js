    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 1000 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .range([0, width]); 

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.category10();
    
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");
        
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.tsv("iris.tsv", function(error, data) {
      if (error) throw error;
	  
      x.domain([4,8]);
      y.domain([1,5]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
					.append("text")
					.text("Sepal Length (cm)")
          .attr("class", "label")
          .attr("x", width)
          .style("font-size", "14px")
          .attr("y", -6)
          .style("text-anchor", "end");
          

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
          .append("text")
					.text("Sepal Width (cm)")
          .style("font-size", "14px")
          .attr("class", "label")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end");
          
          
        sDict = {"setosa": "red", "versicolor": "blue", "virginica": "green"};
        
        svg.selectAll(".point")
          .data(data)
          .enter().append("path")
          .attr("class", "point")
          .attr("r", 3.5)
          .attr("transform", function(d) { 
            return "translate(" + x(d.sepalLength) + "," +  y(d.sepalWidth) + ")";})
          .attr("d", d3.svg.symbol().type(function(d) {
            if (d.species == "setosa") {
                return "circle";
            }
            if (d.species == "versicolor") {
                return "square";
            }
            if (d.species == "virginica") {
                return "triangle-up";
            }
            }))
          .style("stroke", function(d) { return sDict[d.species]; })
          .style("fill", "none")
          .style("stroke-width", "1.7");
          

          
      var legend = svg.selectAll(".legend")
          .data(Object.keys(sDict))
          .enter().append("g")
          .attr("class", ".legend")
          .attr("transform", function(d, i) { return "translate(0," + i * 22 + ")"; });
      
      
      legend.append("path")
          .attr("d", d3.svg.symbol().type(function(d) {
            if (d == "setosa") {
                return "circle";
            }
            if (d == "versicolor") {
                return "square";
            }
            if (d == "virginica") {
                return "triangle-up";
            }
          }))
          .style("stroke", function(d) { return sDict[d]; })
          .style("fill", "none")
          .style("stroke-width", "1.7")
          .attr("transform", function(d, i) { return "translate(" + width + ",12)"; });
          

      legend.append("text")
          .attr("x", width - 20)
          .attr("y", 12)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(function(d) { return d; });

    });