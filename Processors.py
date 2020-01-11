import esper
import tcod
import Components
import random

Inventory_Panel = tcod.console_new(30, 40)
Health_Panel = tcod.console_new(50, 10)
Update_Panels = True

color_dark_wall = tcod.Color(0, 0, 100)
color_light_wall = tcod.Color(130, 110, 50)
color_dark_ground = tcod.Color(50, 50, 150)
color_light_ground = tcod.Color(200, 180, 50)

Radius = 5
fov_map = tcod.map_new(80, 40)


class Movement_Processor(esper.Processor):  # Works with Keyboard input
    def process(self):
        self.Player_Input()
        for ent, (Position, Move, Destination) in self.world.get_components(Components.Position, Components.Can_Move,
                                                                            Components.Destination):
            self.Entity_Move(Position)
            return
        return

    def Entity_Move(self, Position):
        # Checks for a number of entities which hold specific tags, (Hostile, Alien, etc) are on the current map.
        # Checks which co-ord is the closest (while passing a series of checks).
        # Uses A* pathing
        return

    def Player_Input(self):
        for ent, (Player, Position, Move) in self.world.get_components(Components.Player, Components.Position,
                                                                       Components.Can_Move):  # Only affects the player.
            key = tcod.console_wait_for_keypress(True)
            key_char = chr(key.c)
            tcod.console_put_char(0, Position.X, Position.Y, ' ', tcod.BKGND_NONE)
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
                self.Target_Control(Position)
            elif key.vk == tcod.KEY_ESCAPE:
                return 1
            elif key.vk == tcod.KEY_SPACE:
                return

    def Collision(self, Source_Position, Destination):
        for Square, Position in self.world.get_component(Components.Position):
            if Position.X == Destination[0] and Position.Y == Destination[1]:
                if self.world.has_component(Square, Components.Move_Through):
                    return Destination[0], Destination[1]
                else:
                    return Source_Position.X, Source_Position.Y

    def Target_Control(self, Position):
        # Creates an entity cursor where the character is. The player can move it around the area, but can only target
        # up to their weapon's range.
        return


class AI_processor(esper.Processor):  # Deals with the AI choosing stuff to do in the game.
    def process(self):
        for ent1, (Position, Move) in self.world.get_components(Components.Position, Components.Can_Move):
            return


class Render_Processor(esper.Processor):
    def process(self):
        for ren, (Scenery, Render, Position) in self.world.get_components(Components.Scenery, Components.Render,
                                                                          Components.Position):
            if Render.value and Render.Explored:
                tcod.console_put_char_ex(0, Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)

        for ren, (Item, Render, Position) in self.world.get_components(Components.Item, Components.Render,
                                                                       Components.Position):
            if Render.value  and Render.Explored:
                tcod.console_put_char_ex(0, Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)

        for ren, (Entity, Render, Position) in self.world.get_components(Components.Entity, Components.Render,
                                                                         Components.Position):
            if Render.value and Render.Explored:
                tcod.console_put_char_ex(0, Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)

        for ren, (Player, Render, Position) in self.world.get_components(Components.Player, Components.Render,
                                                                         Components.Position):
                tcod.console_put_char_ex(0, Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)

        tcod.console_flush()  # Show the Console.

    def Camera(self):
        # Scrollable Camera
        return


class Combat_Processor(esper.Processor):
    def process(self):
        for ent, (Attacking) in self.world.get_components(Components.Attacking):  # Iterates through and finds an entity which is actually attacking.
            # Iterates through every other entity and checks whether they own a position and a renderable component.
            for target, (Position, Render) in self.world.get_components(Components.Position, Components.Render):
                # If the position of the entity is the same as the target position, it'll figure out if it can be hit.
                if Position.X == Attacking.Target_X and Position.Y == Attacking.Target_Y:
                    return
            return

        for ent, (Alive, Health) in self.world.get_components(Components.Alive, Components.Health):
            if Health.value <= 0:
                self.world.remove_component(ent, Components.Can_Talk)
                self.world.remove_component(ent, Components.Can_Move)
                Alive.value = False
                self.world.remove_component(ent, Components.Render)
                return
        return


class FOV_Processor(esper.Processor):
    def process(self):
        for Player, (Player, Can_See, Position) in self.world.get_components(Components.Player, Components.Can_See,
                                                                             Components.Position):
            tcod.map_compute_fov(fov_map, Position.X, Position.Y, Can_See.Radius, True, 0)
            for Entity, (Pos, Render) in self.world.get_components(Components.Position, Components.Render):
                visible = tcod.map_is_in_fov(fov_map, Pos.X, Pos.Y)
                if not visible:
                    if Render.Explored:
                        if Render.Block_Sight:
                            Render.Background = color_dark_wall
                        else:
                            Render.Background = color_dark_ground
                else:
                    if Render.Block_Sight:
                        Render.Background = color_light_wall
                    else:
                        Render.Background = color_light_ground
                    Render.Explored = True


def Create_Characters(world):
    # Create a Player Character
    Player = world.create_entity(Components.Player(), Components.Position(random.randint(10, 30), random.randint(10, 20)),
                                 Components.Render(True, '@', tcod.black, False),     # Add default parts to the PC
                                 Components.Can_Move(True), Components.Health(10), Components.Alive(True),
                                 Components.Action_Points(5), Components.Speed(5),
                                 Components.Can_See(True), Components.Can_Talk(True), Components.Head(10),
                                 Components.Left_Arm(10), Components.Left_Hand(5, True), Components.Right_Arm(10),
                                 Components.Right_Hand(5, True), Components.Left_Leg(10), Components.Right_Leg(10),
                                 Components.Move_Through(True), Components.Skills())

    world.add_component(Player, Components.Inventory)

    # Creates a standard test character

    Test = world.create_entity(Components.Entity(), Components.Position(20, 20),
                               Components.Render(True, 'T', tcod.black, False), Components.Health(5),
                               Components.Alive(True), Components.Inventory(), Components.Destination())

    for x in range(0, 80):
        for y in range(0, 40):
            world.create_entity(Components.Position(x, y), Components.Render(True, '~', tcod.black, True),
                                Components.Scenery(), Components.Move_Through(True))

    for ent, (Position, Render, Move_Through) in world.get_components(Components.Position, Components.Render,
                                                                      Components.Move_Through):
        tcod.map_set_properties(fov_map, Position.X, Position.Y, Render.value, Move_Through.value)


def Transfer_Inventory(Source, Destination, Item):
    return


def Print_Panels(Update_Panel):
    if Update_Panel:
        tcod.console_blit(Inventory_Panel, 0, 0, 0, 0, 0, 50, 0, 0.5, 0.5)
        tcod.console_blit(Health_Panel, 0, 0, 0, 0, 0, 0, 30, 0.5, 0.5)
        tcod.console_print_frame(Inventory_Panel, 0, 0, 30, 40)
        tcod.console_print_frame(Health_Panel, 0, 0, 50, 10)
        Update_Panel = False
    else:
        return
