#armor
from random import uniform as _uniform
from .frame import Frame

"""
Armor
|  name
|  level
|_ strength
"""

def rng(start = 0, stop = 5):
    return round(_uniform(start, stop))

class Armor:

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Armor")
        self.level = kwargs.get("level", 1)
        self.strength = kwargs.get("strength", 5)

    @property
    def frame(self):
        return Frame(self).dict

class _Armor(Armor):

    def __init__(self, _dict):
        _name = _dict['name']
        _level = _dict['level']
        _strength = _dict['strength']
        super().__init__(
            name = _name,
            level = _level,
            strength = _strength
        )

class RandArmor(Armor):

    def __init__(self, level, name = None):
        _name = name
        _level = rng(stop=level+1) if level < 20 else 20
        _strength = rng(start=_level+5, stop=_level+10)
        super().__init__(
            name = _name,
            level = _level,
            strength = _strength
        )
