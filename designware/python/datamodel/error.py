""" This file creates the error/messaging module

This module creates classes that are used for messaging errors
"""

class AError(Exception):
    """ This is the base class for all exceptions raised in the framework

    Attributes:
        message : string carrying the error message
    """
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message
