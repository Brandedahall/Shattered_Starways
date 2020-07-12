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
        self.Block_Sight = None
        self.Explored = False

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
    def __init__(self, Value):
        self.Value = Value


class Destination:
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Path = {}


class Can_See:
    def __init__(self, value):
        self.value = value
        self.Radius = 15
        self.Visible_To_Player = False


class Visible:
    def __init__(self, value):
        self.value = value


class Can_Move:
    def __init__(self, value):
        self.value = value


class Can_Talk:
    def __init__(self, value):
        self.value = value


class Skills:
    def __init__(self):
        # Piloting Skills
        self.Land_Vehicle = 0
        self.Air_Vehicle = 0
        self.Sea_Vehicle = 0
        self.Space_Vehicle = 0
        self.Battle_Suit = 0
        # Science Skills
        self.Computer = 0
        self.Medical = 0
        self.Engineering = 0
        self.Chemistry = 0
        self.Celestial = 0
        # Information Skills
        self.Local = 0
        self.Business = 0
        self.Nature = 0
        self.Combat = 0
        # Social Skills
        self.Convince = 0
        self.Entertain = 0
        self.Negotiation = 0
        self.Sense_Motive = 0
        self.Intimidate = 0
        # Practical Skills
        self.Sneak = 0
        self.Climb = 0
        self.Athletics = 0
        self.Survival = 0
        # Weapon Skills
        self.Pistol = 0
        self.Shotgun = 0
        self.SubMachine_Gun = 0
        self.Rifle = 0
        self.Heavy_Weapon = 0
        self.Static_Weapon = 0
        self.Melee = 0
        self.Archery = 0
        self.Magic = 0


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
