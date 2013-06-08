#! /usr/bin/env python
# kickoff script
import engine
import screens

import pygame

kernel = engine.Kernel()

screen_surf = kernel.initialize_display((800, 600))

kernel.screen_manager.register_screen(screens.GameMain(kernel))

kernel.screen_manager.switch_to('GameMain')

font = pygame.font.SysFont("Helvetica", 12)

while 1:
    delta = kernel.ticker.get_time()
    
    kernel.process_events()

    kernel.screen_manager.update(delta)

    # Render the FPS display
    fps_surf = font.render("FPS: " + str(int(kernel.ticker.get_fps())), True, (255, 255, 255))
    fps_rect = fps_surf.get_rect()
    fps_rect.topright = screen_surf.get_rect().topright
    screen_surf.blit(fps_surf, fps_rect)

    kernel.flip_display()

    kernel.ticker.tick(60)