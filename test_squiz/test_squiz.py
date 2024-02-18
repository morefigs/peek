from abc import ABC
from threading import Thread
from datetime import datetime

import pytest

from squiz import _in_stdlib


class Foo:
    pass


@pytest.mark.parametrize('result, cls', (
        # Standard classes
        (True, int),
        (True, str),
        (True, ABC),
        (True, Thread),
        (True, datetime),
        (True, ZeroDivisionError),

        # Standard class instances
        (True, 123),
        (True, 'asdf'),
        (True, ABC()),
        (True, Thread()),
        (True, datetime.now()),
        (True, ZeroDivisionError('oops')),

        # Non-standard classes
        (False, Foo),

        # Non-standard class instances
        (False, Foo())
))
def test_in_stdlib(result: bool, cls: type):
    assert _in_stdlib(cls) is result
