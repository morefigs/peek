from squiz import squiz


class Data:
    @property
    def contents(self):
        return self._contents

    def __init__(self):
        self._contents = {1: 'a', 2: 'b'}


class Example:
    _foo = 'FOO'

    def __init__(self):
        self.bar = 123
        self.data = Data()


squiz(Example())
