# Copyright (c) 2020 Hecong Wang
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

from os import path

from flask import Flask

from models import database

CONFIG_JSON = path.join(path.dirname(path.abspath(__file__)), "config.json")

app = Flask(__name__)
app.config.from_json(CONFIG_JSON)

database.init_app(app)
