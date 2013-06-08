import logging
import time
import sys
import os
import pygame
import pygame.locals

###################################################

class Config:
    asset_path = os.path.join("assets")

###################################################

class Colors:
    TRANSPARENT = (255, 0, 255)
    BLACK = (0, 0, 0)
    LIGHT_GREY = (200, 200, 200)
    GREY = (128, 128, 128)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)

###################################################

class Kernel:
    """
    Simple management interface for all of the 
    subsystems of the engine.  Just passes through
    some basic logic so we can manage them easily
    """
    def __init__(self, **kwargs):
        logfilename = kwargs.get('logfilename', 'game.log')
        loglevel = kwargs.get('loglevel', logging.DEBUG)

        logging.basicConfig(filename=logfilename, level=loglevel)

        logging.info("********************************************")

        logging.info("(Kernel) Initializing kernel")

        logging.info("(Kernel) Initializing pygame")
        pygame.init()

        logging.info("(Kernel) PyGame Version: " + pygame.version.ver)

        self.ticker = pygame.time.Clock()

        self.display_surface = None

        self.image_manager = ImageManager(self)
        self.sound_manager = SoundManager(self)

        self.screen_manager = ScreenManager()

    def initialize_display(self, dimensions, fullscreen=False):
        flags = pygame.DOUBLEBUF

        if fullscreen:
            flags = flags | pygame.FULLSCREEN

        logging.info("(Kernel) Initializing Display")

        self.display_surface = pygame.display.set_mode(dimensions, flags)

        assert self.display_surface, "Display failed to initialize."

        return self.display_surface


    def flip_display(self):
        pygame.display.flip()

        self.display_surface.fill(Colors.BLUE)

    def process_system_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

###################################################

class ImageManager:
    """
    Simple utility for loading and cacheing images
    """
    def __init__(self, kernel):
        self.loaded_images = {}
        self.kernel = kernel

    def load(self, filename, transparent = True):
        if (filename in self.loaded_images):
            return self.loaded_image[filename], self.loaded_images[filename].get_rect()
        else:
            image = pygame.image.load(os.path.join(Config.asset_path, "images", filename))
            image = image.convert(self.mKernel.DisplaySurface())

            if (transparent):
                image.set_colorkey(Colors.TRANSPARENT);
                image.set_alpha(255, pygame.locals.RLEACCEL)
            
            self.loaded_images[filename] = image
            return image, image.get_rect()

###################################################

class SoundManager:
    """
    Simple utility class for loading and cacheing sounds
    """
    def __init__(self, kernel):
        self.loaded_sounds = {}
        self.kernel = kernel

    def load(self, filename):
        if (filename in self.loaded_sounds):
            return self.loaded_sounds[filename]
        else:
            sound = pygame.mixer.Sound(os.path.join(Config.asset_path, "sounds", filename))
            self.loaded_sounds[filename] = sound
            return sound

###################################################

class Screen:
    """
    A Screen represents a single screen of the game.
    The functionality of the class essentially acts
    as an interface to the common actions that you
    need throughout a screen of the game.  You are
    expected to subclass this to make individual 
    sceens for your game.
    """
    def __init__(self, kernel, name):
        """
        Standard constructor.  Like most things in robo-py,
        it takes kernal and then keyword args containing the
        following:
            name: The name of this screen
        """
        self.name = name
        self.kernel = kernel
        self.initialized = False
        self.active = False

    def initialize(self):
        """
        Initializes this screen and sets up any data that is
        needed for this screen to run.  Note, this automatically
        starts the game state running.
        """

        logging.info("(Screen '" + self.name + "') Initializing")

        self.initialized = True
        self.active = True

        return True

    def destroy(self):
        """
        Destroys this screen and uninitializes all of this data.
        Should free any resources that this is holding
        """

        logging.info("(Screen '" + self.name + "') destroying")

        self.active = False
        self.initialized = False

        return True

    def pause(self):
        """
        Pause this state, but do not destroy all of its data.
        """

        logging.info("(Screen '" + self.name + "') pausing")

        self.active = False

        return True

    def resume(self):
        """
        Resume this state without re-initializing all of the data.
        """
        
        logging.info("(Screen " + self.name + "'') resuming")

        self.active = True

        return True

    def pump_event(self, event):
        """
        Handles a single event pumped from the system event pump
        """
        return True

    def update(self, delta):
        """
        Tick this screen.
        """
        return True

###################################################

class ScreenManager:
    def __init__(self):
        self.screens = {}
        self.active_screen_name = ""
        self.active_screen = None

    def register_screen(self, screen):
        if screen.name in self.screens:
            logging.warning("(Screen Manager) Screen " + screen.name + " is already registered.")
            return

        self.screens[screen.name] = screen

        logging.info("(Screen Manager) Screen '" + screen.name + "' registered.")

    def deregister_screen(self, name):
        if name not in self.screens:
            logging.warning("(Screen Manager) Screen " + name + " is not registered.")
            return

        if self.screens[name].initialized:
            self.screens[name].destroy()

        if self.active_screen_name == name:
            self.active_screen = None
            self.active_screen_name = ""

        del self.screens[name]

        logging.info("(Screen Manager) Screen '" + name + "' deregistered.")

    def switch_to(self, name):
        if name not in self.screens:
            logging.warning("(Screen Manager) Screen " + name + " is not registered.")

        logging.info("(Screen Manager) Switching to '" + name + "' screen.")

        if self.active_screen:
            if self.active_screen_name == name:
                return

            if self.active_screen.initialized:
                self.active_screen.pause()

        self.active_screen_name = name
        self.active_screen = self.screens[name]

        if self.active_screen.initialized:
            self.active_screen.unpause()
        else:
            self.active_screen.initialize()

    def get_screen(self, name):
        if name not in self.screens:
            logging.warning("(Screen Manager) Screen " + name + " is not registered.")

        return self.screens[name]

    def update(self, delta):
        if self.active_screen:
            self.active_screen.update(delta)

###################################################

