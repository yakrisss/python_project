"""
Module with user exit exception and decorator.

Classes:
    UserExit -- raised when user chooses to exit.
"""


class UserExit(Exception):
    """Exception for user-triggered exit."""
