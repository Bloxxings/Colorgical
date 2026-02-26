import pygame  # python -m pip install pygame-ce
from map import MapClass
from buildings import BuildingsClass
from miner import MinerClass

class GameClass:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()

        self.font = pygame.font.SysFont("Consolas", 24, bold=True)
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Gardening nightmares")
        self.running = True
        self.coordsMouseMode = False
        self.map = MapClass(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.buildings = BuildingsClass()
        self.isDeleting = False
        

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.buildings.currentInteractionMode == "Moving":
                        self.map.isCurrentlyDraging = True
                        self.map.mousePositionOnLastFrame = mousePosition
                    elif self.buildings.currentInteractionMode == "Building":
                        self.map.placeBuilding = True
            

                if event.button == 3:
                    self.isDeleting = True

                if event.button == 4 and self.map.TILE_SIZE < 64: # Scroll up
                    self.map.TILE_SIZE += 4
                    self.map.update_font_size()
                    self.map.zoom_assets()
                if event.button == 5 and self.map.TILE_SIZE > 20: # Scroll down
                    self.map.TILE_SIZE -= 4
                    self.map.update_font_size()
                    self.map.zoom_assets()

            self.buildings.handle_event(event, mousePosition, self.screen, self.map)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.map.isCurrentlyDraging = False
                    self.map.placeBuilding = False
                if event.button == 3:
                    self.isDeleting = False

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
                directions = ["Right", "Down", "Left", "Up"]
                if self.buildings.currentInteractionMode == "Building":
                    if event.key == pygame.K_r:
                        currentDirection = directions.index(self.map.direction)
                        self.map.direction = directions[(currentDirection + 1) % 4]
                    if event.key == pygame.K_e:
                        currentDirection = directions.index(self.map.direction)
                        self.map.direction = directions[(currentDirection - 1) % 4]

        if self.isDeleting:
            self.map.remove_building()
        for building in self.map.SurfaceCache.values():
            if type(building) is MinerClass:
                building.update_mine()
        self.map.move_player(pressed_keys)

    def draw(self):
        startScreenX = self.map.x // self.map.TILE_SIZE
        startScreenY = self.map.y // self.map.TILE_SIZE
        endScreenX = (self.map.x + self.SCREEN_WIDTH) // self.map.TILE_SIZE
        endScreenY = (self.map.y + self.SCREEN_HEIGHT) // self.map.TILE_SIZE
        self.screen.fill((0, 0, 0))
        self.map.draw_map(self.screen, self.buildings.selectedSlot,self.buildings.hotbar, self.buildings.currentInteractionMode)
        for (x, y), pipe in self.map.Pipes.items():
            if (startScreenX - 1 <= x <= endScreenX + 1 and
               startScreenY - 1 <= y <= endScreenY + 1):
                pipe.draw_pipe(self.screen, self.map.x, self.map.y, self.map.TILE_SIZE)

        for building in self.map.SurfaceCache.values():
            if type(building) is MinerClass:
                building.draw_outputs(self.screen,self.map)
        
        # UI 
        self.draw_fps()
        self.draw_coords()
        self.buildings.draw_building_bar(self.screen,self.map.everyBuilding)

    def draw_fps(self):
        fps_val = int(self.clock.get_fps())
        fps_surface = self.font.render(f"FPS: {fps_val}", True, (255, 255, 255))
        self.screen.blit(fps_surface, (20, 20))
        
    def draw_coords(self):
        # Draw coordinates
        x = (self.map.x + self.SCREEN_WIDTH//2) // self.map.TILE_SIZE
        y = (self.map.y + self.SCREEN_HEIGHT//2) // self.map.TILE_SIZE
        coordinatesText = self.font.render(f"X:{pygame.mouse.get_pos()[0] if self.coordsMouseMode else \
                                          x} Y:{pygame.mouse.get_pos()[1] if self.coordsMouseMode else y}",
                                          True,(225,225,225), (20, 20, 20))
        
        self.screen.blit(coordinatesText,(20, 70))
        mode = "Mouse coordinates" if self.coordsMouseMode else "Map coordinates"
        modeText = self.font.render(mode,True,(252, 215, 180))
        self.screen.blit(modeText, (20, 110))


game = GameClass()

while game.running:
    game.update()
    game.draw()
    pygame.display.flip()
    game.clock.tick(60)

pygame.quit()
