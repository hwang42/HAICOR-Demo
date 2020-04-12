// Copyright (c) 2020 Hecong Wang
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

class StoryHighlight {
    constructor(selector, classes) {
        this.container = d3.select(selector).classed("story-highlight", true);
        this.classes = classes;
    }

    async initialize(source) {
        var error, data = await d3.json(source);

        if (error) throw error;

        this.story = [];
        for (var line of data.lines)
            for (var word of line.words) {
                this.story.push({
                    line: line.index,
                    word: word.index,
                    content: word.content,
                    vocabulary: word.vocabulary,
                    importance: 0
                });
            }

        this.container.append("p").selectAll("span")
            .data(this.story, data => (data.line, data.word))
            .enter()
            .append("div")
            .append("span")
            .text(data => data.content)
            .attr("classes", this.classes)
            .classed(this.classes[0], true)
            .filter(data => data.vocabulary)
            .on("click", StoryHighlight.toggle);
    }

    static toggle(data) {
        var element = d3.select(this);
        var classes = element.attr("classes").split(',');

        data.importance = (data.importance + 1) % classes.length;
        element.attr("class", classes[data.importance]);
    }
}

export { StoryHighlight };
