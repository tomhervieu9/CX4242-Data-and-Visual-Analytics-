    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 1000 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    var sqrtx = d3.scale.sqrt()
        .range([0, width]); 

    var sqrty = d3.scale.sqrt()
        .range([height, 0]);

    var color = d3.scale.category10();

    var sqrtxAxis = d3.svg.axis()
        .scale(sqrtx)
        .orient("bottom");

    var sqrtyAxis = d3.svg.axis()
        .scale(sqrty)
        .orient("left");
        
    var svg5 = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.tsv("iris.tsv", function(error, data) {
      if (error) throw error;

      sqrtx.domain([4,8]);
      sqrty.domain([1.5,5]);

      svg5.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(sqrtxAxis)
          .append("text")
					.text("Sepal Length (cm)")
          .attr("class", "label")
          .attr("x", width)
          .style("font-size", "14px")
          .attr("y", -6)
          .style("text-anchor", "end");

      svg5.append("g")
          .attr("class", "y axis")
          .call(sqrtyAxis)
          .append("text")
					.text("Sepal Width (cm)")
          .style("font-size", "14px")
          .attr("class", "label")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end");
          
          
          
        sDict = {"setosa": "red", "versicolor": "blue", "virginica": "green"};
        
        svg5.selectAll(".point")
          .data(data)
          .enter().append("path")
          .attr("class", "point")
          .attr("r", 3.5)
          .attr("transform", function(d) { 
            return "translate(" + sqrtx(d.sepalLength) + "," +  sqrty(d.sepalWidth) + ")";})
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

          
          
      var legend = svg5.selectAll(".legend")
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