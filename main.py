# imports
from interface import Interface
from settings import *
import pygame,sys
from pygameUI import pygameUI

# Main class
class DGraph:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZES)
        self.clock = pygame.time.Clock()
        self.manager = pygameUI.UIManager(SIZES)
        self.interface = Interface(self.manager,self.quit)
    
    @internal
    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit()
            self.manager.handle_events(e)
            self.interface.event(e)
            self.interface.graph.event(e)
    
    @internal
    def update(self):
        self.interface.FPS_label.set_text(str(round(self.clock.get_fps(),2))+" FPS")
        self.manager.update_ui(0.016)
    
    @internal
    def draw(self):
        self.interface.graph.draw(self.screen)
        self.manager.draw_ui(self.screen)
        pygame.display.update()
    
    def quit(self):
        self.interface.save_to_files()
        pygame.quit()
        sys.exit()
    
    @external
    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
if __name__ == "__main__":
    # Create a new app and run it
    dgraph = DGraph()
    dgraph.run()