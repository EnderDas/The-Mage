from random import uniform
from item import Item
from skill import RandSkill, _Skill
import base
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

def differ(val, mval, itera, tira):
    _diff = {i+1: (i)*(mval//itera) for i in range(tira)}
    value = rng(start = 1, stop=tira)
    if _diff[value] <= val:
        return value
    else:
        return differ(val, mval, itera, tira)

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
        self.skills = kwargs.get('skills', None)
        _name = self.NAMES[self.type]
        _cost = kwargs.get('cost', 0)
        super().__init__(
            name = _name,
            buff = [],
            cost = _cost
        )

class _Style(Style):

    def __init__(self, _dict):
        _cost = _dict['cost']
        _type = _dict['type']
        _skills = _dict['skills']
        super().__init__(
            cost = _cost,
            type = _type,
            skills = [_Skill(skill) for skill in _skills]
        )

class RandStyle(Style):

    def __init__(self, level):
        _type = Style.TYPES[differ(level, base.MAX_WEP_LEVEL, 3, 3)]
        _cost = rng(stop = level) * (5 + rng(stop = level + 2))
        _skills = [RandSkill(_type) for i in range(2)]
        super().__init__(
            cost = _cost,
            type = _type,
            skills = _skills
        )

class Weapon:

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Weapon')
        self.level = kwargs.get('level', 1)
        self.style = kwargs.get('style', None)
        self.power = kwargs.get('power', 1)

    @property
    def skills(self):
        return self.style.skills

    @property
    def frame(self):
        return frame.Frame(self).dict

class _Weapon(Weapon):

    def __init__(self, _dict):
        _name = _dict['name']
        _level = _dict['level']
        _style = _dict['style']
        _power = _dict['power']
        super().__init__(
            name = _name,
            level = _level,
            style = _Style(_style),
            power = _power
        )

class RandWeapon(Weapon):

    def __init__(self, level, name = None):
        _name = name
        _level = rng(stop=level) if level <= 20 else 20
        _style = RandStyle(_level)
        _power = rng(start=_level+5, stop=_level+10)
        super().__init__(
            name = _name,
            level = _level,
            style = _style,
            power = _power
        )
