from squiz import squiz


class Data:
    @property
    def contents(self):
        return self._contents

    def __init__(self):
        self._contents = {1: 'a', 2: 'b'}


class Example:
    _foo = 'FOO'
    __bar = 'BAR'

    def __init__(self):
        self.data = Data()
        self.data_cls = Data

    class Inner:
        pass


squiz(Example())
