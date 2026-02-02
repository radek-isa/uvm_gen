#!/bin/python3

from datetime import datetime


"""
This module contains generatig files
"""

class config:
    """
    Common configuration for generating verification files
    """
    def __init__(self, author_name, author_email):
        # This variable is used for generating preambule
        self.year = datetime.now().year
        self.author_name = author_name
        self.author_email = author_email



from . import sv


