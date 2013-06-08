import engine

###################################################
class TestScreen(engine.Screen):
    def __init__(self, kernel):
        engine.Screen.__init__(self, kernel, 'Test Screen')

    def initialize(self):
        engine.Screen.initialize(self)

        print "This is a test of the screen system"

###################################################