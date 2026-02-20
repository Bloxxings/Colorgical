import pygame  # python.exe -m pip install pygame-ce
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
        
        self.assets = Assets()
        self.assets.load_cursor()
        self.assets.load_heart()

        self.fps_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Gardening nightmares")
        self.running = True
        self.terrain = TerrainGenClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.player = PlayerClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.enemy = EnemyClass(100, 100, self.player, self.terrain)
        self.inventory = InventoryClass(self)
        self.dayNightCycle = DayNightCycleClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        

    def update(self, dividedTime):
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                if self.inventory.hotbar[self.inventory.selectedHotbarSlot] == "hoe":
                    self.terrain.modify_tile(pygame.mouse.get_pos(), "farmland")
                elif self.inventory.hotbar[self.inventory.selectedHotbarSlot] == "sword" and self.player.swingCooldown == 0:
                    self.player.isSwinging = True
            elif event.type == pygame.TEXTINPUT:
                self.inventory.select_hotbar_slot(event.text)
        
        self.terrain.move_player(pressed_keys)
        self.enemy.update()
        self.dayNightCycle.update(dividedTime)
        

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Entities
        self.terrain.draw_terrain(self.screen)
        self.enemy.draw(self.screen)
        self.player.draw_player(self.screen)
        self.player.draw_held_tool(self.screen,self.inventory.EveryBlocks,
                                   self.inventory.hotbar[self.inventory.selectedHotbarSlot])
        
        # UI 
        self.dayNightCycle.draw(self.screen)
        self.player.draw_player_info(self.screen,self.assets.heart,self.terrain)
        self.inventory.draw_hotbar(self.screen)
        
        self.draw_fps()
        self.draw_mouse()

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