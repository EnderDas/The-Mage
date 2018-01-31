#skill
from base import MAX_LEVEL
from random import uniform
import frame
"""
Skill
| name
| type
|_buff
"""

TYPES = [
    "Normal",
    "Power",
    "Effect"
]

NAME = {
    "Normal": [
        "Hit",
        "Slash",
        "Swing"
    ],
    "Power": [
        "Bash",
        "Rush",
        "Charge"
    ],
    "Effect": [
        "Stab",
        "Taunt",
        "Distract"
    ]
}

STYLE = {
    0: [
        "Basic",
        "Speedy",
        "Quick"
    ],
    1: [
        "Steady",
        "Accurate",
        "Damaging"
    ],
    2: [
        "Hard",
        "Stagering",
        "Powerful"
    ]
}
class Skill:

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Skill")
        self.type = kwargs.get("type", 0)
        self.buff = kwargs.get("buff", 1)

    @property
    def frame(self):
        return frame.Frame(self).dict

class _Skill(Skill):

    def __init__(self, _dict):
        _name = _dict['name']
        _type = _dict['type']
        _buff = _dict['buff']
        super().__init__(
            name = _name,
            type = _type,
            buff = _buff
        )

def rng(start = 0, stop = 5):
    return round(uniform(start, stop))

class RandSkill(Skill):

    def __init__(self, style):
        _type = rng(stop=2)
        _name = self._make(style, _type)
        _type = TYPES[_type]
        _buff = rng(start=1, stop=3)
        super().__init__(
            name = _name,
            type = _type,
            buff = _buff
        )

    def _make(self, style, _type):
        _name = rng(stop=2)
        _name2 = rng(stop=2)
        return f"{STYLE[style][_name2]} {NAME[TYPES[_type]][_name]}"
