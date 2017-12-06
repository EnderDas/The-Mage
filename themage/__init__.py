#The Mage

import os
import sys
import ujson
import time
import msvcrt

SOLD, LOCKED, BUYABLE = 'SOLD', 'LOCKED', 'BUYABLE'
counter = lambda x: {item: x.count(item) for item in x}


"""
Start
    -> Quit
    -> Play
        -> Saves
            -> (delete/edit save)
            -> (open/new save)
                -> Menu
                    -> Adventure
                        -> Travel
                        -> Arena
                        -> Dungeons
                        -> Scavenge
                    -> Inventory
                        -> Craft
                        -> Equipt
                        -> Edit
                        -> Throw-away
                    -> Shop/Forge
                        Shop
                            -> Sell
                            -> Buy
                            -> Barter
                        Forge
                            -> Buy/Forge
                            -> Sell
                            -> Quests
                            -> Upgrade
                            -> Dismantle
                    -> Mage Scroll
                        -> Upgrade
                        -> Edit
                        -> Quests
                    -> Save & Quit
                        <-
                    <-
                <-
            <-
        <-
    <-
"""

#os.system('mode 40,11')

def clear():
    os.system('mode 40,11')

def cost(obj):
    if hasattr(obj, '_Cost'):
        return obj._Cost()
    else:
        return obj

class Player:

    def __init__(self, slot):
        self.slot = slot
        self.file = f'data\\saves\\{slot}.json'
        self.load()

    def load(self):
        with open(self.file, 'r') as fp:
            data = ujson.load(fp)
        self.dict = data
        self.inventory = self.Inventory(self.dict['inventory'])
        self.name = self.dict['name']
        self.money = self.dict['money']
        self.level = self.dict['level']
        self.exp = self.dict['exp']
        self.weapon = Weapon(self.dict['weapon'])

    def save(self):
        with open(self.file, 'w') as fp:
            ujson.dump(self.dict, fp)

    def save_true(self):
        self.dict = self.get_dict()
        self.save()

    def get_dict(self):
        thing = {
            "name": self.name,
            "inventory": self.inventory.get_dict(),
            "money": self.money,
            "level": self.level,
            "exp": self.exp,
            "weapon": self.weapon.get_dict()
        }
        return thing

    class Inventory:

        def __init__(self, thing):
            self.dict = thing
            self.load()

        def load(self):
            self.items = []
            self.weapons = []
            for item in self.dict['items']:
                self.items.append(Item(item))

            for weapon in self.dict['weapons']:
                self.weapons.append(Weapon(weapon))

        def get_dict(self):
            thing = {
                "items": [items.get_dict() for items in self.items],
                "weapons": [weapons.get_dict() for weapons in self.weapons]
            }
            return thing

        def add_item(self, item_obj):
            self.items.append(item_obj)

        def get_items(self):
            for i in self.items:
                yield i

        def get_item_count(self, item_name):
            new_list = [i.name for i in self.items]
            if item_name in new_list:
                return new_list.count(item_name)
            else:
                return 0

        def get_items_count(self):
            new_list = [i.name for i in self.items]
            return counter(new_list)

        def add_weapon(self, weapon_obj):
            self.weapons.append(weapon_obj)

        def get_weapons(self):
            for i in self.weapons:
                yield i

        def get_weapon_count(self, weapon_name):
            new_list = [i.name for i in self.weapons]
            if weapon_name in new_list:
                return new_list.count(weapon_name)
            else:
                return 0

        def get_weapons_count(self):
            new_list = [i.name for i in self.weapons]
            return counter(new_list)

        def get_item(self, indice):
            return self.items[indice]

        def get_weapon(self, indice):
            return self.weapons[indice]

        def take_item(self, indice):
            item = self.items[indice]
            del self.items[indice]
            return item

        def take_weapon(self, indice):
            weapon = self.weapons[indice]
            del self.weapons[indice]
            return weapon

class Weapon:

    UPGRADES = {
        "sharp": {
            "upgrade": "attack",
            "id": 1,
            "effect": 1,
            "max": 10,
            "types": [
                "sword",
                "dagger",
                "spear"
            ]
        },
        "hardened": {
            "upgrade": "armor",
            "id": 2,
            "effect": 1,
            "max": 15,
            "types": [
                "sword",
                "dagger"
            ]
        },
        "plated": {
            "upgrade": "limb",
            "id": 3,
            "effect": 1,
            "max": 5,
            "types": [
                "sword",
                "mace"
                "javlin"
            ]
        },
        "braced": {
            "upgrade": "attack",
            "id": 4,
            "effect": 2,
            "max": 6,
            "types": [
                "bow",
                "javlin",
                "mace"
            ]
        },
        "treated": {
            "upgrade": "armor",
            "id": 5,
            "effect": 1,
            "max": 14,
            "types": [
                "bow",
                "javlin",
                "mace",
                "spear"
            ]
        }
    }
    TYPES = {
        "sword": 1,
        "bow": 2,
        "dagger": 2,
        "mace": 3,
        "javlin": 4,
        "spear": 3
    }

    def __init__(self, thing):
        self.dict = thing
        self.load()

    def load(self):
        self.name = self.dict['name']
        self.level = self.dict['level']
        self.exp = self.dict['exp']
        self.upgrades = dict(self.dict['upgrades'])
        self.type = self.dict['type']
        self.custom = self.dict.get('custom', False)
        self.quantity = self.dict.get('quantity', None)

    def _Cost(self):
        return int((self.level*2)+(5*len(self.upgrades))+(2*self.TYPES[self.type]) + (10 if self.custom is True else 0))

    @property
    def attack(self):
        attack = 0
        attack += self.TYPES[self.type]
        attack *= self.level
        if self.test_for_upg('sharp') is True:
            attack += self.upgrades['sharp']
        if self.test_for_upg('braced') is True:
            attack += (self.upgrades['braced']*2)
        return attack

    @property
    def limb(self):
        limb = 0
        limb += self.TYPES[self.type]
        limb = limb + (limb * (self.level//2))
        if self.test_for_upg("plated") is True:
            limb += self.upgrades['plated']
        return limb

    @property
    def armor(self):
        armor = 0
        if self.test_for_upg('hardened') is True:
            armor += self.upgrades['hardened']
        if self.test_for_upg('treated') is True:
            armor += self.upgrades['treated']
        return armor

    def test_for_upg(self, upg):
        if upg in self.upgrades.keys():
            return True
        else:
            return False

    def append_upg(self, upg):
        if self.test_for_upg(upg) is True:
            self.add_to_upg(upg)
        else:
            if self.type in self.UPGRADES[upg]['types']:
                self.upgrades[upg] = 1
            else:
                raise ValueError

    def add_to_upg(self, upg):
        if self.upgrades[upg] < self.UPGRADES[upg]['max']:
            self.upgrades[upg] += 1
        else:
            raise KeyError

    def check_level(self):
        if self.exp >= self.level*12:
            self.level += 1

    def get_dict(self):
        thing = {
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "type": self.type,
            "upgrades": self.upgrades,
            "cost": self._Cost(),
            "custom": self.custom,
        }
        return thing

class Item:

    TYPES = {
        "artifact": 4,
        "special": 8,
        "badge": 6,
        "potion": 5,
        "scroll": 10,
        "other": 3
    }
    MODIFIERS: {
        "weapon": 4,
        "health": 5,
        "armor": 3,
        "pickups": 7
    }

    def __init__(self, thing):
        self.dict = thing
        self.load()

    def load(self):
        self.name = self.dict['name']
        self.type = self.dict['type']
        self.desc = self.dict['desc']
        self.lore = self.dict['lore']
        self.mods = self._mods()

    def _mods(self):
        mods = self.dict['mods']
        for i in mods:
            pass

    def _Cost(self):
        return self.TYPE[self.type]*(i for i in [self.MODIFIERS[o['mod']] * o['amount'] for o in self.mods])

    def get_dict(self):
        thing = {
            "name": self.name,
            "type": self.type,
            "desc": self.desc,
            "lore": self.lore,
            "func": self.func,
            "cost": self._Cost()
        }
        return thing

class Armor: #Still Planning

    TYPES = {
        "cloth": 1,
        "iron": 3,
        "steel": 4,
        "strange": 6,
        "magic": 8,
        "holy": 9
    }

    TYPES_STRENGTH = {
        "soft": 1,
        "unsafe": 2,
        "sturdy": 3,
        "harder": 4,
        "hardest": 5,
        "strong": 6
    }

    def __init__(self, thing):
        self.dict = thing
        self.load()

    def load(self):
        self.name = self.dict['name']
        self.type = self.dict['type']
        self.level = self.dict['level']
        self.exp = self.dict['exp']
        self.stng = self.dict['stng']

    @property
    def defence(self):
        defence = 0
        defence += self.TYPES[self.type]
        defence *= self.TYPES_STRENGTH[self.stng]
        return defence

    def _Cost(self):
        return int((self.level*2)+(5+self.TYPES[self.type]))

    def get_dict(self):
        thing = {
            "name": self.name,
            "type": self.type,
            "stng": self.stng
        }
        return thing

class Npc:

    def __init__(self, name):
        self.file = f'data\\npc\\{name}.json'
        with open(self.file, 'r') as fp:
            self.dict = ujson.load(fp)
        self.name = name
        self.desc = self.dict['desc']
        self.merch = self.load_cycle()

    def get_dict(self):
        thing = {
            "name": self.name,
            "desc": self.desc,
            "items": [get_dict(item) for item in self.merch.items()],
            "weapons": [get_dict(weapon) for weapon in self.merch.weapons()]
        }
        return thing

    def load_cycle(self):
        items = [{'object': Item(item)} for item in self.dict['items']]
        weapons = [{'object': Weapon(weapon)} for weapon in self.dict['weapons']]
        return ShopCycle(items, weapons)

    def buy_item(self, indice, player):
        try:
            item = self.merch.item[indice]
            if player.money >= cost(item):
                self.merch.buy_item(indice)
                player.money -= cost(item)
                player.inventory.add_item(item)
                player.save_true()
            else:
                return False
        except:
            raise

    def buy_weapon(self, indice, player):
        try:
            weapon = self.merch.weapons[indice]
            if player.money >= cost(weapon):
                self.merch.buy_weapon(indice)
                player.money -= cost(weapon)
                player.inventory.add_weapon(weapon)
                player.save_true()
            else:
                return False
        except:
            raise

    def sell_item(self, indice, player):
        item = player.get_item(indice)
        player.money += cost(item)
        player.take_item(indice)
        player.save_true()
        self.merch.add_item(item)

    def sell_weapon(self, indice, player):
        weapon = player.get_weapon(indice)
        player.money += cost(weapon)
        player.take_weapon(indice)
        player.save_true()
        self.merch.add_weapon(weapon)

    @property
    def _items(self):
        if self.merch.items is None:
            return None
        else:
            for item in self.merch.items:
                yield item

    @property
    def _weapons(self):
        if self.merch.weapons is None:
            return None
        else:
            for weapon in self.merch.weapons:
                yield weapon

class ShopCycle: #for Npc

    def __init__(self, item_list=list(), weapon_list=list()):
        """
        item_list
            [
                {"object": artifact, "cost": cost(artifact), "status": BUYABLE}
                ... do that *400 more times ;)
            ]
        """
        self.items = item_list
        self.weapons = weapon_list
        if (item_list, weapon_list) == (None, None):
            raise

        #item_things
        def add_item(self, obj):
            self.items.append(obj)

        def add_weapon(self, obj):
            self.weapons.append(obj)

        def buy_item(self, indice):
            item = self.items[indice]
            del self.items[indice]
            return item

        def buy_weapon(self, indice):
            weapon = self.weapons[indice]
            del self.weapons[indice]
            return weapon

class Enemy:
    pass

sword = Weapon({
    "name": "Wood Sword",
    "level": 1,
    "exp": 0,
    "type": "sword",
    "upgrades": []
})

artifact = Item({
    "name": "Wood Idol",
    "type": "artifact",
    "desc": "Small odd object.",
    "lore": None,
    "mods": [
        {"mod": "weapon", "amount": 1}
    ]
})

p = Player("1")

class Game:
    pass
