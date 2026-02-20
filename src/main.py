import pygame  # python -m pip install pygame-ce
from player import PlayerClass
from terrain_gen import TerrainGenClass
from cycle import DayNightCycleClass

class GameClass:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        pygame.mouse.set_visible(False)
        
        """self.assets.load_cursor()
        self.assets.load_heart()"""

        self.fps_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Gardening nightmares")
        self.running = True
        self.terrain = TerrainGenClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        #self.player = PlayerClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        #self.dayNightCycle = DayNightCycleClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        

    def update(self, dividedTime):
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
        
        self.terrain.move_player(pressed_keys)
        

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Entities
        self.terrain.draw_terrain(self.screen)
        
        # UI 
        
        self.draw_fps()
        #self.draw_mouse()

    def draw_fps(self):
        fps_val = int(self.clock.get_fps())
        fps_surface = self.fps_font.render(f"FPS: {fps_val}", True, (255, 255, 0))
        self.screen.blit(fps_surface, (20, 20))

    def draw_mouse(self):
        mousePos = pygame.mouse.get_pos()
        self.screen.blit(self.assets.cursor, mousePos)
        

game = GameClass()

while game.running:
    dividedTime = game.clock.tick(60) / 1000
    game.update(dividedTime)
    game.draw()
    pygame.display.flip()

pygame.quit()