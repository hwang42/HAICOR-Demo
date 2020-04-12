// Copyright (c) 2020 Hecong Wang
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

class Concept {
    constructor(text, speech, delay) {
        this.text_input = document.getElementById(text);
        this.speech_input = document.getElementById(speech);

        this.options = this.speech_input.querySelectorAll("option.speech");
        this.autocomplete = M.Autocomplete.init(this.text_input, { data: {}, onAutocomplete: () => this.update_speech() });

        this.timer = null;
        this.delay = delay;

        this.text_input.addEventListener("input", () => this.wait());
    }

    wait() {
        for (var i = 0; i < this.options.length; ++i) this.options[i].setAttribute("disabled", "");

        M.FormSelect.init(this.speech_input, {});

        clearTimeout(this.timer);
        this.timer = setTimeout(() => this.update_text(), this.delay);
    }

    update_text() {
        var input = this.text_input.value.toLowerCase().replace(/\s+/g, '_');
        var query = `/api/text/${input}`;

        fetch(query).then(source => source.json().then(data => { this.autocomplete.updateData(data); this.autocomplete.open(); }));
    }

    update_speech() {
        var input = this.text_input.value.toLowerCase().replace(/\s+/g, '_');
        var query = `/api/speech/${input}`;

        fetch(query).then(source => source.json().then(data => this.set_speech(data[input])));
    }

    set_speech(data) {
        for (var i = 0; i < this.options.length; ++i)
            if (data.indexOf(this.options[i].value) != -1)
                this.options[i].removeAttribute("disabled");

        M.FormSelect.init(this.speech_input, {});
    }
}
