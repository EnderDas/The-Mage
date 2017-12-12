#The Mage

import os
import sys
import ujson
import time
import msvcrt

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

"""
things



* Move all [load] functions to [__init__] and use kwargs or args
** Add controller class to change and edit player properties easier
*** Combine [Inventory] & [ShopCycle] to one real class
**** Broken, compares classes hashes which is bad because exp isnt accounted
***** Remove because inexplicite exp break
****** Cost should be changed to an @property

! Will be changed or removed
!! Chance to be deprecated and/or removed

^ A citation on this [object/func] is involved with the above [object/func]

Player **
    |- slot
    |- name
    |- level
    |- money
    |- weapon
    |_ Inventory ***
        |- weapons
        |_ items

    <Player>
    load - loads dict*
    save - saves dict**
    !! save_true - same as save but formats the dict
    !! get_dict - formats a dict with class properties (for saving)

    <Player.Inventory>
    load :: loads dict*
    !! get_dict :: formats a dict with class properties (for saving)
    add_item :: adds an item to the players inventory
    !! get_items :: returns a generator with items
    !! get_item_count :: returns count of item ****
    !! get_items_count :: returns count of items in dict ****
    add_weapon :: adds a weapon to the players inventory
    !! get_weapons :: returns a generator with weapons
    !! get_weapon_count :: returns count of weapon ****
    !! get_weapons_count :: returns count of weapons in dict ****
    get_item :: returns item using indice
    get_weapon :: returns weapon using indice
    !! take_item :: removes and returns item object
    !! take_weapon :: removes and returns weapon object

Weapon
    |- name
    |- level
    |- exp
    |- upgrades
    |- type
    |- custom
    |_ ! quantity *****

    <Weapon>
    load :: loads dict *
    _Cost :: returns item cost (use [cost]) ******
    attack :property: returns attack of weapon
    limb :property: returns limb of weapon
    armor :property: return armor of weapon
    !! test_for_upg :: True if (weapon has upgrade) else False
    !! append_upg :: adds new upgrade
    !! add_to_upg :: adds to pre-existing upgrade and if no pre-existsing
                     upgrade; will [append_upg] said upgrade
    !! check_level :: levels up weapon if weapons exp has met requirements
    !! get_dict :: formats a dict with class properties (for saving)

Item
    |- name
    |- type
    |- ! desc
    |- !^ lore
    |_ ! mods


NEW THINGS

Player
    |- name
    |- health
    |- level
    |- energy
    |- weapon
    |- money
    |- attack (property)
    |- defence (property)
    |_ skills (property)

Inventory
    |- weapon
    |- armor
    |- weapons
    |- items
    |_ armors

Map
    |- matrix
    |- x_cord
    |- y_cord
    |_ posititon

Weapon
    |- name
    |- type
    |- level
    |- modifiers
    |- cost (property)
    |- attack (property)
    |- skills (property)
    |_ defence (property)

Item
    |- name
    |- type
    |- modifiers
    |_ cost (property)

Armor
    |- name
    |- type
    |- level
    |- modifiers
    |- cost (property)
    |_ defence (property)

Enemy
    |- name
    |- level
    |- weapon
    |- attack (property)
    |- skills (property)
    |_ defence (property)

Skill
    |- name
    |- weapon
    |- range
    |_ description

Wood type = 2
Level = 3
Defence = 5
Modifiers = 2

 2 * 5 = 10
 10 + 3 = 13
 13 + 5 = 18
 18 + (18 // 2) = 27
 cost is 27

1 = 2 1/2 = 4 1/4 = 8 1/8
1/2 = 2 1/4 = 4 1/8
1/4 = 2 1/8

WEAPON ATTACK PROPERTIES

"""
class _Player:

    def __init__(self, name):
        self.file = f'players\\{name}.json'
        self.name = name
        with open(self.file, 'r') as fp:
            self.dict = ujson.load(fp)
        self.health = self.dict['health']
        self.level = self.dict['level']
        self.energy = self.dict['energy']
        _equipted = self.dict['equipted']
        self.equipted = self._Equipted(self, _equipted)
        self.money = self.dict['money']
        self.inventory = _Inventory(self.dict['inventory'], self)

    @property
    def frame(self):
        frame = {
            "name": self.name,
            "health": self.health,
            "level": self.level,
            "energy": self.energy,
            "equipted": self.equipted.frame,
            "money": self.money,
            "inventory": self.inventory.frame
        }
        return frame

    @property
    def attack(self):
        #get equipted item modifiers
        return self.equipted.attack * self.level

    @property
    def skills(self):
        return self.equipted.skills

    @property
    def defence(self):
        return int(self.equipted.defence)

    class _Equipted:

        def __init__(self, player, _dict):
            self.player = player
            self.dict = _dict
            self.armor = ArmorSet(self.dict['armor'])
            self.item_one = Item(self.dict['item_one'])
            self.item_two = Item(self.dict['item_two'])
            self.item_three = Item(self.dict['item_three'])
            self.weapon = Weapon(self.dict['weapon'])

        @property
        def attack(self):
            attack = self.weapon.attack
            if 'attack' in self.item_one.modifiers:
                attack += self.item_one.modifiers['attack']
            if 'attack' in self.item_two.modifiers:
                attack += self.item_two.modifiers['attack']
            if 'attack' in self.item_three.modifiers:
                attack += self.item_three.modifiers['attack']
            return attack

        @property
        def defence(self):
            defence = self.weapon.defence
            defence += self.armor.defence
            if 'defence' in self.item_one.modifiers:
                defence += self.item_one.modifiers['defence']
            if 'defence' in self.item_two.modifiers:
                defence += self.item_two.modifiers['defence']
            if 'defence' in self.item_three.modifiers:
                defence += self.item_three.modifiers['defence']
            return defence

        @property
        def skills(self):
            skills = self.weapon.skills
            return skills

        @property
        def frame(self):
            frame = {
                "armor": self.armor.frame,
                "item_one": self.item_one.frame,
                "item_two": self.item_two.frame,
                "item_three": self.item_three.frame,
                "weapon": self.weapon.frame
            }
            return frame

class _Inventory:

    def __init__(self, _dict, player, **kwargs):
        self.dict = _dict
        self.player = player
        self.items = [Item(item) for item in self.dict['items']]
        self.weapons = [Weapon(weapon) for weapon in self.dict['weapons']]
        self.armors = [Armor(armor) for armor in self.dict['armors']]

    @property
    def frame(self):
        frame = {
            "items": [item.frame for item in self.items],
            "weapons": [weapon.frame for weapon in self.weapons],
            "armors": [armor.frame for armor in self.armors]
        }

    #buying things
    def buy(self, _type, indice, other):
        types = {
            "items": self.items,
            "weapons": self.weapons,
            "armors": self.armors
        }
        obj_cost = types[_type][indice].cost
        if other.money >= obj_cost:
            other.money -= obj_cost
            other.inventory.put(_type, types[_type][indice])
            del types[_type][indice]
        else:
            raise

    def sell(self, _type, indice, other):
        types = {
            "items": other.inventory.items,
            "weapons": other.inventory.weapons,
            "armors": other.inventory.armors
        }
        obj_cost = types[_type][indice].cost
        if self.player.money >= obj_cost:
            self.player.money -= obj_cost
            self.put(_type, types[_type][indice])
            del types[_type][indice]
        else:
            raise

    def put(self, _type, obj):
        types = {
            "items": self.items,
            "weapons": self.weapons,
            "armors": self.armors
        }
        types[_type].append(obj)

class _Map:

    def __init__(self, size, matrix):
        self.size = size
        self.x = 0
        self.y = 0
        self.matrix = matrix

    @property
    def place(self):
        return self.matrix[self.y][self.x]

    def move(self, x, y):
        try:
            self.matrix[y][x]
            self.x = x
            self.y = y
        except:
            pass

    def north(self): #cord plane "up"
        self.move(self.x, self.y+1)

    def south(self): #cord plane "down"
        self.move(self.x, self.y-1)

    def east(self): #cord plane "right"
        self.move(self.x+1, self.y)

    def west(self): #cord plane "left"
        self.move(self.x-1, self.y)

class _Weapon:

    DEFAULT_TYPE = 1
    DEFAULT_MATERIAL = 1
    TYPES = {
        1: "sword",
        2: "bow",
        3: "spear",
        4: "mace",
        5: "dagger",
        6: "broadsword",
        7: "repeater",
        8: "staff"
    }
    TYPE_C = {
        1: 2,
        2: 3,
        3: 4,
        4: 6,
        5: 4,
        6: 7,
        7: 10,
        8: 12
    }
    MATERIALS = {
        1: "wood",
        2: "iron",
        3: "steel",
        4: "magic",
        5: "stone",
        6: "glass",
        7: "compound",
        8: "atomic"
    }
    MATERIAL_C = {
        1: 1,
        2: 3,
        3: 5,
        4: 7,
        5: 4,
        6: 5,
        7: 8,
        8: 10
    }

    def __init__(self, *args, **kwargs):
        self.name = args[0]
        self.type = kwargs.get("type", self.DEFAULT_TYPE)
        self.level = kwargs.get("level", 1)
        self.modifiers = kwargs.get("modifiers", {})
        self.material = kwargs.get("material", self.DEFAULT_MATERIAL)
        self._unloaded_skills = kwargs.get("skills", None)

    @property
    def frame(self):
        frame = {
            "name": self.name,
            "type": self.type,
            "level": self.level,
            "modifiers": self.modifiers,
            "material": self.material,
            "skills": [skill.frame for skill in self.skills]
        }

    @property
    def attack(self):
        attack = self.TYPE_C[self.type] * 2
        attack += self.MATERIAL_C[self.material]
        attack += self.level * 2
        if "attack" in self.modifiers.keys():
            attack += self.modifiers['attack']
        return attack

    @property
    def skills(self):
        skills = _SkillLoader(self._unloaded_skills, self)
        return skills.skills

    @property
    def defence(self):
        defence = self.MATERIAL_C[self.material] * 2
        if "defence" in self.modifiers.keys():
            defence += self.modifiers['defence']
        return defence

    @property
    def cost(self):
        cost = self.TYPE_C[self.type] * 2
        cost += self.level
        cost += self.MATERIALS[self.material]
        cost = cost + (cost // len(self.modifiers))
        return cost

class Weapon(_Weapon):

    def __init__(self, _dict):
        self.dict = _dict
        super().__init__(
            self.dict['name'],
            type=self.dict['type'],
            level=self.dict['level'],
            modifiers=self.dict['modifiers'],
            materials=self.dict['material'],
            skills=self.dict['skills']
        )

class _Item:

    DEFAULT_TYPE = 1
    TYPES = {
        "artifact": 1,
        "medal": 2,
        "banner": 3,
        "material": 4,
        "part": 5,
        "scroll": 6,
        "book": 7,
        "other": 8
    }
    TYPES_C = {
        1: 3,
        2: 4,
        3: 6,
        4: 2,
        5: 3,
        6: 8,
        7: 10,
        8: 1
    }

    def __init__(self, *args, **kwargs):
        self.name = args[0]
        self.type = kwargs.get("type", self.DEFAULT_TYPE)
        self.lore = kwargs.get("lore", None)
        self.modifiers = kwargs.get("modifiers", {})

    @property
    def frame(self):
        frame = {
            "name": self.name,
            "type": self.type,
            "lore": self.lore,
            "modifiers": self.modifiers
        }
        return frame

    @property
    def cost(self):
        cost = 2
        cost *= self.TYPES_C[self.type]
        cost += len(self.modifiers)
        return cost

class Item(_Item): #might make _Item for explicite obj creation

    def __init__(self, _dict):
        self.dict = _dict
        super().__init__(
            self.dict['name'],
            type=self.dict['type'],
            lore=self.dict['lore'],
            modifiers=self.dict['modifiers']
        )

class _Armor:

    DEFAULT_MATERIAL = 1
    DEFAULT_TYPE = 1
    TYPES = {
        1: "head",
        2: "torso",
        3: "arms",
        4: "legs"
    }
    TYPES_C = {
        1: 3,
        2: 5,
        3: 2,
        4: 2
    }
    MATERIALS = {
        1: "cloth",
        2: "metal",
        3: "glass",
        4: "magic"
    }
    MATERIALS_C = {
        1: 2,
        2: 4,
        3: 3,
        4: 6
    }
    def __init__(self, *args, **kwargs):
        self.name = args[0]
        self.type = kwargs.get("type", self.DEFAULT_TYPE)
        self.material = kwargs.get("material", self.DEFAULT_MATERIAL)
        self.level = kwargs.get("level", 1)
        self.modifiers = kwargs.get("modifiers", [])

    @property
    def frame(self):
        frame = {
            "name": self.name,
            "type": self.type,
            "material": self.material,
            "level": self.level,
            "modifiers": self.modifiers
        }
        return frame

    @property
    def cost(self):
        cost = self.TYPE_C[self.type]
        cost += self.MATERIAL_C[self.material]
        cost += self.level
        return cost

    @property
    def defence(self):
        defence = self.TYPES_C[self.type]
        defence += self.MATERIALS_C[self.material]
        defence /= 2
        if "defence" in self.modifiers.keys():
            defence += self.modifiers['defence']
        return defence

class Armor(_Armor):

    def __init__(self, _dict):
        self.dict = _dict
        super().__init__(
            self.dict['name'],
            type=self.dict['type'],
            material=self.dict['material'],
            level=self.dict['level'],
            modifiers=self.dict['modifiers']
        )

class ArmorSet:

    def __init__(self, _dict):
        self.dict = _dict
        _head = self.dict['head']
        _torso = self.dict['torso']
        _arms = self.dict['arms']
        _legs = self.dict['legs']
        self.head = Armor(_head)
        self.torso = Armor(_torso)
        self.arms = Armor(_arms)
        self.legs = Armor(_legs)

    @property
    def defence(self):
        defence = self.head.defence
        defence += self.torso.defence
        defence += self.arms.defence
        defence += self.legs.defence
        return defence

    @property
    def frame(self):
        frame = {
            "head": self.head.frame,
            "torso": self.torso.frame,
            "arms": self.arms.frame,
            "legs": self.legs.frame
        }
        return frame

class _Enemy:
    pass
class _Npc:
    pass

class _Skill:

    def __init__(self, name, player, _range, desc, buff = 0):
        self.name = name
        self.player = player
        self.range = _range
        self.desc = desc
        self.buff = buff

    @property
    def attack(self):
        attack = self.player.attack
        new = random.randint(attack - self.range, attack + self.buff)
        attack = new
        return new

    @property
    def frame(self):
        frame = {
            "name": self.name,
            "range": self.range,
            "desc": self.desc,
            "buff": self.buff
        }
        return frame

class _SkillLoader: #can probably make this a function that returns list

    def __init__(self, _dict, player):
        self.skills = []
        for i in _dict:
            self.skills.append(_Skill(i['name'], player, i['range'], i['desc'], i['buff']))

# everything new goes ^ up there

#os.system('mode 40,11')

def clear():
    os.system('mode 40,11')

p = _Player("Player")
