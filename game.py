import pygame

class Garmet:
    def __init__(self, kernel, screen):
        self.kernel = kernel
        self.screen = screen

        # Initialize our various properties
        # Image Stuff
        self.image, self.rect = kernel.image_manager.load("monster.bmp", True)

        # Random Color
        self.color = pygame.Color(0, 0, 0)

        # Properties Go Here
        self.position = (0, 0)

        self.falling = True
        self.gravity = 1

        pass

    def shake(self):
        # Drop some coins if we so care to here
        pass

    def update(self, delta):
        # Update our position if we're falling
        pass

    def draw(self, surface):
        if self.image and self.rect:
            # Position the rectangle for correct drawing
            self.rect.center = self.position
            surface.blit(self.image, self.rect)

        pass

class GarmetRandomizer:
    def __init__(self, kernel, screen):
        self.kernel = kernel
        self.screen = screen

    def next(self):
        return Garmet(self.kernel, self.screen)

class Bins:
    def __init__(self, kernel, screen):
        self.bins = [
            'Lights',
            'Darks',
            'Biohazard'
        ]

        self.bin_images = [
            # surface
            # surface
            # surface
        ]

        self.bin_rects = [
            # pygame.Rect
            # pygame.Rect
            # pygame.Rect
        ]

        # How long we've stayed in position
        self.ticks = 0
        self.randomize_time = 1500

    def spin(self):
        # Randomize the order of the bins
        random.shuffle(self.bins)

    def collide_bins(self, garmet):
        # returns which bin the garmet is in
        pass

    def update(self, delta):
        pass

    def draw(self, surface):
        pass

    pass

class Shelves:
    pass
