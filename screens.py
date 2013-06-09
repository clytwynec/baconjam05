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
        self.current_garment = None

        # For the waterfall
        self.next_garment = 0

        # A list of the garments in the game area
        self.garment_randomizer = game.GarmentRandomizer(kernel, self)
        self.garments = []

        # Drawing Stuff
        self.surface = pygame.Surface((800, 600)).convert()
        self.rect = pygame.Rect(0, 0, 800, 600)

        # Background Image
        self.background_image = None
        self.background_rect = None

        # bin stuff
        self.bins = None
        self.bin_score = {'lights': 0, 'darks': 0, 'biohazard': 0}

        self.lives = 10
        self.coin_total = 0

        self.coins = []

        self.sock_bin_streak = 0
        self.sock_bin_points = 0

        self.font = pygame.font.SysFont("Helvetica", 16, True)

        self.sock_bin_right_image, self.sock_bin_right_rect = kernel.image_manager.load('basket_left.bmp', True)
        self.sock_bin_right_rect.bottomleft = (690, 188)

        self.sock_bin_left_image, self.sock_bin_left_rect = kernel.image_manager.load('basket_right.bmp', True)
        self.sock_bin_left_rect.bottomleft = (12, 188)

        print self.sock_bin_left_rect

    def initialize(self):
        engine.Screen.initialize(self)

        self.background_image, self.background_rect = self.kernel.image_manager.load("background_tmp.bmp")

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
            # trigger the shake event for the current garment and
            # reset the counter
            if self.shakes >= 2:
                self.shakes = 0

                if self.current_garment:
                    self.current_garment.shake()

            # Also make sure we drag the current garment around if its set
            if self.current_garment:
                self.current_garment.position = [event.pos[0], event.pos[1]]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for garment in self.garments:
                if garment.rect.collidepoint(event.pos):
                    self.current_garment = garment
                    self.current_garment.pick_up()
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.current_garment:
                self.current_garment.put_down()
                self.current_garment = None


    def update(self, delta):
        self.ticks += delta

        if (self.ticks >= 200): 
            self.ticks = 0
            self.shakes = max(self.shakes - 1, 0)

        # Extra Lives
        if (self.coin_total >= 100 and self.lives < 10):
            if (self.coin_total/100 <= 10 - self.lives):
                num_lives_added = self.coin_total/100
            elif( 10 - self.lives <= self.coin_total/100):
                num_lives_added =  10 - self.lives

            self.lives += num_lives_added
            self.coin_total -= 100 * num_lives_added

        self.next_garment -= self.ticks

        if (self.next_garment <= 0):
            self.garments.append(self.garment_randomizer.next())
            self.next_garment = 10000

        self.bins.update(delta)

        for garment in self.garments:
            garment.update(delta)

            # Check garment collisions
            bin = self.bins.garment_check(garment)

            if bin:
                self.on_bin_collision(garment, bin)

            if (self.sock_bin_left_rect.colliderect(garment.rect) or self.sock_bin_right_rect.colliderect(garment.rect)):
                self.on_sock_bin_collision(garment)

        for coin in self.coins:
            coin.update(delta)

        self.bins.draw(self.surface)
        self.surface.blit(self.sock_bin_left_image, self.sock_bin_left_rect)
        self.surface.blit(self.sock_bin_right_image, self.sock_bin_right_rect)

        for garment in self.garments:
            garment.draw(self.surface)

        for coin in self.coins:
            coin.draw(self.surface)

        text = self.font.render("Lives: " + str(self.lives), True, engine.Colors.BLACK)
        self.surface.blit(text, (10, 10, text.get_rect().width, text.get_rect().height))


        text = self.font.render("Coins: " + str(self.coin_total), True, engine.Colors.BLACK)
        self.surface.blit(text, (790 - text.get_rect().width, 10, text.get_rect().width, text.get_rect().height))

        self.kernel.display_surface.blit(self.surface, self.rect)

        self.surface.fill(engine.Colors.BLUE)
        
        self.surface.blit(self.background_image, self.background_rect)

    def on_sock_bin_collision(self, garment):
        if garment.type == 'sock':            
            if garment.biohazard == True:
                self.sock_bin_streak = 0
            else:
                self.sock_bin_streak += 1
            self.garments.remove(garment)

    def on_bin_collision(self, garment, bin):
        if garment.type == 'sock' and garment.biohazard == False:
            self.sock_bin_streak = 0

        if garment.biohazard == True:

            # if biohazard and in correct bin
            if bin == 'biohazard':
                self.bin_score[bin] += 1

            # if biohazard in wrong bin
            else:
                self.bin_score[bin] -= self.bin_score[bin]/2
                self.lives -= 1 

        # if not biohazard and in correct bin
        elif garment.color_cat == bin:
            self.bin_score[bin] += 1

        # if not biohazard and in wrong bin
        else:
            self.bin_score[bin] -= 1
            self.lives -= 1

        if self.current_garment == garment:
            self.current_garment = None

        self.garments.remove(garment)
        print self.bin_score


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
