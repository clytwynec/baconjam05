#! /usr/bin/env python
# kickoff script
import engine

kernel = engine.Kernel()

kernel.initialize_display((800, 600))

while 1:
    kernel.process_system_event()

    kernel.flip_display()