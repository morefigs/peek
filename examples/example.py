from squiz import squiz


class Quest:
    def __init__(self, aim: str, completed: bool):
        self.aim = aim
        self.completed = completed


class Person:
    def __init__(self):
        self.name = 'Arthur'
        self.occupation = 'King'
        self.quest = Quest('To find the Holy Grail', False)

print('>>> from squiz import squiz')
print('>>> squiz(arthur)')
print()

squiz(Person())
