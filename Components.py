# This file is to factory create new units, player characters or not. This includes, but is not limited to Monsters,
# Robots, Civilians, Drones and Daemons.

# System Components


class Position:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y


class Render:
    def __init__(self, value, Tile, Background):
        self.value = value
        self.Tile = Tile
        self.Background = Background

# Character / 'Unit' components


class Name:
    def __init__(self, value):
        self.value = value


class Player:
    def __init__(self):
        return


class Entity:
    def __init__(self):
        return


class Item:
    def __init__(self):
        return


class Health:
    def __init__(self, value):
        self.value = value


class Wounds:
    def __init__(self, value):
        self.value = value


class Action_Points:
    def __init__(self, value):
        self.value = value


class Escalation_Points:
    def __init__(self, value):
        self.value = value


class Speed:
    def __init__(self, value):
        self.value = value


class Hostile:
    def __init__(self, value):
        self.value = value


class Alive:
    def __init__(self, value):
        self.value = value


class Move_Through:
    def __init__(self):
        return


class Can_See:
    def __init__(self, value):
        self.value = value


class Can_Move:
    def __init__(self, value):
        self.value = value


class Can_Talk:
    def __init__(self, value):
        self.value = value


class Skills:
    def __init__(self, Land_Vehicle, Air_Vehicle, Sea_Vehicle, Space_Vehicle, Battle_Suit, Computer, Medical,
                 Engineering, Chemistry, Celestial, Local, Business, Nature, Combat, Convince, Entertain, Negotiation,
                 Sense_Motive, Intimidate, Sneak, Climb, Athletics, Survival, Pistol, Shotgun, SubMachine_Gun, Rifle,
                 Heavy_Weapon, Static_Weapon, Melee, Archery, Magic):
        # Piloting Skills
        self.Land_Vehicle = Land_Vehicle
        self.Air_Vehicle = Air_Vehicle
        self.Sea_Vehicle = Sea_Vehicle
        self.Space_Vehicle = Space_Vehicle
        self.Battle_Suit = Battle_Suit
        # Science Skills
        self.Computer = Computer
        self.Medical = Medical
        self.Engineering = Engineering
        self.Chemistry = Chemistry
        self.Celestial = Celestial
        # Information Skills
        self.Local = Local
        self.Business = Business
        self.Nature = Nature
        self.Combat = Combat
        # Social Skills
        self.Convince = Convince
        self.Entertain = Entertain
        self.Negotiation = Negotiation
        self.Sense_Motive = Sense_Motive
        self.Intimidate = Intimidate
        # Practical Skills
        self.Sneak = Sneak
        self.Climb = Climb
        self.Athletics = Athletics
        self.Survival = Survival
        # Weapon Skills
        self.Pistol = Pistol
        self.Shotgun = Shotgun
        self.SubMachine_Gun = SubMachine_Gun
        self.Rifle = Rifle
        self.Heavy_Weapon = Heavy_Weapon
        self.Static_Weapon = Static_Weapon
        self.Melee = Melee
        self.Archery = Archery
        self.Magic = Magic


class Description:
    def __init__(self, value):
        self.value = value


class History:
    def __init__(self, Place_Of_Origin, Date_Of_Birth, Date_Of_Manufacture, ):
        self.Place_Of_Origin = Place_Of_Origin
        self.Date_Of_Birth = Date_Of_Birth
        self.Date_Of_Manufacture = Date_Of_Manufacture

# Personality Components (WIP)
# These Components dictate how an NPC will react in combat. These can change during combat due to several factors.


class Aggressive:
    def __init__(self, value):
        self.value = value


class Commander:
    def __init__(self, value):
        self.value = value


class Defender:
    def __init__(self, value):
        self.value = value


class Smart:
    def __init__(self, value):
        self.value = value


class Scared:
    def __init__(self, value):
        self.value = value


class Terrified:
    def __init__(self, value):
        self.value = value

# Body Components (WIP) Players will be able to target different body parts and deal damage independently of the main
# body. Different effects will take place depending on what the player wishes to do.


class Head:
    def __init__(self, HP):
        self.HP = HP


class Torso:
    def __init__(self, HP):
        self.HP = HP
        self.Inventory = {}


class Left_Arm:
    def __init__(self, HP):
        self.HP = HP


class Left_Hand:
    def __init__(self, HP, Can_Carry):
        self.HP = HP
        self.Can_Carry = Can_Carry
        self.Inventory = {}


class Right_Arm:
    def __init__(self, HP):
        self.HP = HP


class Right_Hand:
    def __init__(self, HP, Can_Carry):
        self.HP = HP
        self.Can_Carry = Can_Carry
        self.Inventory = {}


class Left_Leg:
    def __init__(self, HP):
        self.HP = HP


class Right_Leg:
    def __init__(self, HP):
        self.HP = HP

# Item Components


class Inventory:
    def __init__(self):
        self.Inventory = {}


class Armour:
    def __init__(self, Ballistic, Impact, Pierce, Energy, Mobility_Rating, Storage_Rating, Success_Rating,
                 Stealth_Penalty, Movement_Penalty, Threshold, Type, SubType):
        self.Ballistic = Ballistic
        self.Impact = Impact
        self.Pierce = Pierce
        self.Energy = Energy
        self.Mobility_Rating = Mobility_Rating
        self.Storage_Rating = Storage_Rating
        self.Success_Rating = Success_Rating
        self.Stealth_Penalty = Stealth_Penalty
        self.Movement_Penalty = Movement_Penalty
        self.Threshold = Threshold
        self.Type = Type
        self.SubType = SubType
        self.Inventory = {}


class Defence_Ballistic:
    def __init__(self, value):
        self.value = value


class Defence_Impact:
    def __init__(self, value):
        self.value = value


class Defence_Pierce:
    def __init__(self, value):
        self.value = value


class Defence_Energy:
    def __init__(self, value):
        self.value = value


class Equipable:
    def __init__(self, value):
        self.value = value


class Wearable:
    def __init__(self, value):
        self.value = value


class Price:
    def __init__(self, value):
        self.value = value


class Weight:
    def __init__(self, value):
        self.value = value


class Damage_Type:
    def __init__(self, Ballistic, Impact, Pierce, Energy):
        self.value = Ballistic
        self.value = Impact
        self.value = Pierce
        self.value = Energy


class Burst_Fire_Inaccuracy:
    def __init__(self, value):
        self.value = value


class Action_Point_Usage:
    def __init__(self, value):
        self.value = value


class Damage:
    def __init__(self, Amount_of_Dice, Dice_Size):
        self.Amount_of_Dice = Amount_of_Dice
        self.Dice_Size = Dice_Size

class Damage_Flag:
    def __init__(self, Amount):
        self.Amount = Amount

class Attacking:
    def __init__(self, Target_X, Target_Y):
        self.Target_X = Target_X
        self.Target_Y = Target_Y

class Ammo_Capacity:
    def __init__(self, value):
        self.value = value


class Range:
    def __init__(self, value):
        self.value = value


class Space:
    def __init__(self, value):
        self.value = value


class Number_Of_Accessories:
    def __init__(self, value):
        self.value = value


class Armour_Piercing:
    def __init__(self, value):
        self.value = value


class Scenery:
    def __init__(self):
        return
