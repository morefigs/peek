from abc import ABC
from threading import Thread
from datetime import datetime
from functools import partial

import pytest

from squiz.squiz import S_INHERITED, S_RESET, C_NAME, C_NAME_FUNC, C_EQUALS, C_PUNC, C_CLS, C_VALUE, get_cls, \
    in_stdlib, is_function_like, is_member_of, get_members, get_name_str, get_type_str, get_value_str


class GetCls: pass


@pytest.mark.parametrize('obj, type_', (
        (object, object),
        (object(), object),
        (int, int),
        (123, int),
        (str, str),
        ('asdf', str),
        (GetCls, GetCls),
        (GetCls(), GetCls),
))
def test_get_cls(obj: object, type_: type):
    assert get_cls(obj) is type_


class InStdLib: pass


@pytest.mark.parametrize('result, obj', (
        (True, object),
        (True, int),
        (True, str),
        (True, ABC),
        (True, Thread),
        (True, datetime),
        (True, ZeroDivisionError),

        (True, object()),
        (True, 123),
        (True, 'asdf'),
        (True, ABC()),
        (True, Thread()),
        (True, datetime.now()),
        (True, ZeroDivisionError('oops')),

        (False, InStdLib),
        (False, InStdLib())
))
def test_in_stdlib(result: bool, obj: type):
    assert in_stdlib(obj) is result


def func(): pass


class IsFunctionLikeFixture:
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

    @property
    def getset(self):
        return

    @getset.setter
    def getset(self, value):
        pass


class IsFunctionLikeChildFixture(IsFunctionLikeFixture): pass


@pytest.mark.parametrize('result, obj', (
        (True, func),

        (True, IsFunctionLikeFixture.partial_),
        (True, IsFunctionLikeFixture.lambda_),
        (True, IsFunctionLikeFixture.__init__),
        (True, IsFunctionLikeFixture.func),
        (True, IsFunctionLikeFixture.func_class),
        (True, IsFunctionLikeFixture.func_static),
        (True, IsFunctionLikeFixture().partial_),
        (True, IsFunctionLikeFixture().lambda_),
        (True, IsFunctionLikeFixture().__init__),
        (True, IsFunctionLikeFixture().func),
        (True, IsFunctionLikeFixture().func_class),
        (True, IsFunctionLikeFixture().func_static),

        (True, IsFunctionLikeChildFixture.partial_),
        (True, IsFunctionLikeChildFixture.lambda_),
        (True, IsFunctionLikeChildFixture.__init__),
        (True, IsFunctionLikeChildFixture.func),
        (True, IsFunctionLikeChildFixture.func_class),
        (True, IsFunctionLikeChildFixture.func_static),
        (True, IsFunctionLikeChildFixture().partial_),
        (True, IsFunctionLikeChildFixture().lambda_),
        (True, IsFunctionLikeChildFixture().__init__),
        (True, IsFunctionLikeChildFixture().func),
        (True, IsFunctionLikeChildFixture().func_class),
        (True, IsFunctionLikeChildFixture().func_static),

        (False, 123),
        (False, 'asdf'),
        (False, IsFunctionLikeFixture),
        (False, IsFunctionLikeFixture()),
        (False, IsFunctionLikeFixture.getset),
        (False, IsFunctionLikeFixture().getset),
))
def test_is_function_like(result: bool, obj: object):
    assert is_function_like(obj) == result


class IsMemberOfFixture:
    foo = 123


@pytest.mark.parametrize('result, name, classes', (
        (True, 'end_lineno', (SyntaxError,)),
        (True, 'foo', (IsMemberOfFixture,)),
        (True, 'end_lineno', (SyntaxError, IsMemberOfFixture)),
        (True, 'foo', (SyntaxError, IsMemberOfFixture)),

        (False, 'nope', (SyntaxError, )),
        (False, 'nope', (SyntaxError, IsMemberOfFixture)),
))
def test_is_member_of(result: bool, name: str, classes: tuple[type, ...]):
    assert is_member_of(name, classes) == result


class Base:
    foo = None


class Klass(Base, AttributeError):
    bar = None


@pytest.mark.parametrize('result, obj, include_inherited, include_inherited_stdlib, include_magics', (
        ([
             ('bar', Klass.bar, False),
         ], Klass(), False, False, False),
        ([
             ('bar', Klass.bar, False),
             ('foo', Klass.bar, True),
         ], Klass(), True, False, False),
        ([
             ('bar', Klass.bar, False),
         ], Klass, False, False, False),
        ([
             ('bar', Klass.bar, False),
             ('foo', Klass.bar, True),
         ], Klass, True, False, False),
        ([
             ('bar', Klass.bar, False),
         ], Klass, False, True, False),
        ([
             ('bar', Klass.bar, False),
         ], Klass, False, False, True),
        ([
             ('add_note', BaseException.add_note, True),
             ('args', BaseException.args, True),
             ('bar', None, False),
             ('foo', None, True),
             ('name', AttributeError.name, True),
             ('obj', AttributeError.obj, True),
             ('with_traceback', BaseException.with_traceback, True),
         ], Klass, True, True, False),
        ([
             ('__module__', 'test_squiz', True),
             ('__weakref__', Klass.__weakref__, True),
             ('bar', None, False),
             ('foo', None, True),
         ], Klass, True, False, True),
))
def test_get_members(result: list[tuple[str, object]],
                     obj: object,
                     include_inherited: bool,
                     include_inherited_stdlib: bool,
                     include_magics: bool):
    assert get_members(obj, include_inherited, include_inherited_stdlib, include_magics) == result


def test_get_members_all():
    names = [name for name, _, _ in get_members(Klass)]
    for name in ('foo', 'bar', 'add_note', 'name', '__module__', '__weakref__', '__delattr__', '__init__'):
        assert name in names


@pytest.mark.parametrize('result, name, is_function, is_inherited', (
        (f'{C_NAME}member{S_RESET}{C_EQUALS} =', 'member', False, False),
        (f'{C_NAME_FUNC}func{S_RESET}{C_EQUALS} =', 'func', True, False),
        (f'{S_INHERITED}{C_NAME}member{S_RESET}{C_EQUALS} =', 'member', False, True),
        (f'{S_INHERITED}{C_NAME_FUNC}func{S_RESET}{C_EQUALS} =', 'func', True, True),
))
def test_get_name_str(result: str, name: str, is_function: bool, is_inherited: bool):
    assert get_name_str(name, is_function, is_inherited) == result


class GetTypeStr: pass
class GetTypeStrChild(GetTypeStr, OSError): pass


@pytest.mark.parametrize('result, obj', (
        (f'{C_PUNC}{{{C_CLS}GetTypeStr{C_PUNC}}}', GetTypeStr),
        (f'{C_PUNC}{{{C_CLS}GetTypeStr{C_PUNC}}}', GetTypeStr()),
        (f'{C_PUNC}{{{C_CLS}GetTypeStrChild{C_PUNC}({C_CLS}GetTypeStr{C_PUNC}, {C_CLS}OSError{C_PUNC}){C_PUNC}}}',
         GetTypeStrChild),
        (f'{C_PUNC}{{{C_CLS}GetTypeStrChild{C_PUNC}({C_CLS}GetTypeStr{C_PUNC}, {C_CLS}OSError{C_PUNC}){C_PUNC}}}',
         GetTypeStrChild()),
))
def test_get_type_str(result: str, obj: object):
    assert get_type_str(obj) == result


class GetValueStr: pass


@pytest.mark.parametrize('result, obj', (
        (f'{C_VALUE}123', int(123)),
        (f'{C_VALUE}oops', Exception('oops')),
        (f"{C_VALUE}<class 'test_squiz.GetValueStr'>", GetValueStr),
))
def test_get_value_str(result: str, obj: object):
    assert get_value_str(obj) == result
