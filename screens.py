import os
import sys
import random
import pygame

import engine
import game

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

        # For shaking gesture
        self.last_mouse_x = pygame.mouse.get_pos()[0]
        self.shakes = 0
        self.ticks = 0
        self.mouse_moving_right = False

        # For clicking and dragging
        self.current_garmet = None

        # A list of the garmets in the game area
        self.garmet_randomizer = game.GarmetRandomizer(kernel, self)
        self.garmets = []
        self.garmets.append(self.garmet_randomizer.next())

        # Drawing Stuff
        self.surface = pygame.Surface((800, 600)).convert()
        self.rect = pygame.Rect(0, 0, 800, 600)

        self.bins = None

    def initialize(self):
        engine.Screen.initialize(self)

        self.bins = game.Bins(self.kernel, self)

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

        self.bins.update(delta)

        for garmet in self.garmets:
            garmet.update(delta)

        self.bins.draw(self.surface)

        for garmet in self.garmets:
            garmet.draw(self.surface)

        self.kernel.display_surface.blit(self.surface, self.rect)

        self.surface.fill(engine.Colors.BLUE)


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
