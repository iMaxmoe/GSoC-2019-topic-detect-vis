/*Draw the lollipop plot*/
// set the dimensions and margins of the graph
var margin = {
        top: 10,
        right: 30,
        bottom: 40,
        left: 100
    },
    width = 460 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var lollipop = d3.select("#top10")
    .append("svg")
    .attr("id", "lollipop")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

function drawLollipop(dataSource) {
    // Parse the Data
    d3.json(dataSource, function(data) {

        data = data.persons;
        //console.log(data);

        // Add X axis
        var x = d3.scaleLinear()
            .domain([0, 400])
            .range([0, width]);
        lollipop.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-45)")
            .style("text-anchor", "end");

        // Y axis
        var y = d3.scaleBand()
            .range([0, height])
            .domain(data.slice(0, 10).map(function(d) {
                return d.key;
            }))
            .padding(1);
        lollipop.append("g")
            .call(d3.axisLeft(y))

        // Lines
        lollipop.selectAll("myline")
            .data(data.slice(0, 10))
            .enter()
            .append("line")
            .attr("x1", function(d) {
                return x(d.count);
            })
            .attr("x2", x(0))
            .attr("y1", function(d) {
                return y(d.key);
            })
            .attr("y2", function(d) {
                return y(d.key);
            })
            .attr("stroke", "grey")

        // Circles
        lollipop.selectAll("mycircle")
            .data(data.slice(0, 10))
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                return x(d.count);
            })
            .attr("cy", function(d) {
                return y(d.key);
            })
            .attr("r", "7")
            .style("fill", "#69b3a2")
            .attr("stroke", "black")
    });
}

function changeDateLollipop(date) {
    lollipop.selectAll("*").remove();
    let filePath = "./json/" + date + ".json";
    drawLollipop(filePath);
    //drawWordcloud(filePath);
}

changeDateLollipop("2019-06-01");