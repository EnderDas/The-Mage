#item

import frame

"""
Item
| name :str:
| buff :list:
|_cost :int:

Current Buffs
power
damage
"""

class Item:

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Item')
        self.buff = kwargs.get('buff', [])
        self.cost = kwargs.get('cost', 0)

    @property
    def frame(self):
        return frame.Frame(self).dict

class _Item(Item):

    def __init__(self, _dict):
        _name = _dict['name']
        _buff = _dict['buff']
        _cost = _dict['cost']
        super().__init__(
            name = _name,
            buff = _buff,
            cost = _cost
        )
