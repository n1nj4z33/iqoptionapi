# -*- coding: utf-8 -*-
"""A python wrapper for IQ Option API."""

import logging


def _prepare_logging():
    """Prepare logger for module IQ Option API."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.NullHandler())

_prepare_logging()
