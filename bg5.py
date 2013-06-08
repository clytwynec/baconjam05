#! /usr/bin/env python
# kickoff script
import engine
import screens

kernel = engine.Kernel()

kernel.initialize_display((800, 600))

kernel.screen_manager.register_screen(engine.Screen(kernel, 'Testing'))
kernel.screen_manager.register_screen(screens.TestScreen(kernel))

kernel.screen_manager.switch_to('Test Screen')

while 1:
    kernel.process_system_event()

    kernel.flip_display()