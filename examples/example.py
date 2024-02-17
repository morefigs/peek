from peek import peek


class Data:
    def __init__(self):
        self.data = {1: 'a', 2: 'b'}


class Example:
    _foo = 'FOO'

    def __init__(self):
        self.bar = 123
        self.internal = Data()


peek(Example())
