import pygame

class MinerClass:
    def __init__(miner,x,y,colorPatches):
        miner.x = x
        miner.y = y
        miner.color = colorPatches[(x,y)]
        miner.storage = []
        miner.mineCooldown = 60
        miner.outputcooldown = 30
        miner.output = (miner.x+1,miner.y)

    def mine(miner):
        if len(miner.storage) < 10 and miner.mineCooldown == 0:
            miner.storage.append(miner.color)
            miner.mineCooldown = 60
        else:
            miner.mine_cooldown -= 1
        
    def empty_storage(miner):
        if miner.output is not None:
            miner.outputcooldown -= 1 
            #if miner.outputcooldown == 0:
                
