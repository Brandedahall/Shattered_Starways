import tcod
import Processors
import esper

###########################
# Basic system information
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 60

tileset = tcod.tileset.load_tilesheet(
        "TiledFont.png", 32, 10, tcod.tileset.CHARMAP_CP437
    )

###########################
# Esper Information
world = esper.World()

Render_Processor = Processors.Render_Processor()
FOV_Processor = Processors.FOV_Processor()
AI_processor = Processors.AI_processor()
Keyboard_Processor = Processors.Movement_Processor()
Combat_Processor = Processors.Combat_Processor()

world.add_processor(FOV_Processor, 2)
world.add_processor(Render_Processor, 1)
world.add_processor(AI_processor, 3)
world.add_processor(Keyboard_Processor)
world.add_processor(Combat_Processor)

Processors.make_map(world)

###########################

with tcod.context.new_terminal(SCREEN_WIDTH, SCREEN_HEIGHT, title="Shattered Starways", vsync=True,) as context:
    root_console = tcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
    Render_Processor.set_console(root_console)
    while True:
        world.process()
        context.present(root_console)
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
