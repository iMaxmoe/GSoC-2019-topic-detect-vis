let date = "2019-06-01"; // default date
var filePath = "./json/" + date + ".json";

var cloud = d3.layout.cloud()
    .size([500, 500])

function drawWordcloud(dataSource, type) {
    /* type: \n
        "name" : person name cloud \n
        "occupation": occupation cloud */

    d3.json(dataSource, function(data) {

        var entity;

        if (type == "name") {
            entity = data.persons;
            var wordScale = d3.scaleLinear().domain([1, 10, 100, 500]).range([10, 20, 40, 80]).clamp(true);
            var wordColor = d3.scaleLinear().domain([10, 20, 40, 80]).range(["blue", "green", "orange", "red"]);
        } else {
            entity = data.occupations;
            var wordScale = d3.scaleLinear().domain([1, 4, 16, 64]).range([10, 20, 40, 80]).clamp(true);
            var wordColor = d3.scaleLinear().domain([10, 20, 40, 80]).range(["blue", "green", "orange", "red"]);
        }

        // Number of words to be included in the word cloud
        var num = entity.length < 100 ? entity.length : 100;

        entity = entity.slice(0, num);

        cloud.words(entity.map(function(d) {
                return { text: d.key, size: wordScale(parseInt(d.count)) }
            }))
            .padding(5)
            .font("Impact")
            .fontSize(function(d) { return d.size; })
            .on("end", draw);

        cloud.start();

        function draw(words) {
            d3.select("#wordcloud").append("svg")
                .attr("width", cloud.size()[0])
                .attr("height", cloud.size()[1])
                .append("g")
                .attr("transform", "translate(" + cloud.size()[0] / 2 + "," + cloud.size()[1] / 2 + ")")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.size + "px"; })
                .style("font-family", "Impact")
                .style("fill", function(d) { return wordColor(d.size); })
                .attr("text-anchor", "middle")
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.text; });
        }
    })
}

// Response to the selection list
function changeDateWordcloud(date) {
    d3.select("#wordcloud").selectAll("*").remove();
    filePath = "./json/" + date + ".json";

    // Recover the radio buttons
    var btns = d3.select("#name")
        .attr("checked", "checked");

    drawWordcloud(filePath, "name");
}


// Switch between occupation cloud and name cloud
function switchCloud(type) {
    d3.select("#canvas").selectAll("*").remove();
    drawWordcloud(filePath, type);
}

var btns = document.getElementsByName("typeOfCloud");
var prev = null;

for (btn of btns) {
    btn.addEventListener('change', function() {
        if (this !== prev) {
            switchCloud(this.id);
            prev = this;
        }
    });
}


function drawHeatmap(dataSource) {

    // set the dimensions and margins of the graph
    var margin = {
            top: 30,
            right: 30,
            bottom: 150,
            left: 150
        },
        width = 600 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#heatmap")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    //Read the data
    d3.json(dataSource, function(data) {

        var myGroups = data.pairX,
            myVars = data.pairY;

        // Build X scales and axis:
        var x = d3.scaleBand()
            .range([0, width])
            .domain(myGroups)
            .padding(0.01);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        svg.selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(90)")
            .style("text-anchor", "start");


        // Build Y scales and axis:
        var y = d3.scaleBand()
            .range([height, 0])
            .domain(myVars)
            .padding(0.01);
        svg.append("g")
            .call(d3.axisLeft(y));

        // Build color scale
        var myColor = d3.scaleLinear()
            .range(["white", "#69b3a2"])
            .domain([1, 15])

        svg.selectAll()
            .data(data.pairs, function(d) {
                return d.A + ':' + d.B;
            })
            .enter()
            .append("rect")
            .attr("x", function(d) {
                return x(d.A)
            })
            .attr("y", function(d) {
                return y(d.B)
            })
            .attr("width", x.bandwidth())
            .attr("height", y.bandwidth())
            .style("fill", function(d) {
                return myColor(d.count)
            })
    })
}


// Switch between wordcloud and heatmap
function switchCanvas(type) {
    d3.select("#canvas").selectAll("*").remove();
    d3.select("#radio-select").selectAll("*").style("visibility", "hidden");

    if (type == "wordcloudButton") {
        drawWordcloud(filePath, "name");
    } else if (type == "heatmapButton")
        drawHeatmap(filePath);
}

var btnsTop = document.querySelectorAll("button");

for (btn of btnsTop) {
    btn.addEventListener('click', function() {
        switchCanvas(this.id);
    });
}


// Initial state: show the name cloud on 2019-06-01
drawWordcloud(filePath, "name");
drawHeatmap(filePath);