import os
import sys
import random
import pygame

import engine

###################################################
class TestScreen(engine.Screen):
    def __init__(self, kernel):
        engine.Screen.__init__(self, kernel, 'Test Screen')

    def initialize(self):
        engine.Screen.initialize(self)

        print "This is a test of the screen system"

###################################################

class GameMain(engine.Screen):
    def __init__(self, kernel):
        engine.Screen.__init__(self, kernel, 'GameMain')

        self.last_mouse_x = pygame.mouse.get_pos()[0]
        self.shakes = 0
        self.ticks = 0
        self.mouse_moving_right = False

        self.current_garmet = None

        self.garmets = []

    def initialize(self):
        engine.Screen.initialize(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            current_mouse_x = event.pos[0]

            # Calculate shakes.  This is done by counting how many times
            # the mouse has changed direction within a given timeframe
            if self.mouse_moving_right and self.last_mouse_x > current_mouse_x:
                self.shakes += 1
                self.mouse_moving_right = False
            elif not self.mouse_moving_right and self.last_mouse_x < current_mouse_x:
                self.shakes += 1
                self.mouse_moving_right = True

            self.last_mouse_x = current_mouse_x

            # If we've changed directions more than 5 times, then
            # trigger the shake event for the current garmet and
            # reset the counter
            if self.shakes >= 5:
                self.shakes = 0

                if self.current_garmet:
                    self.current_garmet.shake()

            # Also make sure we drag the current garmet around if its set
            if self.current_garmet:
                self.current_garmet.position = (event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for garmet in self.garmets:
                if garmet.rect.collidepoint(event.pos):
                    self.current_garmet = garmet
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.current_garmet:
                self.current_garmet = None


    def update(self, delta):
        self.ticks += delta

        if (self.ticks >= 200):
            self.ticks = 0
            self.shakes = max(self.shakes - 1, 0)


###################################################

class MenuBase(engine.Screen):
    def __init__(self, name, kernel, gsm):
        engine.Screen.__init__(self, name, kernel)

        self.heading = None
        self.heading_rect = None
        self.menu_items = {}
        self.menu_images = {}
        self.menu_hover_images = {}
        self.menu_rects = {}

    def initialize(self):
        if (len(self.menu_items.keys()) == 0):
            self.menu_items = self.menu_images

        return engine.screen.initialize(self)

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            for item in self.menu_rects:
                if (self.menu_rects[item].collidepoint(event.pos) and item in self.menu_hover_images):
                    self.menu_items[item] = self.menu_hover_images[item]
                else:
                    self.menu_items[item] = self.menu_images[item]
        elif event.type == MOUSEBUTTONDOWN:
            for item in self.menu_rects:
                if (self.menu_rects[item].collidepoint(event.pos)):
                    if (item == "Exit"):
                        pygame.quit()
                        sys.exit()
                    else:
                        self.screen_manager.switch_to(item)


    def update(self, delta):
        if (self.heading):
            self.kernel.display_surface.blit(self.heading, self.headingRect)

        for item in self.menu_items:
            self.kernel.display_surface.blit(self.menu_items[item], self.menu_rects[item])

        return engine.screen.update(self, delta)
