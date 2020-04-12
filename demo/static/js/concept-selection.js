// Copyright (c) 2020 Hecong Wang
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

class ConceptSelection {
    constructor(text_id, speech_id, input_delay) {
        this.text_input = document.getElementById(text_id);
        this.speech_input = document.getElementById(speech_id);

        this.options = this.speech_input.querySelectorAll("option.speech");
        this.complete = M.Autocomplete.init(
            this.text_input,
            {
                data: {},
                onAutocomplete: () => this.query_speech()
            }
        );

        this.input_delay = input_delay;
        this.input_timer = null;

        this.text_input.addEventListener("input", () => this.listener());
    }

    listener() {
        for (var option of this.options) option.setAttribute("disabled", "");

        M.FormSelect.init(this.speech_input, {});

        clearTimeout(this.input_timer);
        this.input_timer = setTimeout(() => this.query_text(), this.input_delay);
    }

    async query_text() {
        var input = this.text_input.value.toLowerCase().replace(/\s+/g, '_');
        var query = `/api/text/${input}`;

        var source = await fetch(query);
        var data = await source.json();

        this.complete.updateData(data);
        this.complete.open();
    }

    async query_speech() {
        var input = this.text_input.value.toLowerCase().replace(/\s+/g, '_');
        var query = `/api/speech/${input}`;

        var source = await fetch(query);
        var data = await source.json();

        for (var option of this.options)
            if (data[input].includes(option.value))
                option.removeAttribute("disabled");

        M.FormSelect.init(this.speech_input, {});
    }
}

export { ConceptSelection };
