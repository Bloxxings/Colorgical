import pygame

class MinerClass:
    def __init__(miner,x,y, direction, MinerSprites):
        miner.x = x
        miner.y = y
        miner.direction = direction
        miner.Sprites = MinerSprites
        miner.imagr = None
        miner.Crossings = [7, 11, 13, 14, 15]

        miner.binary = {"Right": 1, "Down": 2, "Left": 4, "Up": 8}

        miner.pick_asset({})
    
    def get_connections(miner, allPipes):
        connections = []
        check = {
            "Up": (miner.x, miner.y - 1),
            "Down": (miner.x, miner.y + 1),
            "Left": (miner.x - 1, miner.y),
            "Right": (miner.x + 1, miner.y)
        }
        for direction, coords in check.items():
            if coords in allPipes:
                connections.append(direction)
        return connections

    def calc_overlay_asset(miner, allPipes):
        connections = miner.get_connections(allPipes)
        
        if not connections:
            tileID = miner.binary.get(miner.direction, 1)
        else:
            neighbour = connections[0]
            
            assetID = miner.binary[neighbour] + miner.binary[miner.direction]
            
            assets = {
                5: 5,
                10: 10,
                9:  22 if neighbour == "Right" else 27,
                12: 23 if neighbour == "Up" else 28,
                6:  24 if neighbour == "Left" else 29,
                3:  25 if neighbour == "Down" else 26
            }
            tileID = assets.get(assetID, miner.binary[miner.direction])

        miner.image = miner.Sprites.get(tileID, miner.Sprites.get(1))

    def pick_asset(miner, allPipes):
        connections = miner.get_connections(allPipes)
        tileID = sum(miner.binary[d] for d in connections)
        
        if tileID == 0:
            tileID = miner.binary.get(miner.direction, 1)

        if tileID in miner.Crossings:
            return 
        else:
            miner.image = miner.Sprites.get(tileID, miner.Sprites.get(1))

    def draw_miner(miner, screen, camX, camY, TILE_SIZE, allPipes=None, overlay=False):
        drawX = miner.x * TILE_SIZE - camX
        drawY = miner.y * TILE_SIZE - camY

        if overlay:
            miner.calc_overlay_asset(allPipes if allPipes is not None else {})
            
            if miner.image:
                miner.image.set_alpha(120)
                mousePosition = pygame.mouse.get_pos()
                mouseX = mousePosition[0] - TILE_SIZE // 2
                mouseY = mousePosition[1] - TILE_SIZE // 2
                screen.blit(miner.image, (mouseX, mouseY))
        else:
            if miner.image:
                miner.image.set_alpha(255)
                screen.blit(miner.image, (drawX, drawY))
            else:
                miner.pick_asset(allPipes if allPipes is not None else {})
                if miner.image:
                    screen.blit(miner.image, (drawX, drawY))







""" Do we really keep this ?

def update_mine(miner):
        miner.mine()
        miner.empty_storage()

    def mine(miner):
        if miner.mineCooldown <= 0 and len(miner.storage) < 10:
            miner.storage.append(miner.color)
            miner.mineCooldown = 60
        else:
            miner.mineCooldown -= 1
        
    def empty_storage(miner):
        miner.outputcooldown -= 1 
        if miner.outputcooldown <= 0 and miner.output is not None and miner.storage != []:
            miner.outputs.append(miner.storage.pop())
            miner.outputcooldown = 30

    def draw_outputs(miner,screen,map):
        for i in range(len(miner.outputs)):
            drawX = (miner.output[0]+i) * map.TILE_SIZE - map.x + map.TILE_SIZE // 4
            drawY = miner.output[1] * map.TILE_SIZE - map.y + map.TILE_SIZE // 4
            pygame.draw.rect(screen,miner.outputs[i],(drawX,drawY,map.TILE_SIZE//2,map.TILE_SIZE//2))

"""