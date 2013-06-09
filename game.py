import pygame, math, random

class Garment:
    def __init__(self, kernel, screen, garment_type, biohazard, coins):
        self.kernel = kernel
        self.screen = screen

        # Initialize our various properties
        # Image Stuff
        self.image, self.rect = kernel.image_manager.load("monster.bmp", True)

        # Random Color
        self.color = pygame.Color(0, 0, 0)
        self.type = garment_type
        self.biohazard = biohazard
        self.coinage = coins

        # Properties Go Here
        self.position = [0, 0]

        self.falling = True
        self.gravity = 0.05
        self.velocity = 0


    def pick_up(self):
        self.falling = False
        self.velocity = 0

    def put_down(self):
        self.falling = True

    def shake(self):
        # Drop some coins if we so care to here
        print "Shake shake shake"

    def on_bin_collision(self, bin_type):
        pass

    def update(self, delta):
        # Update our position if we're falling
        if self.falling:
            self.velocity += self.gravity
            self.position[1] += self.velocity

        if self.position[1] > 600:
            self.position[0] = 400
            self.position[1] = 0
            self.velocity = 0

    def draw(self, surface):
        if self.image and self.rect:
            # Position the rectangle for correct drawing
            self.rect.center = self.position
            surface.blit(self.image, self.rect)


class GarmentRandomizer:
    def __init__(self, kernel, screen):
        self.kernel = kernel
        self.screen = screen
        self.weights = {'pants': 20, 'shirt': 40, 'sock': 10, 'undies': 30  }
        self.choice_list = []

        for item, weight in self.weights.iteritems():
            self.choice_list.extend([item] * weight)

    def next(self):
        garment_choice = random.choice(self.choice_list)
        
        # Choose if Biohazard
        if garment_choice == 'undies' or garment_choice == 'sock':
            biohazard_choice = (random.randint(0, 99) < 60)
        else:
            biohazard_choice = False

        # Choose how many coins in pockets
        if garment_choice == 'pants':
            coinage = random.randint(0, 5)
        else: 
            coinage = 0 

        print garment_choice, biohazard_choice, coinage

        return Garment(self.kernel, self.screen, garment_choice, biohazard_choice, coinage)

class Bins:
    def __init__(self, kernel, screen):
        self.bins = [
            'Lights',
            'Darks',
            'Biohazard'
        ]

        light_image, light_rect = kernel.image_manager.load("lights.bmp", True)
        dark_image, dark_rect = kernel.image_manager.load("darks.bmp", True)
        bio_image, bio_rect = kernel.image_manager.load("biohazard.bmp", True)

        self.bin_images = {
            'Lights': light_image,
            'Darks': dark_image,
            'Biohazard': bio_image,
        }

        self.bin_rects = {
            'Lights': light_rect,
            'Darks': dark_rect,
            'Biohazard': bio_rect,
        }

        self.bin_x_positions = [
            100,
            300,
            500
        ]

        # How long we've stayed in position
        self.ticks = 0
        self.randomize_time = 1500
        self.move_counter = 0
        self.y_position = 450

        self.y_position = 450

    def spin(self):
        # Randomize the order of the bins
        random.shuffle(self.bins)

    def garment_check(self, garment):
        for (bin, pos) in zip(self.bins, self.bin_x_positions):
            rect = pygame.Rect(pos, self.y_position, self.bin_rects[bin].width, self.bin_rects[bin].height)

            if rect.colliderect(garment.rect):
                return bin

        return None

    def update(self, delta):
        self.ticks += delta

        if self.ticks >= self.randomize_time:
            max_counter = 20

            t = (self.move_counter / float(max_counter)) * math.pi

            midpoint = (((max_counter / 2) - 1) / float(max_counter)) * math.pi

            if t != (math.pi / 2):
                movement = math.tan(t) / math.tan(midpoint)
                self.y_position += 100 * movement

            if self.move_counter == max_counter / 2:
                self.spin()

            if self.move_counter >= max_counter:
                self.move_counter = 0
                self.ticks = 0

            self.move_counter += 1

    def draw(self, surface):
        for (bin, x_position) in zip(self.bins, self.bin_x_positions):
            image = self.bin_images[bin]
            rect = self.bin_rects[bin]

            surface.blit(
                image,
                pygame.Rect(
                    x_position,
                    self.y_position,
                    rect.width,
                    rect.height
                )
            )

class Shelves:
    pass
