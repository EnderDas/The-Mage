#player
from BlueDB.blue2 import Blue
import inventory
import weapon
import armor
import frame

class Player:

    def __init__(self, name):
        self.name = name
        db = Blue(self.name)
        try:
            self.weapon = weapon._Weapon(db['weapon'])
            self.armor = armor._Armor(db['armor'])
            self.inventory = inventory._Inventory(db['inventory'])
            self.level = db['level']
            self.money = db['money']
            self.meta = db['meta']
        except:
            self.weapon = weapon.RandWeapon(1, "Starter Weapon")
            self.armor = armor.RandArmor(1, "Starter Armor")
            self.inventory = inventory.Inventory()
            self.level = 1
            self.money = 0
            self.meta = {}
            db.update(self.frame)

    def save(self):
        db = Blue(self.name)
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
        return frame.Frame(self).dict

    def __end__(self):
        self.save()
