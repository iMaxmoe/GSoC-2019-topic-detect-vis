var date = "2019-06-01"; // default date
var filePath = "./json/" + date + ".json";

/**************************** Draw Lollipop *********************************/
// set the dimensions and margins of the graph
var margin = {top: 15, right: 20, bottom: 30, left: 100},
    width = 460 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom,
    radius = 6;

// append the svg object to the body of the page

function drawLollipop(dataSource, container, type) {

    var lollipop = d3.select(container)
                 .append("svg")
                    .attr("id", "lollipop")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                 .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Parse the Data
    d3.json(dataSource, function(data) {
        data = data[type];

        // Add X axis
        var x = d3.scaleLinear()
                    .domain([0, d3.max(data, (d)=>(d["count"]+10))])
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
                    .domain(data.slice(0, 10).map((d)=>(d.key)))
                    .padding(1);

        lollipop.append("g")
                .call(d3.axisLeft(y))

        // Lines
        lollipop.selectAll("myline")
                    .data(data.slice(0, 10))
                    .enter()
                .append("line")
                    .attr("x1", (d)=> x(d.count))
                    .attr("x2", x(0))
                    .attr("y1", (d)=> y(d.key))
                    .attr("y2", (d)=> y(d.key))
                    .attr("stroke", "grey")

        // Circles
        lollipop.selectAll("mycircle")
                    .data(data.slice(0, 10))
                    .enter()
                .append("circle")
                    .attr("cx", (d)=> x(d.count))
                    .attr("cy", (d)=> y(d.key))
                    .attr("r", "7")
                    .attr("class", "circle")
                    .style("fill", "#69b3a2")
                    .attr("stroke", "black")
                .append("title")
                    .text((d)=>(d.key+", "+d.count))
    });
}

function changeDateLollipop(date) {
    // lollipop.selectAll("*").remove();
    var filePath = "./json/" + date + ".json";
    drawLollipop(filePath, ".g-names .m-top10 .card-content", "persons");
    drawLollipop(filePath, ".g-jobs .m-top10 .card-content", "occupations");
    //drawWordcloud(filePath);
}

changeDateLollipop("2019-06-01");

/**************************** Draw wordclouds *********************************/
var cloud = d3.layout.cloud().size([480, 430])

function drawWordcloud(dataSource, container, type) {
    /* type: \n
        "name" : person name cloud \n
        "occupations": occupation cloud */
    d3.json(dataSource, function(data) {
        data = data[type];
        let max = d3.max(data, (d) => d.count)
        let wordSize = d3.scaleLinear().domain([0, max/25, max/5, max]).range([10, 20, 40, 80]);
        let wordColor = d3.scaleLinear().domain([10, 20, 40, 80]).range(["blue", "green", "orange", "red"]);

        // Number of words to be included in the word cloud
        var num = data.length < 100 ? data.length : 100;
        data = data.slice(0, num);

        cloud.words(data.map(function(d) {
                return { text: d.key, size: wordSize(parseInt(d.count))}
            }))
             .padding(5)
             .font("Impact")
             .fontSize((d) => (d.size))
             .on("end", draw);

        cloud.start();

        function draw(words) {
            d3.select(container)
              .append("svg")
                .attr("width", cloud.size()[0])
                .attr("height", cloud.size()[1])
              .append("g")
                .attr("transform", "translate(" + cloud.size()[0] / 2 + "," + cloud.size()[1] / 2 + ")")
              .selectAll("text")
                .data(words)
                .enter()
              .append("text")
                .style("font-size", function(d) { return d.size + "px";})
                .style("font-family", "Impact, Courier New")
                .style("fill", (d) => (wordColor(d.size)))
                .attr("class", "words")
                .attr("text-anchor", "middle")
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text((d) => d.text)
        }
    })
}

drawWordcloud(filePath, ".g-names .m-wordcloud .card-content", "persons");
drawWordcloud(filePath, ".g-jobs .m-wordcloud .card-content", "occupations");


/**************************** Draw Heatmap *********************************/
function drawHeatmap(dataSource, container) {
    // set the dimensions and margins of the graph
    var margin = {top: 20,right: 30,bottom: 130,left: 120},
        width = 500 - margin.left - margin.right,
        height = 480 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(container)
                .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                .append("g")
                    .attr("transform","translate(" + margin.left + "," + margin.top + ")");

    //Read the data
    d3.json(dataSource, function(data) {

        // Build X scales and axis:
        var x = d3.scaleBand()
                    .range([0.1, width])
                    .domain(data.axis)
                    .padding(0.05);

        svg.append("g")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x));

        svg.selectAll("text")
              .attr("y", 0)
              .attr("x", 9)
              .attr("dy", ".35em")
              .attr("transform", "translate(-10,0)rotate(60)")
              .style("text-anchor", "start");

        // Build Y scales and axis:
        var y = d3.scaleBand()
                    .range([height, 0])
                    .domain(data.axis)
                    .padding(0.015);

        svg.append("g")
            .call(d3.axisLeft(y));

        // Build color scale
        var myColor = d3.scaleLinear()
                          .domain([1, d3.max(data.pairs, (d) => d.value)])
                          .range(["white", "#69c3b2"]) 
                                                    

        svg.selectAll()
           .data(data.pairs)
           .enter()
           .append("rect")
             .attr("x", (d) => x(d.source))
             .attr("y", (d) => y(d.target))
             .attr("width", x.bandwidth())
             .attr("height", y.bandwidth())
             .attr("class", "square")
             .style("fill", (d) => myColor(d.value))
           .append("title")
             .text((d) => d.source+" & "+d.target+": "+d.value)
    })
}

drawHeatmap(filePath, ".m-heatmap .card-content");


/**************************** Draw Network *********************************/
function drawNetwork(dataSource, container) {
    var svg = d3.select(container)
                .append("svg")
                  .attr("width", 480)
                  .attr("height", 460),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var simulation = d3.forceSimulation()
                       .force("link", d3.forceLink().id((d) => d.id))
                       .force("charge", d3.forceManyBody().strength(-8))
                       .force("center", d3.forceCenter(width / 2, height / 2));
                    
    d3.json(dataSource, function(data) {

        var link = svg.append("g")
                        .attr("class", "links")
                      .selectAll("line")
                        .data(data.links)
                        .enter()
                      .append("line")
                        .attr("stroke", "#999")
                        .attr("stroke-opacity", "0.6")
                        .attr("stroke-width", (d) => Math.sqrt(d.value));
                        
        var node = svg.append("g")
                        .attr("class", "nodes")
                      .selectAll("g")
                        .data(data.nodes)
                        .enter()
                      .append("g")
            
        var circles = node.append("circle")
                            .attr("r", 8)
                            .attr("fill", "#69c3b2")
                            .call(d3.drag()
                                .on("start", dragstarted)
                                .on("drag", dragged)
                                .on("end", dragended));

        var lables = node.append("text")
                            .text((d) => d.id)
                            .attr('x', 6)
                            .attr('y', 3);

        node.append("title")
            .text((d) => d.id);

        simulation.nodes(data.nodes)
                    .on("tick", ticked);
                    
        simulation.force("link")
                    .links(data.links)

        function ticked() {       
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")"})
                .attr("cx", function(d) { return d.x = Math.max(radius, Math.min(width - radius, d.x)); })
                .attr("cy", function(d) { return d.y = Math.max(radius, Math.min(height - radius, d.y)); });
        }
    });

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

drawNetwork(filePath, ".m-network .card-content");
