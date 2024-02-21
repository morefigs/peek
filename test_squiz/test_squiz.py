from abc import ABC
from threading import Thread
from datetime import datetime
from functools import partial

import pytest

from squiz import S_PROTECTED, S_RESET, C_NAME, C_NAME_FUNC, C_EQUALS, C_PUNC, C_CLS, C_VALUE, in_stdlib, \
    is_function_like, is_member_of, get_members, get_name_str, get_type_str, get_value_str


def func():
    pass


class Funcs:
    foo = None
    partial_ = partial(func, 1)
    lambda_ = lambda x: None

    def __init__(self):
        pass

    def func(self):
        pass

    @classmethod
    def func_class(cls):
        pass

    @staticmethod
    def func_static(*args):
        pass


class FuncsChild(Funcs, OSError):
    pass


class Parent:
    __u = None
    def __v(self): pass
    _w = None
    def _x(self): pass
    y = None
    def z(self): pass


class Child(Parent):
    __a = None
    def __b(self): pass
    _c = None
    def _d(self): pass
    e = None
    def f(self): pass


@pytest.mark.parametrize('result, obj', (
        (True, int),
        (True, str),
        (True, ABC),
        (True, Thread),
        (True, datetime),
        (True, ZeroDivisionError),

        (True, 123),
        (True, 'asdf'),
        (True, ABC()),
        (True, Thread()),
        (True, datetime.now()),
        (True, ZeroDivisionError('oops')),

        (False, Funcs),

        (False, Funcs())
))
def test_in_stdlib(result: bool, obj: type):
    assert in_stdlib(obj) is result


@pytest.mark.parametrize('result, obj', (
        (True, func),

        (True, Funcs.partial_),
        (True, Funcs.lambda_),
        (True, Funcs.__init__),
        (True, Funcs.func),
        (True, Funcs.func_class),
        (True, Funcs.func_static),
        (True, Funcs().partial_),
        (True, Funcs().lambda_),
        (True, Funcs().__init__),
        (True, Funcs().func),
        (True, Funcs().func_class),
        (True, Funcs().func_static),

        (True, FuncsChild.partial_),
        (True, FuncsChild.lambda_),
        (True, FuncsChild.__init__),
        (True, FuncsChild.func),
        (True, FuncsChild.func_class),
        (True, FuncsChild.func_static),
        (True, FuncsChild().partial_),
        (True, FuncsChild().lambda_),
        (True, FuncsChild().__init__),
        (True, FuncsChild().func),
        (True, FuncsChild().func_class),
        (True, FuncsChild().func_static),

        (False, 123),
        (False, 'asdf'),
        (False, Funcs),
        (False, Funcs()),
))
def test_is_function_like(result: bool, obj: object):
    assert is_function_like(obj) == result


@pytest.mark.parametrize('result, name, classes', (
        (True, 'end_lineno', (SyntaxError,)),
        (True, 'foo', (Funcs,)),
        (True, 'end_lineno', (SyntaxError, Funcs)),
        (True, 'foo', (SyntaxError, Funcs)),

        (False, 'nope', (SyntaxError, )),
        (False, 'nope', (SyntaxError, Funcs)),
))
def test_is_member_of(result: bool, name: str, classes: tuple[type, ...]):
    assert is_member_of(name, classes) == result


@pytest.mark.parametrize('result, obj, include_inherited, include_inherited_stdlib, include_magics', (
        ([
             ('_Child__a', Child._Child__a),
             ('_Child__b', Child._Child__b),
             ('_c', Child._c),
             ('_d', Child._d),
             ('e', Child.e),
             ('f', Child.f),
        ], Child, False, False, False),
        ([
             ('_Child__a', Child._Child__a),
             ('_Child__b', Child._Child__b),
             ('_Parent__u', Child._Parent__u),
             ('_Parent__v', Child._Parent__v),
             ('_c', Child._c),
             ('_d', Child._d),
             ('_w', Child._w),
             ('_x', Child._x),
             ('e', Child.e),
             ('f', Child.f),
             ('y', Child.y),
             ('z', Child.z),
         ], Child, True, False, False),
))
def test_get_members(result: list[tuple[str, object]],
                     obj: object,
                     include_inherited: bool,
                     include_inherited_stdlib: bool,
                     include_magics: bool):
    assert get_members(obj, include_inherited, include_inherited_stdlib, include_magics) == result


@pytest.mark.parametrize('result, name, is_function', (
        (f'{C_NAME}member{S_RESET}{C_EQUALS} =', 'member', False),
        (f'{C_NAME_FUNC}func{S_RESET}{C_EQUALS} =', 'func', True),
        (f'{S_PROTECTED}{C_NAME}_protected_member{S_RESET}{C_EQUALS} =', '_protected_member', False),
        (f'{S_PROTECTED}{C_NAME_FUNC}_protected_func{S_RESET}{C_EQUALS} =', '_protected_func', True),
))
def test_get_name_str(result: str, name: str, is_function: bool):
    assert get_name_str(name, is_function) == result


@pytest.mark.parametrize('result, obj', (
        (f'{C_PUNC}{{{C_CLS}Funcs{C_PUNC}}}', Funcs),
        (f'{C_PUNC}{{{C_CLS}Funcs{C_PUNC}}}', Funcs()),
        (f'{C_PUNC}{{{C_CLS}FuncsChild{C_PUNC}({C_CLS}Funcs{C_PUNC}, {C_CLS}OSError{C_PUNC}){C_PUNC}}}', FuncsChild),
        (f'{C_PUNC}{{{C_CLS}FuncsChild{C_PUNC}({C_CLS}Funcs{C_PUNC}, {C_CLS}OSError{C_PUNC}){C_PUNC}}}', FuncsChild()),
))
def test_get_type_str(result: str, obj: object):
    assert get_type_str(obj) == result


@pytest.mark.parametrize('result, obj', (
        (f'{C_VALUE}123', int(123)),
        (f'{C_VALUE}oops', Exception('oops')),
        (f"{C_VALUE}<class 'test_squiz.Funcs'>", Funcs),
))
def test_get_value_str(result: str, obj: object):
    assert get_value_str(obj) == result
