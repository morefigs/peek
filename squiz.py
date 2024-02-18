from sys import stdlib_module_names
from inspect import getmembers, isclass


# Terminal print colors
_NONE = '\33[0m'
_GREY = '\33[90m'
_BLUE = '\33[34m'

_GAP = '   '


def _in_stdlib(obj: object) -> bool:
    cls = obj if isclass(obj) else type(obj)
    return cls.__module__ in stdlib_module_names


def _squiz(obj: object, depth: int = 0):
    # Don't bother further inspecting standard types
    if not _in_stdlib(obj):
        for name, member in getmembers(obj):
            # Ignore magic methods for clarity
            if not name.startswith('__') or not name.endswith('__'):
                # Print members details
                print(f"{_GAP * (depth + 1)}{_BLUE}{name} {_NONE}= {_GREY}{{{type(member).__name__}}} {_NONE}{member}")

                # Recursively check nested members
                _squiz(member, depth + 1)


def squiz(obj: object) -> None:
    """
    Prints the direct and nested member names, types, and values of the target object.
    """
    # Print the target object details
    print(f'{_GREY}{{{type(obj).__name__}}} {_NONE}{obj}')

    _squiz(obj)
