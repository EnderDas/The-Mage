#inventory
import frame
from weapon import _Weapon
from armor import _Armor

class Inventory:

    def __init__(self, **kwargs):
        self.weapons = [_Weapon(wep) for wep in kwargs.get('weapons', [])]
        self.armors = [_Armor(arm) for arm in kwargs.get('armors', [])]

    @property
    def frame(self):
        return frame.Frame(self).dict

class _Inventory(Inventory):

    def __init__(self, _dict):
        _weapons = _dict['weapons']
        _armors = _dict['armors']
        super().__init__(
            weapons = _weapons,
            armors = _armors
        )
