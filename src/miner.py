import pygame

class MinerClass:
    def __init__(miner,x,y,colorPatches):
        miner.x = x
        miner.y = y
        miner.color = colorPatches[(x,y)]
        miner.storage = []
        miner.mine_cooldown = 60

    def mine(miner):
        if len(miner.storage) < 10 and miner.mine_cooldown == 0:
            miner.storage.append(miner.color)
            miner.mine_cooldown = 60
        else:
            miner.mine_cooldown -= 1