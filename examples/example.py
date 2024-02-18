from squiz import squiz


class Bar:
    @property
    def bar(self):
        return self._bar

    def __init__(self):
        self._bar = {1: 'a', 2: 'b'}


class Foo:
    class InnerFoo:
        inner_foo = ['inner', 'foo']

    __foo = 12
    _foo = 34

    def __init__(self):
        self.bar = Bar()
        self.bar_cls = Bar

    def method(self):
        pass

    @staticmethod
    def static_method():
        pass


squiz(Foo())
