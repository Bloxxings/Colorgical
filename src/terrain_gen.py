import pygame
import random
import math
from opensimplex import OpenSimplex

from config import Assets


def get_random_value(x, y, randomNumber):
    return ((math.sin(x * 12.9898 + y * 78.233 + randomNumber) * 43758.5453) % 1)


class TerrainGenClass:
    def __init__(terrain, screen_width, screen_height):
        terrain.SCREEN_WIDTH = screen_width
        terrain.SCREEN_HEIGHT = screen_height
        terrain.TILE_SIZE = 40
        terrain.PLAYER_SPEED = 10
        terrain.x, terrain.y = 0, 0
        terrain.tmpNoiseBiomes = OpenSimplex(seed=random.randint(0, 1000000))
        terrain.tmpNoiseWater = OpenSimplex(seed=random.randint(0, 1000000))
        terrain.lightOverlay = pygame.Surface((terrain.TILE_SIZE, terrain.TILE_SIZE), pygame.SRCALPHA)
        terrain.lightOverlay.fill((200, 200, 200, 50))  
        terrain.mouseHighlightOverlay = pygame.Surface((terrain.TILE_SIZE, terrain.TILE_SIZE), pygame.SRCALPHA)
        terrain.mouseHighlightOverlay.fill((255, 255, 255, 100)) 
        terrain.ModifiedTiles = {}

        terrain.assets = Assets(terrain.TILE_SIZE)
        terrain.assets.load_grass() # Get an image : terrain.assets.GrassList[index]
        terrain.assets.load_farmland()
        terrain.assets.load_nature()
        terrain.assets.load_tree()
        terrain.assets.load_lake()

        terrain.SurfaceCache = {}

    def move_player(terrain, keys):
        nerf = 1
        keysPressed = [keys[pygame.K_d],keys[pygame.K_q],keys[pygame.K_z],keys[pygame.K_s]]
        pressedKeysNumber = 0
        for keyIsPressed in keysPressed:
            if keyIsPressed:
                pressedKeysNumber += 1
        if pressedKeysNumber == 2:
            nerf = (((terrain.PLAYER_SPEED**2)/2)**0.5)/terrain.PLAYER_SPEED 
        if keys[pygame.K_d]:
            terrain.x += terrain.PLAYER_SPEED*nerf
        if keys[pygame.K_q]:
            terrain.x -= terrain.PLAYER_SPEED*nerf
        if keys[pygame.K_z]:
            terrain.y -= terrain.PLAYER_SPEED*nerf
        if keys[pygame.K_s]:
            terrain.y += terrain.PLAYER_SPEED*nerf
        terrain.x,terrain.y = round(terrain.x),round(terrain.y)

    def modify_tile(terrain, mousePos, newTileType):
        tileX = (terrain.x + mousePos[0]) // terrain.TILE_SIZE
        tileY = (terrain.y + mousePos[1]) // terrain.TILE_SIZE
        if (tileX, tileY) in terrain.ModifiedTiles:
            return 
        elif newTileType == "farmland":
            terrain.ModifiedTiles[(tileX, tileY)] = terrain.assets.Blocks.EveryBlock["farmland"]
            if (tileX, tileY) in terrain.SurfaceCache:
                del terrain.SurfaceCache[(tileX, tileY)]



    def draw_terrain(terrain, screen):
        biomeScale = 0.05

        startScreenX = int(terrain.x // terrain.TILE_SIZE)
        startScreenY = int(terrain.y // terrain.TILE_SIZE)
        endScreenX = int((terrain.x + terrain.SCREEN_WIDTH) // terrain.TILE_SIZE) + 2
        endScreenY = int((terrain.y + terrain.SCREEN_HEIGHT) // terrain.TILE_SIZE) + 3
        
        playerTileX = (terrain.x + terrain.SCREEN_WIDTH // 2) // terrain.TILE_SIZE
        playerTileY = (terrain.y + terrain.SCREEN_HEIGHT // 2) // terrain.TILE_SIZE

        mouseTileX = (terrain.x + pygame.mouse.get_pos()[0]) // terrain.TILE_SIZE
        mouseTileY = (terrain.y + pygame.mouse.get_pos()[1]) // terrain.TILE_SIZE

        for tileY in range(startScreenY, endScreenY):
            for tileX in range(startScreenX, endScreenX):
                drawX = tileX * terrain.TILE_SIZE - terrain.x
                drawY = tileY * terrain.TILE_SIZE - terrain.y

                terrain.draw_tile(biomeScale, tileX, tileY, drawX, drawY, screen)
                if tileX == playerTileX and tileY == playerTileY:
                    screen.blit(terrain.lightOverlay, (drawX, drawY))

                if tileX == mouseTileX and tileY == mouseTileY:
                    screen.blit(terrain.mouseHighlightOverlay, (drawX, drawY))
                

    def draw_tile(terrain, biomeScale, tileX, tileY, drawX, drawY, screen):
        
        # Check modified tiles
        if (tileX, tileY) in terrain.ModifiedTiles:
            screen.blit(terrain.ModifiedTiles[(tileX, tileY)], (drawX, drawY))
            return 
        
        # Check cache 
        if (tileX, tileY) in terrain.SurfaceCache:
            cached = terrain.SurfaceCache[(tileX, tileY)]
            if isinstance(cached, tuple):
                surf, xOff, yOff = cached
                screen.blit(surf, (drawX - xOff, drawY - yOff))
            else:
                screen.blit(cached, (drawX, drawY))
            return

        tileSurface = pygame.Surface((terrain.TILE_SIZE * 3, terrain.TILE_SIZE * 3), pygame.SRCALPHA)
        baseDrawX = terrain.TILE_SIZE
        baseDrawY = terrain.TILE_SIZE * 2

        randomValueGrassWater = get_random_value(tileX, tileY, 174)
        randomValueNatureTree = get_random_value(tileX, tileY, 194)


        # Biome (grass type)
        noiseValueBiome = terrain.tmpNoiseBiomes.noise2(tileX * biomeScale, tileY * biomeScale)
        grassType = 0 if noiseValueBiome < -0.333 else (3 if noiseValueBiome < 0.333 else 6)


        # Water
        noiseValueWater = terrain.tmpNoiseWater.noise2(tileX * biomeScale * 2, tileY * biomeScale * 2)

        if noiseValueWater < -0.6:
            lakeType = 0 if randomValueGrassWater < 0.8 else (1 if randomValueGrassWater < 0.95 else 2)
            tileSurface.blit(terrain.assets.LakeList[lakeType], (baseDrawX, baseDrawY))
        else:

            # Foliage
            foliageType = 0 if randomValueGrassWater < 0.9 else (1 if randomValueGrassWater < 0.97 else 2)
            tileSurface.blit(terrain.assets.GrassList[foliageType + grassType], (baseDrawX, baseDrawY))


            # Nature and Trees
            if grassType == 3:
                if randomValueNatureTree < 0.01:
                    natureChoice = terrain.assets.NatureList[int(randomValueGrassWater * len(terrain.assets.NatureList))]
                    tileSurface.blit(natureChoice, (baseDrawX, baseDrawY))
                elif randomValueNatureTree < 0.02:
                    treeChoice = terrain.assets.TreesList[int(randomValueGrassWater * len(terrain.assets.TreesList))]
                    tileSurface.blit(treeChoice, (baseDrawX - terrain.TILE_SIZE, baseDrawY - terrain.TILE_SIZE*2))
                    
        terrain.SurfaceCache[(tileX, tileY)] = (tileSurface, baseDrawX, baseDrawY)
        screen.blit(tileSurface, (drawX - baseDrawX, drawY - baseDrawY))