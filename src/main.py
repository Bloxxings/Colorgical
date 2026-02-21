import pygame  # python -m pip install pygame-ce
from player import PlayerClass
from map import MapClass
from cycle import DayNightCycleClass

class GameClass:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        
        """self.assets.load_cursor()
        self.assets.load_heart()"""

        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Gardening nightmares")
        self.running = True
        self.map = MapClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        

    def update(self, dividedTime):
        pressed_keys = pygame.key.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    if self.map.currentInteractionMode == "Moving":
                        self.map.isCurrentlyDraging = True
                        self.map.mousePositionOnLastFrame = mousePosition
                    elif self.map.currentInteractionMode == "Building":
                        pass

                if event.button == 4 and self.map.TILE_SIZE < 64: # Scroll up
                    self.map.TILE_SIZE += 4
                if event.button == 5 and self.map.TILE_SIZE > 12: # Scroll down
                    self.map.TILE_SIZE -= 4

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.map.isCurrentlyDraging = False
            if event.type == pygame.MOUSEMOTION:
                if self.map.isCurrentlyDraging and self.map.currentInteractionMode == "Moving":
                    mouseDifferenceX = mousePosition[0] - self.map.mousePositionOnLastFrame[0]
                    mouseDifferenceY = mousePosition[1] - self.map.mousePositionOnLastFrame[1]
                
                    self.map.x -= mouseDifferenceX
                    self.map.y -= mouseDifferenceY
                    self.map.mousePositionOnLastFrame = mousePosition

        self.map.move_player(pressed_keys)
        #self.dayNightCycle.update(dividedTime)
        

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Entities
        self.map.draw_map(self.screen)
        
        # UI 
        self.draw_fps()
        self.draw_coords()

    def draw_fps(self):
        fps_val = int(self.clock.get_fps())
        fps_surface = self.font.render(f"FPS: {fps_val}", True, (255, 255, 0))
        self.screen.blit(fps_surface, (20, 20))
        
    def draw_coords(self):
        # Draw coordinates
        x = self.map.x // self.map.TILE_SIZE
        y =self.map.y // self.map.TILE_SIZE
        coordinatesText = self.font.render(f"X:{x} Y:{y}",True,(225,225,225), (20, 20, 20))
        self.screen.blit(coordinatesText,(20, 70))


game = GameClass()

while game.running:
    dividedTime = game.clock.tick(60) / 1000
    game.update(dividedTime)
    game.draw()
    pygame.display.flip()

pygame.quit()   