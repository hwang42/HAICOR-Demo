# Copyright (c) 2020 Hecong Wang
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import jsonify

from ..app import app, database
from ..models.concepts import Concept, PartOfSpeech


@app.route("/api/complete/<string:text>")
def complete(text: str) -> str:
    speech = database.session.query(PartOfSpeech)

    speech = {i.id: i.code for i in speech}
    speech[None] = None

    concept = database.session.query(Concept.text, Concept.speech)\
        .filter(Concept.text.contains(text)).distinct()

    concept = ({"text": i.text, "speech": speech[i.speech]} for i in concept)

    return jsonify({"concepts": tuple(concept)})
