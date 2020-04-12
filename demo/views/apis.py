# Copyright (c) 2020 Hecong Wang
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

from typing import Optional

from flask import jsonify

from ..app import app, database
from ..models.concepts import Concept, PartOfSpeech


def uri(concept: Concept) -> str:
    return f"/c/{concept.language.code}/{concept.text}" \
        + (f"/{concept.part_of_speech.code}" if concept.speech else "") \
        + (concept.suffix if concept.suffix else "")


@app.route("/api/text/<string:text>")
def concept_text(text: str) -> str:
    concepts = database.session.query(Concept)\
        .filter(Concept.text.contains(text))

    return jsonify({c.text.replace('_', ' '): None for c in concepts})


@app.route("/api/speech/<string:text>")
def concept_speech(text: str) -> str:
    concepts = database.session.query(Concept).filter_by(text=text)
    speeches = (c.part_of_speech.code if c.speech else ' ' for c in concepts)

    return jsonify({text: tuple(set(speeches))})


@app.route("/api/concept/<string:text>", defaults={"speech": None})
@app.route("/api/concept/<string:text>/<string:speech>")
def conepts(text: str, speech: Optional[str]) -> str:
    speech = database.session.query(PartOfSpeech)\
        .filter_by(code=speech).one().id if speech else None
    concepts = database.session.query(Concept)\
        .filter_by(text=text, speech=speech)
    concepts = ({"id": c.id, "text": c.text, "speech": c.speech, "uri": uri(c)}
                for c in concepts)

    return jsonify({"concepts": tuple(concepts)})
