from random import uniform
from item import Item
import frame
"""
Weapon
| name :str:
| level :int:
| style :Style object:
|_body :Body object:

Style
| name :str:
| type :str:
| weight :int:
|_price :int:
"""

def rng(start = 0, stop = 5):
    return round(uniform(start, stop))

class Style(Item):
    TYPES = [
        0, #Fast
        1, #Patient
        2, #Strategic

    ]
    NAMES = [
        "Fast",
        "Patient",
        "Strategic"
    ]
    def __init__(self, **kwargs):
        self.type = kwargs.get('type', self.TYPES[0])
        _name = self.NAMES[self.type]
        _cost = kwargs.get('cost', 0)
        self.weight = kwargs.get('weight', 50)
        super().__init__(
            name = _name,
            buff = [],
            cost = _cost
        )

class _Style(Style):

    def __init__(self, _dict):
        _name = _dict['name']
        _cost = _dict['cost']
        _type = _dict['type']
        _weight = _dict['weight']
        _price = _dict['price']
        super().__init__(
            name = _name,
            cost = _cost,
            type = _type,
            weight = _weight
        )

class RandStyle(Style):

    def __init__(self, )

class Weapon:

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Weapon')
        self.level = kwargs.get('level', 1)
        self.style = kwargs.get('style', None)
        self.skills = kwargs.get('skills', {})
        self.power = kwargs.get('power', 1)

    @property
    def frame(self):
        return frame.Frame(self).dict

class _Weapon(Weapon):

    def __init__(self, _dict):
        _name = _dict['name']
        _level = _dict['level']
        _style = _dict['style']
        _body = _dict['body']
        _power = _dict['power']
        super().__init__(
            name = _name,
            level = _level,
            style = _Style(_style),
            body = _Body(_body),
            power = _power
        )

class RandWeapon(Weapon):

    def __init__(self, level, name = None):
        pass
