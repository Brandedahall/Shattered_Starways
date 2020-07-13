import tcod
import tcod.console
import tcod.event
import Classes
import Processors
import esper

###########################
# Basic system information
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 60
LIMIT_FPS = 144

###########################
# Esper Information
world = esper.World()

Render_Processor = Processors.Render_Processor()
FOV_Processor = Processors.FOV_Processor()
AI_processor = Processors.AI_processor()
Keyboard_Processor = Processors.Movement_Processor()
Combat_Processor = Processors.Combat_Processor()

world.add_processor(FOV_Processor, 1)
world.add_processor(Render_Processor, 2)
world.add_processor(AI_processor, 3)
world.add_processor(Keyboard_Processor)
world.add_processor(Combat_Processor)

Processors.make_map(world)


###########################

with tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False):
    while not tcod.console_is_window_closed():
        world.process()
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()