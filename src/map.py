import pygame
import random
from pipes import PipeClass
from miner import MinerClass
import os



class MapClass:
    def __init__(map, screen_width, screen_height):

        map.base_path = os.path.dirname(os.path.abspath(__file__))
        map.root_path = os.path.join(map.base_path, "..")
        map.assets_path = os.path.join(map.root_path, "assets")

        map.SCREEN_WIDTH = screen_width
        map.SCREEN_HEIGHT = screen_height
        map.TILE_SIZE = 40
        map.PLAYER_SPEED = 10

        map.coreSize = 6
        map.coreX, map.coreY = -3 , -3
        map.x = (map.coreX * map.TILE_SIZE) - (screen_width // 2) + (map.coreSize * map.TILE_SIZE // 2)
        map.y = (map.coreY * map.TILE_SIZE) - (screen_height // 2) + (map.coreSize * map.TILE_SIZE // 2)
        
        map.ColorPatches = {}
        map.colorSpacing = 50

        map.ModifiedTiles = {}
        map.SurfaceCache = {}

        map.isCurrentlyDraging = False
        map.mousePositionOnLastFrame = (0, 0)
        map.placeBuilding = False

        map.Pipes = {}
        map.direction = "Right"

        # Name associated with image for the inventory
        pipeImage = pygame.image.load("assets/pipes/pipe17.png").convert_alpha()
        map.everyBuilding = {"Pipe" : pipeImage}

        arrow_full_path = os.path.join(map.assets_path, "arrow.png")
        map.arrowSprite = pygame.image.load(arrow_full_path).convert_alpha()

        # Pipes
        map.PipeSprites = {}
        for i in range(1, 25):
            p_path = os.path.join(map.assets_path, "pipes", f"pipe{i}.png")
            if os.path.exists(p_path):
                img = pygame.image.load(p_path).convert_alpha()
                map.PipeSprites[i] = pygame.transform.scale(img, (map.TILE_SIZE, map.TILE_SIZE))

        map.update_font_size()
        map.compute_ressources_position(5)

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
        if mouseTile in map.Pipes:
            del map.Pipes[mouseTile]
            x, y = mouseTile
            Neighbours = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
            for coordinates in Neighbours:
                if coordinates in map.Pipes:
                    map.Pipes[coordinates].pick_asset(map.Pipes)
        elif mouseTile in map.SurfaceCache:
            del map.SurfaceCache[mouseTile]

    def move_player(map, keys):
        nerf = 1
        keysPressed = [keys[pygame.K_d], keys[pygame.K_q], keys[pygame.K_z], keys[pygame.K_s]]
        
        pressedCount = sum(keysPressed)
        if pressedCount == 2:
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


    def draw_arrow(map, screen, drawX, drawY, direction):
        directions = {"Right":0, "Up":1, "Left":2, "Down":3}
        arrow = pygame.transform.scale(map.arrowSprite, (map.TILE_SIZE, map.TILE_SIZE))
        arrow = pygame.transform.rotate(arrow, 90*directions[direction])
        screen.blit(arrow, (drawX, drawY, map.TILE_SIZE, map.TILE_SIZE))


    def draw_map(map, screen, selectedSlot, hotbar, interactionMode):
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

                    if type(buildingType) is MinerClass:
                        centerX = drawX + map.TILE_SIZE // 2
                        centerY = drawY + map.TILE_SIZE // 2
                        pygame.draw.circle(screen, (255, 127, 0), (centerX, centerY), map.TILE_SIZE // 3)
        

        isInCore = map.coreX <= mouseTileX < (map.coreX + map.coreSize) and \
                   map.coreY <= mouseTileY < (map.coreY + map.coreSize)
        
        if map.placeBuilding and not isInCore:
            item = hotbar[selectedSlot]
            
            if item == "Miner":
                if (mouseTileX, mouseTileY) in map.ColorPatches:
                    map.SurfaceCache[(mouseTileX, mouseTileY)] = MinerClass(mouseTileX, mouseTileY, map.ColorPatches)

            elif item == "Pipe":
                if (mouseTileX, mouseTileY) not in map.Pipes:
                    map.Pipes[(mouseTileX, mouseTileY)] = PipeClass(mouseTileX, mouseTileY, map.direction, map.PipeSprites)

                    for neighbourX, neighbourY in [(0,0), (0,-1), (0,1), (-1,0), (1,0)]:
                        target = (mouseTileX + neighbourX, mouseTileY + neighbourY)
                        if target in map.Pipes:
                            map.Pipes[target].pick_asset(map.Pipes)
            else:
                map.SurfaceCache[(mouseTileX, mouseTileY)] = item


        if interactionMode == "Building" and selectedSlot is not None:
            overlayX = mouseTileX * map.TILE_SIZE - map.x
            overlayY = mouseTileY * map.TILE_SIZE - map.y

            overlaySurf = pygame.Surface((map.TILE_SIZE, map.TILE_SIZE), pygame.SRCALPHA)
            overlayColor = (255, 50, 50, 120) if isInCore else (255, 255, 255, 120)
            
            overlaySurf.fill(overlayColor)
            screen.blit(overlaySurf, (overlayX, overlayY))

            map.draw_arrow(screen, overlayX, overlayY, map.direction)

        map.draw_core(screen)














































































































































































































class TheGuyReadingThisCode:
    def __init__(you):
        you.getNoBitches = True
