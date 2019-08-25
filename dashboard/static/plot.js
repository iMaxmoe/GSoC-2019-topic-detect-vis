// var filePath = "./json/" + date + ".json";

/**************************** Draw Lollipop *********************************/
// set the dimensions and margins of the graph
var margin = {top: 15, right: 20, bottom: 30, left: 100},
    width = $(".g-names .m-top10").width()- 50 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom,
    radius = 6;

// append the svg object to the body of the page

function drawLollipop(data, container, type) {

    var lollipop = d3.select(container)
                    .append("svg")
                    .attr("id", "lollipop")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

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
}


/**************************** Draw wordclouds *********************************/
var cloudWidth = $(".g-names .m-wordcloud").width()-40;
var cloud = d3.layout.cloud().size([cloudWidth, 430])

function drawWordcloud(data, container, type) {
    /* type: \n
        "name" : person name cloud \n
        "occupations": occupation cloud */

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
            .style("font-family", "Impact, Haettenschweiler, Franklin Gothic Bold, Charcoal, Helvetica Inserat, Bitstream Vera Sans Bold, Arial Black, sans serif")
            .style("fill", (d) => (wordColor(d.size)))
            .attr("class", "words")
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text((d) => d.text)
    }
}


/**************************** Draw Heatmap *********************************/
function drawHeatmap(data, container) {
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
                        .range(["#afe3e5", "#209aa9"]) 
                                                

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
}


/**************************** Draw Network *********************************/
function drawNetwork(data, container) {

    var svg = d3.select(container)
                .append("svg")
                  .attr("width", $(".g-relation .m-network").width()-30)
                  .attr("height", 460),
        width = +svg.attr("width"),
        height = +svg.attr("height");
    
    var simulation = d3.forceSimulation()
                       .force("link", d3.forceLink().id((d) => d.id))
                       .force("charge", d3.forceManyBody().strength(-100))
                       .force("center", d3.forceCenter(width/2, height/2))
                       .nodes(data.nodes)
                       .on("tick", ticked);

    var link = svg.append("g")
                    .attr("class", "links")
                    .selectAll("line")
                    .data(data.links)
                    .enter()
                    .append("line")
                        .attr("stroke", "#999")
                        .attr("stroke-opacity", "0.6")
                        .attr("stroke-width", (d) => Math.sqrt(d.value)/2);
                    
    var node = svg.append("g")
                    .attr("class", "nodes")
                    .selectAll("g")
                    .data(data.nodes)
                    .enter()
                    .append("g")
                    
    function ticked() {       
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")"})
            .attr("cx", function(d) { return d.x = Math.max(radius, Math.min(width - radius, d.x)); })
            .attr("cy", function(d) { return d.y = Math.max(radius, Math.min(height - radius, d.y)); });
    }                    
        
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
            
    link.append("title")
        .text((d) => d.value);

    simulation.nodes(data.nodes)
              .on("tick", ticked);
                
    simulation.force("link")
              .links(data.links)
    
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

};

/*********************** Draw Trend *********************************/

function drawTrend(data, container) {

    data = data['count']
    
    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = $(".m-barchart").width() - margin.left - margin.right,
        height = $(".m-barchart").height() - margin.top - margin.bottom;

    // set the ranges
    var x = d3.scaleBand()
              .range([0, width])
              .padding(0.04);
    var y = d3.scaleLinear()
              .range([height, 0]);
              
    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select(container)
                .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                        .attr("transform", 
                              "translate(" + margin.left + "," + margin.top + ")");  
                              
    data.forEach(function(d) {
        d.num = +d.num;
    });  
                              
    x.domain(data.map(function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.num; })]);

    // append the rectangles for the bar chart
    svg.selectAll(".bar")
       .data(data)
       .enter()
       .append("rect")
           .attr("class", "bar")
           .attr("x", function(d) { return x(d.date); })
           .attr("width", x.bandwidth())
           .attr("y", function(d) { return y(d.num); })
           .attr("height", function(d) { return height - y(d.num); })
           .style("fill", "lightseagreen")
           .append("title")
                .text((d)=>(d.date+", "+d.num))   

    svg.selectAll("text")
       .data(data)
       .enter()
       .append("text")
           .text((d)=>(d.num))
           .attr("x", (d, i) => (i*(width/ data.length) +5))
           .attr("y", (d) => (height-4*d+15))
           .attr("font-family", "sans-serif")
           .attr("font-size", "11px")
           .attr("fill", "white")           
                
    // add the x Axis
    svg.append("g")
           .attr("transform", "translate(0," + height + ")")
           .call(d3.axisBottom(x));
           
    svg.selectAll("text")
        .attr("y", -7)
        .attr("x", -12)
        .attr("dy", ".35em")
        .attr("transform", "translate(-10,0)rotate(15)")
        .style("text-anchor", "start");

    // add the y Axis
    svg.append("g")
       .call(d3.axisLeft(y));
}


/*********************** Draw Donut *********************************/
function drawDonut(data, container) {

    data = data['network']

    var svg = d3.select(container)
                .append("svg")
                    .attr("width", $(".m-donutchart").width()-30)
                    .attr("height", $(".m-donutchart").height()-30),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        radius = Math.min(width, height) / 2,
        g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
        

    var color = d3.scaleOrdinal(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    var pie = d3.pie()
                .value(function(d) { return d.num; });

    var path = d3.arc()
                 .outerRadius(radius - 10)
                 .innerRadius(radius - 100);

    var label = d3.arc()
                  .outerRadius(radius - 40)
                  .innerRadius(radius - 40);
                  
    data.forEach(function(d) {
        d.num = +d.num;
    });  
                  
    var arc = g.selectAll(".arc")
               .data(pie(data))
               .enter()
               .append("g")
                   .attr("class", "arc");

    arc.append("path")
           .attr("d", path)
           .attr("fill", function(d) { return color(d.data.name); })
           .append("title")
               .text((d)=>(d.data.name+", "+d.data.num))               

    arc.append("text")
           .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
           .attr("dy", "0.35em")
           .text(function(d) { return d.data.name; });
}
