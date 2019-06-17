// @TODO: YOUR CODE HERE!

// set margins
var svgWidth = 800;
var svgHeight = 500;

var margin = {
    top: 20,
    right: 40,
    bottom: 60,
    left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// append svg and group
var svg = d3.select("#scatter")
    .append("svg")
    .attr("height", svgHeight)
    .attr("width", svgWidth);

var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// load data
d3.csv("assets/data/data.csv", function(error, data) {
    if(error) throw error;

    //parse data
    data.forEach(function(d) {
        d.poverty = +d.poverty;
        d.healthcare = +d.healthcare;
    });

// setup x
var xValue = function(d) { return d.poverty;},
    xLinearScale = d3.scaleLinear().range([0, width]),
    xMap = function(d) { return xLinearScale(xValue(d));},
    xAxis = d3.axisBottom(xLinearScale);

// setup y
var yValue = function(d) { return d.healthcare;},
    yLinearScale = d3.scaleLinear().range([height, 0]),
    yMap = function(d) {return yLinearScale(yValue(d));},
    yAxis = d3.axisLeft(yLinearScale);

// setup toolTip
var toolTip = d3.tip()
    .attr("class", "d3-tip")
    .html(function(d) { return d["state"] + "<br> Poverty: " + xValue(d) + "% <br> Lacks Healthcare: " + yValue(d) + "%"});

xLinearScale.domain([d3.min(data, xValue)-1, d3.max(data, xValue)+1]);
yLinearScale.domain([d3.min(data, yValue)-1, d3.max(data, yValue)+1]);

chartGroup.call(toolTip);

// append x
chartGroup.append("g")
    .classed("x-axis", true)
    .attr("transform", `translate(0, ${height})`)
    .call(xAxis)

// append y
 chartGroup.append("g")
    .classed("y-axis", true)
    .attr("transform", "translate(0)")
    .call(yAxis)

// x and y axis title
chartGroup.append("text")
    .attr("y", (margin.bottom + height))
    .attr("x", (width / 2))
    .text("In Poverty (%)");

chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", 0-(height/2))
    .attr("y", 0-margin.left+40)
    .text("Lacks Healthcare (%)");

// create dots
chartGroup.selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("class", "bubble")
    .attr("cx", xMap)
    .attr("cy", yMap)
    .attr("r", 10)
    .style("fill", "blue")
    .style("opacity", ".5")
    .on("mouseover", toolTip.show)
    .on("mouseout", toolTip.hide);

// label data points with state abbreviations
chartGroup.selectAll("bubble")
    .data(data)
    .enter()
    .append("text")
    .text(function(d){return d.abbr;})
    .attr("x", xMap)
    .attr("y", yMap)
    .attr("font-family", "courier")
    .attr("font-size", "8px")
    .attr("fill", "white")
    .attr("text-anchor", "middle");

});

