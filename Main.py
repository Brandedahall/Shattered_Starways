import tcod
import tcod.event
import esper
import Processors


def run():
    ###########################
    # Basic system information
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 40
    LIMIT_FPS = 60

    font_path = 'arial10x10.png'
    font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    tcod.console_set_custom_font(font_path, font_flags)

    window_title = 'Shattered Starways'
    Fullscreen = False
    tcod.sys_set_fps(LIMIT_FPS)
    ###########################
    # Esper Information
    world = esper.World()

    Render_Processor = Processors.Render_Processor()
    AI_processor = Processors.AI_processor()
    Keyboard_Processor = Processors.Movement_Processor()
    Death_Processor = Processors.Death_Processor()
    Combat_Processor = Processors.Combat_Processor()

    world.add_processor(Render_Processor)
    world.add_processor(AI_processor)
    world.add_processor(Keyboard_Processor)
    world.add_processor(Death_Processor)
    world.add_processor(Combat_Processor)

    Processors.Create_Characters(world)

    ###########################

    with tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, Fullscreen):
        while not tcod.console_is_window_closed():
            world.process()
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()


if __name__ == "__main__":
    run()
