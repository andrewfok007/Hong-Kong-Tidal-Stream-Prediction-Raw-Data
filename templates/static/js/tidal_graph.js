function update_chart(data) {
    $("#visualisation").html("");

    var vis = d3.select("#visualisation"),
        width = 1100,
        height = 550,
        margin = {
            top: 50,
            right: 20,
            bottom: 20,
            left: 50
        },
        xmax = d3.max(data, function(d) {return d.prediction_interval;}),
        ymax = d3.max(data, function(d) {return d.knots;}),
        ymax2 = d3.max(data, function(d) {return knots_to_power(d.knots);}),
        xScale = d3.scale.linear().range([margin.left, width]).domain([0, xmax]),
        yScale = d3.scale.linear().range([height, 0]).domain([0, ymax]),
        y2Scale = d3.scale.linear().range([height, 0]).domain([0, ymax2]),
        xAxis = d3.svg.axis().scale(xScale).orient("bottom"),
        yAxisLeft = d3.svg.axis().scale(yScale).orient("left"),
        yAxisRight = d3.svg.axis().scale(y2Scale).orient("right");

    var lineGen = d3.svg.line()
        .x(function(d) { return xScale(d.prediction_interval); })
        .y(function(d) { return yScale(d.knots); })

    var lineGen2 = d3.svg.line()
        .x(function(d) { return xScale(d.prediction_interval); })
        .y(function(d) {
            return y2Scale(knots_to_power(d.knots));
        })

    vis.append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", 
                  "translate(" + margin.left + "," + margin.top + ")");

    sub_data = []
    for (var i = 0; i < data.length; i++){
        if(data[i].prediction_interval%4 == 0 || data[i].prediction_interval == 1){
            temp = data[i];
            sub_data.push(temp);
        }
    }

    vis.append('path')
        .attr('d', lineGen(sub_data))
        .attr('stroke', 'steelblue')
        .attr('fill', 'none');

    vis.append('path')
        .attr('d', lineGen2(sub_data))
        .attr('stroke', 'red')
        .attr('fill', 'none');

    vis.append("g")            // Add the X Axis
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    vis.append("g")
        .attr("class", "y axis")
        .style("fill", "steelblue")
        .attr("transform", "translate(" + margin.left + " ,0)")  
        .call(yAxisLeft);

    vis.append("g")             
        .attr("class", "y axis")    
        .attr("transform", "translate(" + width + " ,0)")   
        .style("fill", "red")       
        .call(yAxisRight);
        // .text("Power Generation (kW)");

    vis.append("text")      // text label for the x axis
        .attr("x", 550 )
        .attr("y",  590 )
        .style("text-anchor", "middle")
        .text("Time Intervals");

    vis.append("text")      // text label for the x axis
        .attr("x", 120 )
        .attr("y",  10 )
        .style("fill", "steelblue")
        .style("text-anchor", "middle")
        .text("Tidal Flow (Knots)");

    vis.append("text")      // text label for the x axis
        .attr("x", 1000 )
        .attr("y",  10 )
        .style("fill", "red")
        .style("text-anchor", "middle")
        .text("Power Generation (kW)");
}