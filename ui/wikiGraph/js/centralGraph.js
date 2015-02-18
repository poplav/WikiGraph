        $(document).ready(function ()
        {
            $('#request').click(function()
            {
                        doD3();
            });
        });

        function contains(a, obj)
        {
            for (var i = 0; i < a.length; i++) {
                if (a[i] === obj) {
                    return true;
                }
            }
            return false;
        }

        function getGraph(data)
        {
            var nodes = [];
            for(var i=0;i<data.length;i++)
            {
                var tempSource = data[i]["source"];
                var tempDestination = data[i]["destination"];
                if(!contains(nodes, tempSource))
                    nodes.push(tempSource);
                if(!contains(nodes, tempDestination))
                    nodes.push(tempDestination);
            }

            var graph = [];
            for(var i=0; i<nodes.length; i++)
            {
                graph[nodes[i]] = [];
                graph[nodes[i]].push(i);
            }

            for(var i=0;i<data.length;i++)
            {
                var tempSource = data[i]["source"];
                var tempDestination = data[i]["destination"];
                graph[tempSource].push(tempDestination);
            }

            return graph;
        }
	function doD3()
	{
	        d3.select("svg").remove();
            // Get the data
            //http://localhost:5000/getCentralGraph/'Amtrak'/topN/2/depth/1
            var url = "http://localhost:5000/getCentralGraph/" + document.getElementById("vertex").value +
                        "/topN/" + + document.getElementById("topN").value + "/depth/" + document.getElementById("depth").value;
            d3.json(url, function(data)
            {
                for(var i=0;i<data.length;i++)
                {
                    var obj = data[i];
                    for(var key in obj)
                    {
                        var attrName = key;
                        var attrValue = obj[key];
                        console.log(key);
                        console.log(attrName + " -> " + attrValue);
                    }
                }
                var graph = getGraph(data);
                console.log(graph);
                for(i in graph)
                {
                    var s = i;
                    for(j in graph[i])
                        console.log(s + " - " + graph[i][j]);
                }

                var w = 1460, h = 600;

                var labelDistance = 0;
                var vis = d3.select("body").append("svg:svg").attr("width", w).attr("height", h);

                var nodes = [];
                var labelAnchors = [];
                var labelAnchorLinks = [];
                var links = [];


                for(var i in graph) {
                    var node = {
                        label : i
                    };
                    nodes.push(node);
                    labelAnchors.push({
                        node : node
                    });
                    labelAnchors.push({
                        node : node
                    });
                };

                console.log(nodes.length);
                for(var i in graph)
                {
                    var sourceIndex = graph[i][0];
                    for(var j=1; j<graph[i].length; j++)
                    {
                        var destinationIndex = graph[graph[i][j]][0];
                        console.log(sourceIndex + " - " + destinationIndex);
                        links.push({
                                source : sourceIndex,
                                target : destinationIndex,
                                weight : 1
                            });
                    }

                    labelAnchorLinks.push({
                        source : sourceIndex * 2,
                        target : sourceIndex * 2 + 1,
                        weight : 1
                    });
                }


                var force = d3.layout.force().size([w, h]).nodes(nodes).links(links).gravity(1).linkDistance(50).charge(-3000).linkStrength(function(x) {
                    return x.weight * 10
                });


                force.start();

                var force2 = d3.layout.force().nodes(labelAnchors).links(labelAnchorLinks).gravity(0).linkDistance(0).linkStrength(8).charge(-100).size([w, h]);
                force2.start();

                var link = vis.selectAll("line.link").data(links).enter().append("svg:line").attr("class", "link").style("stroke", "#CCC");

                var node = vis.selectAll("g.node").data(force.nodes()).enter().append("svg:g").attr("class", "node");
                node.append("svg:circle").attr("r", 5).style("fill", "#555").style("stroke", "#FFF").style("stroke-width", 3);
                node.call(force.drag);


                var anchorLink = vis.selectAll("line.anchorLink").data(labelAnchorLinks)//.enter().append("svg:line").attr("class", "anchorLink").style("stroke", "#999");

                var anchorNode = vis.selectAll("g.anchorNode").data(force2.nodes()).enter().append("svg:g").attr("class", "anchorNode");
                anchorNode.append("svg:circle").attr("r", 0).style("fill", "#FFF");
                    anchorNode.append("svg:text").text(function(d, i) {
                    return i % 2 == 0 ? "" : d.node.label
                }).style("fill", "#555").style("font-family", "Arial").style("font-size", 12);

                var updateLink = function() {
                    this.attr("x1", function(d) {
                        return d.source.x;
                    }).attr("y1", function(d) {
                        return d.source.y;
                    }).attr("x2", function(d) {
                        return d.target.x;
                    }).attr("y2", function(d) {
                        return d.target.y;
                    });

                }

                var updateNode = function() {
                    this.attr("transform", function(d) {
                        return "translate(" + d.x + "," + d.y + ")";
                    });

                }


                force.on("tick", function() {

                    force2.start();

                    node.call(updateNode);

                    anchorNode.each(function(d, i) {
                        if(i % 2 == 0) {
                            d.x = d.node.x;
                            d.y = d.node.y;
                        } else {
                            var b = this.childNodes[1].getBBox();

                            var diffX = d.x - d.node.x;
                            var diffY = d.y - d.node.y;

                            var dist = Math.sqrt(diffX * diffX + diffY * diffY);

                            var shiftX = b.width * (diffX - dist) / (dist * 2);
                            shiftX = Math.max(-b.width, Math.min(0, shiftX));
                            var shiftY = 5;
                            this.childNodes[1].setAttribute("transform", "translate(" + shiftX + "," + shiftY + ")");
                        }
                    });


                    anchorNode.call(updateNode);

                    link.call(updateLink);
                    anchorLink.call(updateLink);

                });
            });
	}
