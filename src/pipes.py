class PipeClass:
    def __init__(self, x, y, direction, Sprites):
        self.x = x
        self.y = y
        self.direction = direction
        self.Sprites = Sprites
        self.startDirection = None
        self.endDirection = direction
        self.image = None
        self.pick_asset({})

    def get_connections(self, allPipes):
        connections = []
        check = {
            "Up": (self.x, self.y - 1),
            "Down": (self.x, self.y + 1),
            "Left": (self.x - 1, self.y),
            "Right": (self.x + 1, self.y)
        }
        
        for direction, coords in check.items():
            if coords in allPipes:
                connections.append(direction)
        return connections
        
    def pick_asset(self, allPipes):
        connections = self.get_connections(allPipes)
        
        binary = {"Right": 1, "Down": 2, "Left": 4, "Up": 8}
        tileID = sum(binary[d] for d in connections)
        if tileID == 0:
            tileID = binary.get(self.direction, 1)

        self.image = self.Sprites.get(tileID, self.Sprites.get(1))

    def draw_pipe(self, screen, camX, camY, TILE_SIZE):
        drawX = self.x * TILE_SIZE - camX
        drawY = self.y * TILE_SIZE - camY
        screen.blit(self.image, (drawX, drawY))















"""
class PipeClass:
    def __init__(pipe,x,y,map):
        pipe.x = x
        pipe.y = y
        pipe.SIZE = map.TILE_SIZE//3
        pipe.neighbours = {
            "Up" : (pipe.x, pipe.y - 1),
            "Down" : (pipe.x, pipe.y + 1),
            "Right" : (pipe.x + 1, pipe.y),
            "Left" : (pipe.x - 1, pipe.y)

            #"UpRight" : (pipe.x + 1, pipe.y - 1),
            #"UpLeft" : (pipe.x - 1, pipe.y - 1),
            #"DownRight" : (pipe.x + 1, pipe.y + 1),
            #"DownLeft" : (pipe.x - 1, pipe.y + 1)
        }
        pipe.previous_pipe = None
        pipe.next_pipe = None
        pipe.previous_direction = None
        pipe.next_direction = None
        pipe.object = None
        
        
    def update_pipe(pipe,map):
        if pipe.previous_pipe is None or not (pipe.previous_pipe.x,pipe.previous_pipe.y) in map.pipes.keys():
            pipe.get_pipe_links(map)
        pipe.get_direction(map)
    
    def get_pipe_links(pipe,map):
        neighbours = [1 if dir in map.pipes.keys() else 0 for dir in pipe.neighbours.values()]
        if sum(neighbours) == 0:
            pipe.previous_pipe = None
        else:
            possibilities = []
            for neighbour in pipe.neighbours.values():
                if neighbour in map.pipes.keys():
                    if map.pipes[neighbour].next_pipe is None:
                        possibilities.append(neighbour)
            if len(possibilities) == 1:
                chosen = map.pipes[possibilities[0]]
                if list(map.pipes.keys()).index((pipe.x,pipe.y)) < list(map.pipes.keys()).index((chosen.x,chosen.y)):
                    if pipe.next_pipe is None:
                        pipe.previous_pipe = None
                        chosen.previous_pipe = pipe
                        pipe.next_pipe = chosen
                    elif chosen.previous_pipe != pipe:
                        pipe.previous_pipe = chosen
                        chosen.next_pipe = pipe
                else:
                    if chosen.next_pipe is None:
                        pipe.previous_pipe = chosen
                        chosen.next_pipe = pipe
                    elif chosen.previous_pipe is None:
                        pipe.next_pipe = chosen
                        chosen.previous_pipe = pipe
    
    def get_direction(pipe,map):
        if pipe.previous_pipe is not None:
            for direction, tile in pipe.neighbours.items():
                if tile in map.pipes.keys():
                    if map.pipes[tile] == pipe.previous_pipe:
                        pipe.previous_direction = direction
        else:
            pipe.previous_direction = None
        
        if pipe.next_pipe is not None:
            for direction, tile in pipe.neighbours.items():
                if tile in map.pipes.keys():
                    if map.pipes[tile] == pipe.next_pipe:
                        pipe.next_direction = direction
        else:
            pipe.next_direction = None
        

    def draw_pipe_logic(pipe, map, screen):
        offset = (map.TILE_SIZE - pipe.SIZE) // 2
        drawX = pipe.x * map.TILE_SIZE - map.x
        drawY = pipe.y * map.TILE_SIZE - map.y
        pygame.draw.rect(screen, (40, 40, 45), (drawX + offset, drawY + offset, pipe.SIZE, pipe.SIZE))
        Neighbours = {
        "Up": (offset, 0, pipe.SIZE, offset),                  
        "Down": (offset, offset + pipe.SIZE, pipe.SIZE, offset),  
        "Left": (0, offset, offset, pipe.SIZE),                  
        "Right": (offset + pipe.SIZE, offset, offset, pipe.SIZE)  
    }
        if pipe.previous_direction is not None:
            pygame.draw.rect(screen, (40, 40, 45), (drawX + Neighbours[pipe.previous_direction][0], drawY + Neighbours[pipe.previous_direction][1], Neighbours[pipe.previous_direction][2], Neighbours[pipe.previous_direction][3]))
        if pipe.next_direction is not None:
            pygame.draw.rect(screen, (40, 40, 45), (drawX + Neighbours[pipe.next_direction][0], drawY + Neighbours[pipe.next_direction][1], Neighbours[pipe.next_direction][2], Neighbours[pipe.next_direction][3]))
"""