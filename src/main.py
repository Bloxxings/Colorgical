import pygame  # python -m pip install pygame-ce
from map import MapClass
from buildings import BuildingsClass

class GameClass:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        
        """self.assets.load_cursor()
        self.assets.load_heart()"""

        self.font = pygame.font.SysFont("Consolas", 24, bold=True)
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Gardening nightmares")
        self.running = True
        self.coordsMouseMode = False
        self.map = MapClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.buildings = BuildingsClass()
        

    def update(self, dividedTime):
        pressed_keys = pygame.key.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        for event in pygame.event.get():
            self.buildings.handle_event(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    if self.buildings.currentInteractionMode == "Moving":
                        self.map.isCurrentlyDraging = True
                        self.map.mousePositionOnLastFrame = mousePosition
                    elif self.buildings.currentInteractionMode == "Building":
                        pass

                if event.button == 4 and self.map.TILE_SIZE < 64: # Scroll up
                    self.map.TILE_SIZE += 4
                    self.map.update_font_size()
                if event.button == 5 and self.map.TILE_SIZE > 20: # Scroll down
                    self.map.TILE_SIZE -= 4
                    self.map.update_font_size()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.map.isCurrentlyDraging = False
            if event.type == pygame.MOUSEMOTION:
                if self.map.isCurrentlyDraging and self.buildings.currentInteractionMode == "Moving":
                    mouseDifferenceX = mousePosition[0] - self.map.mousePositionOnLastFrame[0]
                    mouseDifferenceY = mousePosition[1] - self.map.mousePositionOnLastFrame[1]
                
                    self.map.x -= mouseDifferenceX
                    self.map.y -= mouseDifferenceY
                    self.map.mousePositionOnLastFrame = mousePosition
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.coordsMouseMode =  not self.coordsMouseMode

        self.map.move_player(pressed_keys)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw_map(self.screen, self.buildings.selectedSlot)
        
        # UI 
        self.draw_fps()
        self.draw_coords()
        self.buildings.draw_building_bar(self.screen)

    def draw_fps(self):
        fps_val = int(self.clock.get_fps())
        fps_surface = self.font.render(f"FPS: {fps_val}", True, (255, 255, 255))
        self.screen.blit(fps_surface, (20, 20))
        
    def draw_coords(self):
        # Draw coordinates
        x = self.map.x // self.map.TILE_SIZE
        y =self.map.y // self.map.TILE_SIZE
        coordinatesText = self.font.render(f"X:{pygame.mouse.get_pos()[0] if self.coordsMouseMode else x} Y:{pygame.mouse.get_pos()[1] if self.coordsMouseMode else y}",True,(225,225,225), (20, 20, 20))
        self.screen.blit(coordinatesText,(20, 70))
        mode = "Mouse coordinates" if self.coordsMouseMode else "Map coordinates"
        modeText = self.font.render(mode,True,(252, 215, 180))
        self.screen.blit(modeText, (20, 110))


game = GameClass()

while game.running:
    dividedTime = game.clock.tick(60) / 1000
    game.update(dividedTime)
    game.draw()
    pygame.display.flip()

pygame.quit()
