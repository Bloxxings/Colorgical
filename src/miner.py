import pygame

class MinerClass:
    def __init__(miner,x,y,colorPatches):
        miner.x = x
        miner.y = y
        miner.color = colorPatches[(x,y)]
        miner.storage = []
        miner.mineCooldown = 60

    def mine(miner):
        if len(miner.storage) < 10 and miner.mineCooldown == 0:
            miner.storage.append(miner.color)
            miner.mineCooldown = 60
        else:
            miner.mineCooldown -= 1
        
    