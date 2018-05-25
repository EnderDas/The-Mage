#player
from BlueDB.blue2 import Blue as _Blue
from .inventory import Inventory, _Inventory
from .weapon import _Weapon, RandWeapon
from .armor import _Armor, RandArmor
from .frame import Frame

class Player:

    def __init__(self, name):
        self.name = name
        db = _Blue(self.name)
        try:
            self.weapon = _Weapon(db['weapon'])
            self.armor = _Armor(db['armor'])
            self.inventory = _Inventory(db['inventory'])
            self.level = db['level']
            self.money = db['money']
            self.meta = db['meta']
        except:
            self.weapon = RandWeapon(1, "Starter Weapon")
            self.armor = RandArmor(1, "Starter Armor")
            self.inventory = Inventory()
            self.level = 1
            self.money = 0
            self.meta = {}
            db.update(self.frame)

    def save(self):
        db = _Blue(self.name)
        db.update(self.frame)

    @property
    def attack(self):
        attack = self.weapon.power
        attack = attack + (attack * ((self.level+1)//2))
        return attack

    @property
    def defense(self):
        defense = self.armor.strength
        defense = defense + (defense * ((self.level+1)//2))
        return defense

    @property
    def frame(self):
        return Frame(self).dict

    def __end__(self):
        self.save()
