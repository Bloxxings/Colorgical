import pygame


class PipesClass:
    def __init__(pipes):
        pass
        

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