// Copyright (c) 2020 Hecong Wang
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

class KnowledgeGraph {
    constructor(selector) {
        this.width = 800;
        this.height = 600;
        this.svg = d3.select(selector).append("svg")
            .classed("knowledge-graph", true)
            .attr("preserveAspectRatio", "xMidYMid meet")
            .attr("viewBox", `0 0 ${this.width} ${this.height}`);

        this.concepts = [];
        this.relations = [];

        this.simulation = d3.forceSimulation(this.concepts)
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .force("relation", d3.forceLink(this.relations))
            .force("collision", d3.forceCollide())
            .on("tick", () => this.ticked());
    }

    ticked() {
        this.svg.selectAll("line")
            .data(this.relations)
            .enter()
            .append("line")
            .classed("relation", true)
            .merge(this.svg.selectAll("line").data(this.relations))
            .attr("x1", data => data.source.x)
            .attr("y1", data => data.source.y)
            .attr("x2", data => data.target.x)
            .attr("y2", data => data.target.y);

        this.svg.selectAll("circle")
            .data(this.concepts)
            .enter()
            .append("circle")
            .attr("r", "1rem")
            .classed("concept", true)
            .call(d3.drag()
                .on("start", data => this.drag_start(data))
                .on("drag", data => this.dragging(data))
                .on("end", data => this.drag_end(data)))
            .merge(this.svg.selectAll("circle").data(this.concepts))
            .attr("cx", data => data.x)
            .attr("cy", data => data.y);
    }

    add_concept(node) {
    }

    add_relation(source, target) {
    }

    drag_start(data) {
        if (!d3.event.active) this.simulation.alphaTarget(0.3).restart();

        data.fx = data.x;
        data.fy = data.y;
    }

    dragging(data) {
        data.fx = d3.event.x;
        data.fy = d3.event.y;
    }

    drag_end(data) {
        if (!d3.event.active) this.simulation.alphaTarget(0);

        data.fx = null;
        data.fy = null;
    }
}

export { KnowledgeGraph };
