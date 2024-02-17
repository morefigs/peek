import builtins
from inspect import getmembers


# Terminal print colors
_NONE = '\33[0m'
_GREY = '\33[90m'
_BLUE = '\033[34m'

_BUILTIN_TYPES = tuple(value for _, value in getmembers(builtins) if type(value) is type)


def _squiz(obj: object, depth: int):
    # Don't bother further inspecting built-in types (int, str, Exception, ...), except for 'type' itself
    if type(obj) not in _BUILTIN_TYPES or type(obj) is type:
        for name, value in getmembers(obj):
            # Ignore hidden members and magic methods
            if not name.startswith('__'):
                # Print members details
                print(f"{depth * '   ' + '   '}{_BLUE}{name} {_NONE}= {_GREY}{{{type(value).__name__}}} {_NONE}{value}")

                # Recursively check nested members
                _squiz(value, depth + 1)


def squiz(obj: object) -> None:
    """
    Prints the direct and nested member names, types, and values of the target object.
    """
    # Print the target object details
    print(f'{_GREY}{{{type(obj).__name__}}} {_NONE}{obj}')

    _squiz(obj, 0)
