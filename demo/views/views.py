# Copyright (c) 2020 Hecong Wang
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import render_template
from ..app import app


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
