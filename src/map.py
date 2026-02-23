import pygame
import random

class MapClass:
    def __init__(map, screen_width, screen_height):
        map.SCREEN_WIDTH = screen_width
        map.SCREEN_HEIGHT = screen_height
        map.TILE_SIZE = 40
        map.PLAYER_SPEED = 10

        map.coreSize = 5
        map.coreX, map.coreY = 0, 0
        map.x = (map.coreX * map.TILE_SIZE) - (screen_width // 2) + (map.coreSize * map.TILE_SIZE // 2)
        map.y = (map.coreY * map.TILE_SIZE) - (screen_height // 2) + (map.coreSize * map.TILE_SIZE // 2)
        map.update_font_size()
        
        map.ColorPatches = {}
        map.colorSpacing = 50
        map.compute_ressources_position(5)

        map.ModifiedTiles = {}
        map.SurfaceCache = {}

        map.isCurrentlyDraging = False
        map.mousePositionOnLastFrame = (0, 0)
        map.placeBuilding = False

    def update_font_size(map):
        fontSize = int(map.TILE_SIZE * 0.8)
        map.coreTextFont = pygame.font.SysFont("Consolas", fontSize, bold=True)

    def compute_ressources_position(map, amountPerColor):
        map.Colors = [(250, 48, 48), # Red
                      (66, 222, 77), # Green
                      (51, 89, 224)] # Blue
        
        for color in map.Colors:
            for _ in range(amountPerColor):
                spawnX = random.randint(map.colorSpacing * -1, map.colorSpacing)
                spawnY = random.randint(map.colorSpacing * -1, map.colorSpacing)
                if abs(spawnX) < 10 and abs(spawnY) < 10:
                    spawnX += 20
                patchLength = random.randint(3, 5)
                patchSizeHeight = random.randint(3, 5)
                for x in range(patchLength):
                    for y in range(patchSizeHeight):
                        if random.random() > 0.1:
                            map.ColorPatches[(spawnX + x, spawnY + y)] = color

    def remove_building(map):
        mousePosition = pygame.mouse.get_pos()
        mouseTileX = (map.x + mousePosition[0]) // map.TILE_SIZE
        mouseTileY = (map.y + mousePosition[1]) // map.TILE_SIZE
        mouseTile = (mouseTileX, mouseTileY)
        if mouseTile in map.SurfaceCache:
            del map.SurfaceCache[mouseTile]

    def move_player(map, keys):
        nerf = 1
        keysPressed = [keys[pygame.K_d], keys[pygame.K_q], keys[pygame.K_z], keys[pygame.K_s]]
        
        pressedCount = sum(keysPressed)
        if pressedCount >= 2:
            nerf = 0.7071
        if not map.isCurrentlyDraging:
            if keys[pygame.K_d]:
                map.x += map.PLAYER_SPEED * nerf * (2 if keys[pygame.K_LSHIFT] else 1)
            if keys[pygame.K_q]:
                map.x -= map.PLAYER_SPEED * nerf * (2 if keys[pygame.K_LSHIFT] else 1)
            if keys[pygame.K_z]:
                map.y -= map.PLAYER_SPEED * nerf * (2 if keys[pygame.K_LSHIFT] else 1)
            if keys[pygame.K_s]:
                map.y += map.PLAYER_SPEED * nerf * (2 if keys[pygame.K_LSHIFT] else 1)
                
            map.x, map.y = round(map.x), round(map.y)



    def draw_pipe_logic(map, drawX, drawY, tileX, tileY, screen):
        pipeSize = map.TILE_SIZE//3
        offset = (map.TILE_SIZE - pipeSize) // 2
        pygame.draw.rect(screen, (40, 40, 45), (drawX + offset, drawY + offset, pipeSize, pipeSize))

        Neighbours = {
        (tileX, tileY - 1): (offset, 0, pipeSize, offset),                  # Up
        (tileX, tileY + 1): (offset, offset + pipeSize, pipeSize, offset),  # Down
        (tileX - 1, tileY): (0, offset, offset, pipeSize),                  # Left
        (tileX + 1, tileY): (offset + pipeSize, offset, offset, pipeSize)   # Right
    }

        for coordinates, rectangle in Neighbours.items():
            if map.SurfaceCache.get(coordinates) == "Pipe":
                pygame.draw.rect(screen, (40, 40, 45), (drawX + rectangle[0], drawY + rectangle[1], rectangle[2], rectangle[3]))



    def draw_core(map, screen):
        coreDrawX = (map.coreX * map.TILE_SIZE) - map.x
        coreDrawY = (map.coreY * map.TILE_SIZE) - map.y
        corePixelSize = map.coreSize * map.TILE_SIZE

        if (coreDrawX + corePixelSize > 0 and coreDrawX < map.SCREEN_WIDTH and 
            coreDrawY + corePixelSize > 0 and coreDrawY < map.SCREEN_HEIGHT):
            pygame.draw.rect(screen, (50, 51, 63), (coreDrawX, coreDrawY, corePixelSize, corePixelSize))
            padding = map.TILE_SIZE // 4
            pygame.draw.rect(screen, (220, 220, 230), 
                             (coreDrawX + padding, coreDrawY + padding, 
                              corePixelSize - (padding * 2), corePixelSize - (padding * 2)))
            levelText = map.coreTextFont.render("Level 1", True, (10, 10, 10))

            textRect = levelText.get_rect(center=(coreDrawX + corePixelSize // 2,
                                                  coreDrawY + corePixelSize // 2 +  1.75 * map.TILE_SIZE))
            
            screen.blit(levelText, textRect)


    def draw_map(map, screen, selectedSlot):
        startScreenX = int(map.x // map.TILE_SIZE)
        startScreenY = int(map.y // map.TILE_SIZE)
        endScreenX = int((map.x + map.SCREEN_WIDTH) // map.TILE_SIZE) + 2
        endScreenY = int((map.y + map.SCREEN_HEIGHT) // map.TILE_SIZE) + 3

        mousePosition = pygame.mouse.get_pos()
        mouseTileX = (map.x + mousePosition[0]) // map.TILE_SIZE
        mouseTileY = (map.y + mousePosition[1]) // map.TILE_SIZE

        for tileY in range(startScreenY, endScreenY):
            for tileX in range(startScreenX, endScreenX):
                drawX = tileX * map.TILE_SIZE - map.x
                drawY = tileY * map.TILE_SIZE - map.y
                tileColor = (66, 67, 79)
                if map.TILE_SIZE < 20:
                    outlineColor = (68, 69, 81) # Barely visible against tileColor 
                else:
                    outlineColor = (71, 72, 84)

                if (tileX, tileY) in map.ColorPatches:
                    tileColor = map.ColorPatches[(tileX, tileY)]
                    outlineColor = tileColor
                pygame.draw.rect(screen, tileColor, (drawX, drawY, map.TILE_SIZE, map.TILE_SIZE))
                pygame.draw.rect(screen, outlineColor, (drawX, drawY, map.TILE_SIZE, map.TILE_SIZE), 1)

                if (tileX, tileY) in map.SurfaceCache:
                    buildingType = map.SurfaceCache[(tileX, tileY)]
                    if buildingType == "Pipe":
                        map.draw_pipe_logic(drawX, drawY, tileX, tileY, screen)

                    elif buildingType == "placeholder":
                        centerX = drawX + map.TILE_SIZE // 2
                        centerY = drawY + map.TILE_SIZE // 2
                        pygame.draw.circle(screen, (255, 50, 255), (centerX, centerY), map.TILE_SIZE // 3)

        map.draw_core(screen)

        isInCore = map.coreX <= mouseTileX < (map.coreX + map.coreSize) and \
                   map.coreY <= mouseTileY < (map.coreY + map.coreSize)
        
        if map.placeBuilding:
            pygame.draw.circle(screen, (255, 50, 255), (mouseTileX - map.TILE_SIZE//2, mouseTileY - map.TILE_SIZE//2), map.TILE_SIZE/2)
            if not isInCore:
                map.SurfaceCache[(mouseTileX, mouseTileY)] = "Pipe" if selectedSlot == 0 else "placeholder"

        if selectedSlot is not None:
            buildingOverlayX = mouseTileX * map.TILE_SIZE - map.x
            buildingOverlayY = mouseTileY * map.TILE_SIZE - map.y

            buildingOverlaySurface = pygame.Surface((map.TILE_SIZE, map.TILE_SIZE))
            buildingOverlaySurface.set_alpha(120)


            if isInCore:
                overlayColor = (255, 50, 50)
            else:
                overlayColor = (255, 255, 255)

            buildingOverlaySurface.fill(overlayColor)
            screen.blit(buildingOverlaySurface, (buildingOverlayX, buildingOverlayY))
            pygame.draw.rect(screen, overlayColor,
                             (buildingOverlayX, buildingOverlayY, map.TILE_SIZE, map.TILE_SIZE), 1)