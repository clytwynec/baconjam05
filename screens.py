import engine

###################################################
class TestScreen(engine.Screen):
    def __init__(self, kernel):
        engine.Screen.__init__(self, kernel, 'Test Screen')

    def initialize(self):
        engine.Screen.initialize(self)

        print "This is a test of the screen system"

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
        