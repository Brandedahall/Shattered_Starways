import random
import tcod
import tcod.console
import Components
import esper
import math
import numpy as np
from Classes import Tile, Rect

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 60
MAP_WIDTH = 100
MAP_HEIGHT = 60

ROOM_MAX_SIZE = 20
ROOM_MIN_SIZE = 5
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

FOV_ALGO = 0  # default FOV algorithm
FOV_LIGHT_WALLS = True  # light walls or not

fov_recompute = True

con = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)  # Console

tcod.sys_set_fps(144)

#############################################
Player_Information = tcod.console_new(20, 60)
#############################################


class Movement_Processor(esper.Processor):  # Works with Keyboard input
    def process(self):
        self.Player_Input()
        self.Distance()

    def Distance(self):
        TargetX, TargetY = 0, 0
        for Player, (Player, Position) in self.world.get_components(Components.Player, Components.Position):
            TargetX, TargetY = Position.X, Position.Y

        for Entity, (Entity, Position, Move, Render) in self.world.get_components(Components.Entity, Components.Position,
                                                                                  Components.Can_Move, Components.Render):
            if Render.Exists and distance_to(Position.X, Position.Y, TargetX, TargetY) <= 5 and tcod.map_is_in_fov(
                    fov_map, Position.X, Position.Y):
                Position.X, Position.Y = self.Entity_Move(Position.X, Position.Y, TargetX, TargetY)

    def Entity_Move(self, Self_X, Self_Y, Target_x, Target_y):
        # Checks for a number of entities which hold specific tags, (Hostile, Alien, etc) are on the current map.
        # Uses A* pathing
        fov = tcod.map_new(MAP_WIDTH, MAP_HEIGHT)
        for y1 in range(MAP_HEIGHT):
            for x1 in range(MAP_WIDTH):
                tcod.map_set_properties(fov, x1, y1, not map[x1][y1].block_sight, not map[x1][y1].blocked)

        for Entity, (Position, Blocks) in self.world.get_components(Components.Position, Components.Move_Through):
            if Blocks and not self.world.has_component(Entity, Components.Player):
                tcod.map_set_properties(fov, Position.X, Position.Y, True, False)

        My_Path = tcod.path_new_using_map(fov, 1.41)

        tcod.path_compute(My_Path, Self_X, Self_Y, Target_x, Target_y)

        if not tcod.path_is_empty(My_Path) and tcod.path_size(My_Path) < 25:
            x, y = tcod.path_walk(My_Path, True)
            if x or y:
                tcod.path_delete(My_Path)
                return x, y
        else:
            tcod.path_delete(My_Path)
            return Self_X, Self_Y

    def Player_Input(self):
        global fov_recompute
        for ent, (Player, Position, Move, Inventory) in self.world.get_components(Components.Player,
                                                                                  Components.Position,
                                                                                  Components.Can_Move,
                                                                                  Components.Inventory):  # Only affects the player.
            key = tcod.console_wait_for_keypress(True)
            key_char = chr(key.c)
            # Four cardinal directions
            if key.vk == tcod.KEY_KP8:
                Destination = Position.X, Position.Y - 1
                Position.X, Position.Y = self.Collision(Position, Destination)  # UP
            elif key.vk == tcod.KEY_KP2:
                Destination = Position.X, Position.Y + 1
                Position.X, Position.Y = self.Collision(Position, Destination)  # Down
            elif key.vk == tcod.KEY_KP4:
                Destination = Position.X - 1, Position.Y
                Position.X, Position.Y = self.Collision(Position, Destination)  # Left
            elif key.vk == tcod.KEY_KP6:
                Destination = Position.X + 1, Position.Y
                Position.X, Position.Y = self.Collision(Position, Destination)  # Right
            # Four Diagonal directions
            elif key.vk == tcod.KEY_KP7:
                Destination = Position.X - 1, Position.Y - 1
                Position.X, Position.Y = self.Collision(Position, Destination)
            elif key.vk == tcod.KEY_KP9:
                Destination = Position.X + 1, Position.Y - 1
                Position.X, Position.Y = self.Collision(Position, Destination)
            elif key.vk == tcod.KEY_KP1:
                Destination = Position.X - 1, Position.Y + 1
                Position.X, Position.Y = self.Collision(Position, Destination)
            elif key.vk == tcod.KEY_KP3:
                Destination = Position.X + 1, Position.Y + 1
                Position.X, Position.Y = self.Collision(Position, Destination)

            elif key_char == "a":
                self.Target_Control(Position.X, Position.Y, ent)
            elif key_char == 'k':
                self.Pickup(Position.X, Position.Y, Inventory.Inventory)
            elif key_char == "l":
                self.Loot_Drop()
            elif key_char == 't':
                self.Show_Inventory(Inventory)
        fov_recompute = True

    def Pickup(self, Player_Position_X, Player_Position_Y, Player_Inventory):
        for Ent, (Position, Entity, Render) in self.world.get_components(Components.Position, Components.Entity,
                                                                         Components.Render):
            if Render.value and Render.Exists:
                if Position.X == Player_Position_X and Position.Y == Player_Position_Y:
                    Player_Inventory.append(Ent)
                    Render.Exists = False

    def Show_Inventory(self, Inventory):
        i = 0
        for x in Inventory.Inventory:
            if self.world.try_component(x, Components.Name):
                Name = self.world.component_for_entity(x, Components.Name)
                tcod.console_print(con, 10, 10 + i, Name.value)
                i += 1

    def Collision(self, Source_Position, Destination):
        if map[Destination[0]][Destination[1]].blocked:
            return Source_Position.X, Source_Position.Y
        else:
            return Destination[0], Destination[1]

    def Target_Control(self, PositionX, PositionY, Ent):
        # Creates an entity cursor where the character is. The player can move it around the area, but can only target
        # up to their weapon's range.
        return

    def Loot_Drop(self):
        self.world.create_entity(Components.Item(), Components.Render(True, 'O', tcod.black, False),
                                 Components.Position(random.randint(10, 30), random.randint(10, 20)))
        return


class AI_processor(esper.Processor):  # Deals with the AI choosing stuff to do in the game.
    def process(self):
        return


def distance_to(selfX, selfY, targetX, targetY):
    dx = targetX - selfX
    dy = targetY - selfY
    return math.sqrt(dx ** 2 + dy ** 2)


class Render_Processor(esper.Processor):
    def set_console(self, console):
        self.console = console

    def process(self):
        # for Non_Player, (Render, Position) in self.world.get_components(Components.Render, Components.Position):
        #    if Render.value:
        #        if Render.Exists:
        #            con.print(Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)
        for Player, (Player, Render, Position) in self.world.get_components(Components.Player, Components.Render,
                                                                            Components.Position):
            con.print(Position.X, Position.Y, '@', tcod.white, Render.Background)
        con.blit(self.console, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


class Combat_Processor(esper.Processor):
    def process(self):
        for ent, (Attacking) in self.world.get_components(
                Components.Attacking):  # Iterates through and finds an entity which is actually attacking.
            # Iterates through every other entity and checks whether they own a position and a renderable component.
            for target, (Position, Render) in self.world.get_components(Components.Position, Components.Render):
                # If the position of the entity is the same as the target position, it'll figure out if it can be hit.
                if Position.X == Attacking.Target_X and Position.Y == Attacking.Target_Y:
                    return
            return

        for ent, (Alive, Health) in self.world.get_components(Components.Alive, Components.Health):
            if Health.value <= 0:
                Alive.value = False
                self.world.add_component(ent, Components.Move_Through(True))
                return
        return


class FOV_Processor(esper.Processor):
    def set_console(self, console):
        self.console = console

    def process(self):
        global fov_map, fov_recompute
        if fov_recompute:
            fov_recompute = False
            for Player, (Player, Position) in self.world.get_components(Components.Player, Components.Position):
                tcod.map_compute_fov(fov_map, Position.X, Position.Y, 15, FOV_LIGHT_WALLS, FOV_ALGO)
            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    visible = tcod.map_is_in_fov(fov_map, x, y)
                    wall = map[x][y].block_sight
                    if not visible:
                        if map[x][y].explored:  # It's out of the player's FOV
                            if wall:
                                con.print(x, y, '#', tcod.grey, tcod.black)
                            else:
                                con.print(x, y, ' ', tcod.grey, tcod.black)
                    else:  # It's visible
                        if wall:
                            con.print(x, y, '#', tcod.white, tcod.black)
                        else:
                            con.print(x, y, ' ', tcod.white, tcod.black)
                        map[x][y].explored = True
            for Entity, (Render, Position) in self.world.get_components(Components.Render, Components.Position):
                visible = tcod.map_is_in_fov(fov_map, Position.X, Position.Y)
                if not visible:
                    if not Render.In_FoV:
                        Render.value = False
                else:
                    if Render.Exists:
                        Render.value = True


def Create_Character(world, Player_X, Player_Y):
    # Create a Player Character
    Player = world.create_entity(Components.Player(),
                                 Components.Position(Player_X, Player_Y),
                                 Components.Render(True, '@', tcod.black, False),  # Add default parts to the PC
                                 Components.Can_Move(True), Components.Health(10, 10), Components.Alive(True),
                                 Components.Action_Points(5), Components.Speed(5),
                                 Components.Can_See(True), Components.Can_Talk(True), Components.Head(10),
                                 Components.Left_Arm(10), Components.Left_Hand(5, True), Components.Right_Arm(10),
                                 Components.Right_Hand(5, True), Components.Left_Leg(10), Components.Right_Leg(10),
                                 Components.Move_Through(False), Components.Skills(), Components.Inventory())


def Create_Items(world, Item_X, Item_Y):

    return


def Create_Entities(world, Room):
    num_monsters = tcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)
    for i in range(num_monsters):
        # choose random spot for this monster
        x = tcod.random_get_int(0, Room.x1 - 1, Room.x2 - 1)
        y = tcod.random_get_int(0, Room.y1 - 1, Room.y2 - 1)

        if tcod.random_get_int(0, 0, 100) < 80:  # 80% chance of getting an orc
            # create an orc
            world.create_entity(Components.Entity(), Components.Position(x, y),
                                Components.Render(True, 'O', tcod.black, False),
                                Components.Can_Move(True), Components.Health(tcod.random_get_int(0, 3, 5), 5),
                                Components.Alive(True), Components.Name('Orc'), Components.Move_Through(False))
        else:
            # create a troll
            world.create_entity(Components.Entity(), Components.Position(x, y),
                                Components.Render(True, 'T', tcod.black, False),
                                Components.Can_Move(True), Components.Health(tcod.random_get_int(0, 3, 5), 5),
                                Components.Alive(True), Components.Name('Troll'), Components.Move_Through(False))
    return


def Random_Name_Gen():
    Total_Name = ''
    Prefix_List = {' ', ' ', ' '}
    Suffix_List = {' ', ' ', ' '}

    return Total_Name


def make_map(world):
    global map, fov_map, Astar_Map

    # fill map with "blocked" tiles

    map = [
        [Tile(True) for y in range(MAP_HEIGHT)]
        for x in range(MAP_WIDTH)
    ]

    rooms = []
    num_rooms = 0

    for r in range(MAX_ROOMS):
        # random width and height
        w = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = tcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = tcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # this means there are no intersections, so this room is valid
            # "paint" it to the map's tiles
            Create_Rooms(new_room)
            # Create_Entities(world, new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # this is the first room, where the player starts at
                Create_Character(world, new_x, new_y)
            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                # draw a coin (random number that is either 0 or 1)
                if tcod.random_get_int(0, 0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

    fov_map = tcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    Astar_Map = np.ones((MAP_WIDTH, MAP_HEIGHT), dtype=np.int8, order="F")
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
            if not map[x][y].blocked:
                Astar_Map[x][y] = 1


def Create_Rooms(room):
    global map
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False


def create_h_tunnel(x1, x2, y):
    global map
    # horizontal tunnel. min() and max() are used in case x1>x2
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False


def create_v_tunnel(y1, y2, x):
    global map
    # vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

