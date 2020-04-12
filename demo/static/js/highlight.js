// Copyright (c) 2020 Hecong Wang
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

class Highlight {
    constructor(selector, classes, source) {
        this.content = d3.select(selector);
        this.classes = classes

        d3.json(source).then((data, error) => this.initialize(data, error));
    }

    initialize(data, error) {
        if (error) throw error;

        this.story = [];
        for (var i = 0; i < data.lines.length; ++i) {
            for (var j = 0; j < data.lines[i].words.length; ++j) {
                this.story.push({
                    line: i,
                    index: j,
                    content: data.lines[i].words[j].content,
                    vocabulary: data.lines[i].words[j].vocabulary
                });
            }
        }

        this.content.append("p").classed("flow-text", true).selectAll("span")
            .data(this.story, data => (data.line, data.index))
            .enter()
            .append("div")
            .classed("word", true)
            .append("span")
            .classed(this.classes[0], true)
            .attr("classes", this.classes)
            .html(data => data.content)
            .filter(data => data.vocabulary)
            .on("click", Highlight.toggle);
    }

    static toggle() {
        var element = d3.select(this);
        var classes = element.attr("classes").split(',');

        var current = classes.indexOf(element.attr("class"));
        var next = (current + 1) % classes.length;

        element.classed(classes[current], false).classed(classes[next], true);
    }
}
