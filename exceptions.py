"""
Module contains a custom exception UserExit.

Classes:
    UserExit -- exception indicating a user-triggered exit.

The UserExit exception is used to handle situations where the user explicitly
interrupts the program execution or exits the process.

Example usage:
    raise UserExit("User initiated exit")
"""


class UserExit(Exception):
    """Exception for user-triggered exit."""
    pass