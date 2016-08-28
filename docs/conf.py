# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join('../iqapi'))

extensions = ["sphinx.ext.todo",
              "sphinx.ext.viewcode",
              "sphinx.ext.autodoc"]

master_doc = "index"
