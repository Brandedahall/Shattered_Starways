import esper
import tcod
import Components
import random

Inventory_Panel = tcod.console_new(30, 40)
Health_Panel = tcod.console_new(50, 10)
Update_Panels = True


class Movement_Processor(esper.Processor):  # Works with Keyboard input
    def process(self):
        for ent, (Player, Position, Move) in self.world.get_components(Components.Player, Components.Position,
                                                                       Components.Can_Move):
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
                    if self.world.component_for_entity(Square, Components.Move_Through):
                        return Destination[0], Destination[1]
                    else:
                        return Source_Position.X, Source_Position.Y
                else:
                    return Source_Position.X, Source_Position.Y

    def Target_Control(self, Position):
        tcod.console_put_char_ex(0, Position.x, Position.Y, 'F', tcod.white, tcod.black)
        return


class AI_processor(esper.Processor):  # Deals with the AI choosing stuff to do in the game.
    def process(self):
        for ent, (Position, Move) in self.world.get_components(Components.Position, Components.Can_Move):
            return


class Render_Processor(esper.Processor):
    def process(self):
        for ren, (Scenery, Render, Position) in self.world.get_components(Components.Scenery, Components.Render,
                                                                          Components.Position):
            if Render.value:
                tcod.console_put_char_ex(0, Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)
            else:
                return

        for ren, (Item, Render, Position) in self.world.get_components(Components.Item, Components.Render,
                                                                       Components.Position):
            if Render.value:
                tcod.console_put_char_ex(0, Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)
            else:
                return

        for ren, (Entity, Render, Position) in self.world.get_components(Components.Entity, Components.Render,
                                                                         Components.Position):
            if Render.value:
                tcod.console_put_char_ex(0, Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)
            else:
                return

        for ren, (Player, Render, Position) in self.world.get_components(Components.Player, Components.Render,
                                                                         Components.Position):
            if Render.value:
                tcod.console_put_char_ex(0, Position.X, Position.Y, Render.Tile, tcod.white, Render.Background)
            else:
                return

        tcod.console_flush()  # Show the Console.


# 'Kills' the entity if it dies in-game.
class Death_Processor(esper.Processor):
    def process(self):
        for ent, (Alive, Health) in self.world.get_components(Components.Alive, Components.Health):
            if Health.value <= 0:
                self.world.remove_component(ent, Components.Can_Talk)
                self.world.remove_component(ent, Components.Can_Move)
                Alive.value = False
                return


class Combat_Processor(esper.Processor):
    def process(self):
        for ent, (Attacking) in self.world.get_components(Components.Attacking): # Iterates through and finds an entity which is actually attacking.
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


def Create_Characters(world):
    # Create a Player Character
    Player = world.create_entity(Components.Player(), Components.Position(random.randint(0, 1), random.randint(0, 1)),
                                 Components.Render(True, '@', tcod.black),     # Add default parts to the PC
                                 Components.Can_Move(True), Components.Health(10), Components.Alive(True),
                                 Components.Action_Points(5), Components.Speed(5),
                                 Components.Can_See(True), Components.Can_Talk(True), Components.Head(10),
                                 Components.Left_Arm(10), Components.Left_Hand(5, True), Components.Right_Arm(10),
                                 Components.Right_Hand(5, True), Components.Left_Leg(10), Components.Right_Leg(10), Components.Move_Through(True))

    world.add_component(Player, Components.Inventory)

    # Creates a standard test character

    Test = world.create_entity(Components.Entity(), Components.Position(20, 20),
                               Components.Render(True, 'T', tcod.black), Components.Health(5),
                               Components.Alive(True), Components.Inventory())

    for x in range(0, 80):
        for y in range(0, 40):
            world.create_entity(Components.Position(x, y), Components.Render(True, '~', tcod.black),
                                Components.Scenery(), Components.Move_Through(True))


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


