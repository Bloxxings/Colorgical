import pygame
import random
import math
from opensimplex import OpenSimplex


class TerrainGenClass:
    def __init__(terrain, screen_width, screen_height):
        terrain.SCREEN_WIDTH = screen_width
        terrain.SCREEN_HEIGHT = screen_height
        terrain.TILE_SIZE = 40
        terrain.PLAYER_SPEED = 10
        terrain.x, terrain.y = 0, 0
        terrain.NoiseMap = OpenSimplex(seed=random.randint(0, 1000000))
        terrain.ModifiedTiles = {}
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



    def draw_terrain(terrain, screen):
        noiseScale = 0.05

        startScreenX = int(terrain.x // terrain.TILE_SIZE)
        startScreenY = int(terrain.y // terrain.TILE_SIZE)
        endScreenX = int((terrain.x + terrain.SCREEN_WIDTH) // terrain.TILE_SIZE) + 2
        endScreenY = int((terrain.y + terrain.SCREEN_HEIGHT) // terrain.TILE_SIZE) + 3
        

        for tileY in range(startScreenY, endScreenY):
            for tileX in range(startScreenX, endScreenX):
                drawX = tileX * terrain.TILE_SIZE - terrain.x
                drawY = tileY * terrain.TILE_SIZE - terrain.y

                tileColor = (terrain.NoiseMap.noise2(tileX * noiseScale, tileY * noiseScale) + 2) * 128
                rgb = (tileColor, tileColor, tileColor)

                pygame.draw.rect(screen, rgb, (0, 0, terrain.TILE_SIZE, terrain.TILE_SIZE))
                tileSurface = (rgb, (0, 0, terrain.TILE_SIZE, terrain.TILE_SIZE))

                terrain.SurfaceCache[(tileX, tileY)] = (tileSurface, drawX, drawY)