from sys import stdlib_module_names
from inspect import getmembers, isclass, isfunction, ismethod, ismethoddescriptor, ismethodwrapper
from types import FunctionType, BuiltinFunctionType
from functools import partial

from colorama import Fore


ITALIC = '\033[3m'
ITALIC_RESET = '\033[0m'

# Styles
S_PROTECTED = ITALIC
S_RESET = ITALIC_RESET

# Colors
C_NAME = Fore.BLUE
C_NAME_FUNC = Fore.GREEN
C_EQUALS = Fore.RESET
C_PUNC = Fore.LIGHTBLACK_EX
C_CLS = Fore.WHITE
C_VALUE = Fore.RESET

_GAP = '   '


def in_stdlib(obj: object) -> bool:
    """
    Returns True iff an object is part of the standard library.
    """
    cls = obj if isclass(obj) else type(obj)
    return cls.__module__ in stdlib_module_names


def is_function_like(obj: object) -> bool:
    """
    Returns True iff an object is function like.
    """
    return (isfunction(obj)
            or ismethod(obj)
            or ismethoddescriptor(obj)
            or ismethodwrapper(obj)
            or isinstance(obj, (FunctionType, BuiltinFunctionType, partial)))


def is_member_of(name: str, classes: tuple[type, ...]) -> bool:
    """
    Returns True iff a member name is found to be a member of at least one of the provided classes.
    """
    for cls in classes:
        if name in [name for name, _ in getmembers(cls)]:
            return True
    return False


def get_members(obj: object,
                include_inherited: bool = True,
                include_inherited_stdlib: bool = False,
                include_magics: bool = False,

                ) -> list[tuple[str, object]]:
    """
    Get the members as (name, value) pairs of an object.
    """
    # Get class, standard lib base classes, and standard lib base class member names
    cls = obj if isclass(obj) else type(obj)

    # Get base classes
    bases = cls.__bases__

    # Get bases classes that are in the standard lib
    bases_stdlib = tuple(base for base in bases
                         if in_stdlib(base))

    # Get all member names of base classes that are in the standard lib
    bases_stdlib_member_names = []
    if not include_inherited_stdlib:
        bases_stdlib_member_names = [name
                                     for base in bases_stdlib
                                     for name, _ in getmembers(base)]

    # Get all members with that match the criteria
    members = []
    for name, value in getmembers(obj):
        if (
                (include_inherited or not is_member_of(name, bases))
                and (include_inherited_stdlib or name not in bases_stdlib_member_names)
                and (include_magics or not name.startswith('__') or not name.endswith('__'))
        ):
            members.append((name, value))
    return members


def get_name_str(name: str, is_function: bool) -> str:
    """
    Generates the name str, e.g. "foo =".
    """
    style = S_PROTECTED if name.startswith('_') else ''
    color = C_NAME_FUNC if is_function else C_NAME

    return (
        f'{style}{color}{name}'
        f'{S_RESET}{C_EQUALS} ='
    )


def get_type_str(obj: object) -> str:
    """
    Generates the type str, e.g. "{Foo(Bar, Exception)}".
    """
    cls = obj if isclass(obj) else type(obj)

    # Not interesting to show that a class inherits from object
    bases_str = f'{C_PUNC}, '.join([f'{C_CLS}{base.__name__}'
                                    for base in cls.__bases__
                                    if base != object])

    bases_str = f'{C_PUNC}({bases_str}{C_PUNC})' if bases_str else ''

    return (
        f'{C_PUNC}{{'
        f'{C_CLS}{cls.__name__}'
        f'{bases_str}'
        f'{C_PUNC}}}'
    )


def get_value_str(obj: object) -> str:
    """
    Generates the value str, e.g. "<__main__.Foo object at 0x10fa51850>".
    """
    return (
        f'{C_VALUE}{obj}'
    )


def _inspect_members(obj: object, parent_classes: list[type], depth: int = 0) -> None:
    """
    Recursive function for inspecting and printing info of members and their members.
    """
    for name, member in get_members(obj):
        # Print members details
        print(_GAP * (depth + 1), get_name_str(name, is_function_like(member)), get_type_str(member),
              get_value_str(member))

        member_cls = member if isclass(member) else type(member)

        # Don't further inspect members that have the same class as any of its parents, to prevent infinite recursion
        # Don't further inspect members that are standard types (properties of standard types aren't interesting)
        if member_cls not in parent_classes and not in_stdlib(member):
            # Add the member's class to a list copy, to prevent list cross contamination between recursion branches
            parent_classes_copy = parent_classes.copy()
            parent_classes_copy.append(member_cls)

            _inspect_members(member, parent_classes_copy, depth + 1)


def squiz(obj: object) -> None:
    """
    Prints the direct and nested member names, types, and values of the target object.
    """
    # Print the main object's details only (we can't easily know it's variable name)
    print(get_type_str(obj), get_value_str(obj))

    # Don't further inspect standard types (properties of standard types aren't interesting)
    if not in_stdlib(obj):
        cls = obj if isclass(obj) else type(obj)
        _inspect_members(obj, parent_classes=[cls])
