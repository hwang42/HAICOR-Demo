# Copyright (c) 2020 Hecong Wang
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import jsonify

from ..app import app, database
from ..models.concepts import Concept


@app.route("/api/text/<string:text>")
def concept_text(text: str) -> str:
    concepts = database.session.query(Concept.text)\
        .filter(Concept.text.contains(text)).distinct()

    return jsonify({c.text.replace('_', ' '): None for c in concepts})


@app.route("/api/speech/<string:text>")
def concept_speech(text: str) -> str:
    concepts = database.session.query(Concept)\
        .filter(Concept.text == text).distinct(Concept.speech)
    speeches = (c.part_of_speech.code if c.speech else ' ' for c in concepts)

    return jsonify({text: tuple(set(speeches))})
