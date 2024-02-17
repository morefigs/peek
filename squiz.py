import builtins
from inspect import getmembers


# Terminal print colors
_NONE = '\33[0m'
_GREY = '\33[90m'
_BLUE = '\033[34m'

_BUILTIN_TYPES = tuple(value for name, value in getmembers(builtins) if type(value) is type)


def _squiz(obj: object, depth: int):
    for name, value in getmembers(obj):
        if not name.startswith('__'):
            type_ = type(value)

            print(f"{depth * '   ' + '   '}{_BLUE}{name} {_NONE}= {_GREY}{{{type_.__name__}}} {_NONE}{value}")

            # Only recursively inspect attributes that aren't built-in types
            if type_ not in _BUILTIN_TYPES:
                _squiz(value, depth + 1)


def squiz(obj: object) -> None:
    """
    Prints the direct and nested attribute names, types, and values of the target object.
    """
    print(f'{_GREY}{{{type(obj).__name__}}} {_NONE}{obj}')

    _squiz(obj, 0)
