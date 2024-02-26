from squiz import squiz


class Character:
    def __init__(self, name):
        self.name = name

    def say_ni(self):
        pass


class Squire(Character):
    pass


class King(Character):
    def __init__(self, name, squire):
        super().__init__(name)
        self.squire = squire

    def seek_grail(self):
        pass


arthur = King('Arthur', Squire('Patsy'))
squiz(arthur)
