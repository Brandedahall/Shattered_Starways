import esper
import tcod
import Components
import random

Inventory_Panel = tcod.console_new(30, 40)
Health_Panel = tcod.console_new(50, 10)
Update_Panels = True


class Keyboard_Processor(esper.Processor):  # Works with Keyboard input
    def process(self):
        for ent, (Player, Position, Move) in self.world.get_components(Components.Player, Components.Position,
                                                                       Components.Can_Move):
            key = tcod.console_wait_for_keypress(True)
            tcod.console_put_char(0, Position.X, Position.Y, ' ', tcod.BKGND_NONE)
            # Four cardinal directions
            if key.vk == tcod.KEY_KP8:
                Position.Y -= 1
            elif key.vk == tcod.KEY_KP2:
                Position.Y += 1
            elif key.vk == tcod.KEY_KP4:
                Position.X -= 1
            elif key.vk == tcod.KEY_KP6:
                Position.X += 1
            # Four Diagonal directions
            elif key.vk == tcod.KEY_KP7:
                Position.Y = Position.Y - 1
                Position.X = Position.X - 1
            elif key.vk == tcod.KEY_KP9:
                Position.Y = Position.Y - 1
                Position.X = Position.X + 1
            elif key.vk == tcod.KEY_KP1:
                Position.Y = Position.Y + 1
                Position.X = Position.X - 1
            elif key.vk == tcod.KEY_KP3:
                Position.Y = Position.Y + 1
                Position.X = Position.X + 1
            elif key.vk == tcod.KEY_ESCAPE:
                raise SystemExit()
            elif key.vk == tcod.KEY_SPACE:
                return


class AI_processor(esper.Processor):  # Deals with the AI choosing stuff to do in the game.
    def process(self):
        for ent, (Position, Move) in self.world.get_components(Components.Position, Components.Can_Move):
            return


class Render_Processor(esper.Processor):
    def process(self):
        for ren, (Render, Position) in self.world.get_components(Components.Render, Components.Position):
            tcod.console_flush()  # Show the Console.
            tcod.console_put_char(0, Position.X, Position.Y, Render.Tile, tcod.BKGND_NONE)
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
        return

    def Damage(self, Weapon_Damage, Armour_Values):
        return

    def Death(self):
        for ent, (Alive, Health) in self.world.get_components(Components.Alive, Components.Health):
            if Health.value <= 0:
                self.world.remove_component(ent, Components.Can_Talk)
                self.world.remove_component(ent, Components.Can_Move)
                Alive.value = False
                return


def Create_Characters(world):
    # Create a Player Character
    Player = world.create_entity(Components.Player(True), Components.Position(random.randint(1, 49), random.randint(1, 40)),
                                 Components.Render(True, '@'),     # Add default parts to the PC
                                 Components.Can_Move(True), Components.Health(10), Components.Alive(True),
                                 Components.Action_Points(5), Components.Speed(5), Components.Move_Through(False),
                                 Components.Can_See(True), Components.Can_Talk(True), Components.Head(10),
                                 Components.Left_Arm(10), Components.Left_Hand(5, True), Components.Right_Arm(10),
                                 Components.Right_Hand(5, True), Components.Left_Leg(10), Components.Right_Leg(10))

    world.add_component(Player, Components.Inventory)


def Print_Panels(Update_Panels):
    if Update_Panels:
        tcod.console_blit(Inventory_Panel, 0, 0, 0, 0, 0, 50, 0, 0.5, 0.5)
        tcod.console_blit(Health_Panel, 0, 0, 0, 0, 0, 0, 30, 0.5, 0.5)
        tcod.console_print_frame(Inventory_Panel, 0, 0, 30, 40)
        tcod.console_print_frame(Health_Panel, 0, 0, 50, 10)
        Update_Panels = False
    else:
        return


