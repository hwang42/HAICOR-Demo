# Copyright (c) 2020 Hecong Wang
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

app: Flask = Flask(__name__)
app.config.from_json(os.path.join(APP_DIRECTORY, "config.json"))

database: SQLAlchemy = SQLAlchemy(app)
