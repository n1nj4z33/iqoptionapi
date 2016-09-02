# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

extensions = ["sphinx.ext.todo",
              "sphinx.ext.viewcode",
              "sphinx.ext.autodoc"]

master_doc = "index"

autoclass_content = "both"

html_static_path = ["_static"]

templates_path = ["_templates"]

project = "iqoptionapi"

copyright = "2016, n1nj4z33"

author = "n1nj4z33"

version = "0.1"
