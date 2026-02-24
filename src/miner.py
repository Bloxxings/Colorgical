import pygame

class MinerClass:
    def __init__(miner,x,y,colorPatches):
        miner.x = x
        miner.y = y
        miner.color = colorPatches[(x,y)]
        miner.storage = []
        miner.mineCooldown = 60
        miner.outputcooldown = 30
        miner.output = [miner.x+1,miner.y]
        miner.outputs = []

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
            print("hello")
            miner.outputs.append(miner.storage.pop())
            miner.outputcooldown = 30

    def draw_outputs(miner,screen,map):
        for i in range(len(miner.outputs)):
            drawX = (miner.output[0]+i) * map.TILE_SIZE - map.x + map.TILE_SIZE // 4
            drawY = miner.output[1] * map.TILE_SIZE - map.y + map.TILE_SIZE // 4
            pygame.draw.rect(screen,miner.outputs[i],(drawX,drawY,map.TILE_SIZE//2,map.TILE_SIZE//2))