import pygame

pygame.init()
font = pygame.font.Font("assets/fonts/BoldPixels.otf",50)
class PlayerClass:
    def __init__(player, screenWidth, screenHeight):
        player.position = pygame.Vector2(screenWidth // 2, screenHeight // 2)
        player.SIZE = 40
        player.health = 100
        player.itemIndex = 8 
        player.font = pygame.font.SysFont("Arial", 30, bold=True)
        player.Items = []
        player.isSwinging = False
        player.swingStep = 0
        player.swingCooldown = 0

    def draw_held_tool(player,screen,objects,held):            
        if held is not None:
            toolImage = objects[held]
            toolImage = pygame.transform.scale(toolImage,(player.SIZE,player.SIZE))

            mousePos = pygame.Vector2(pygame.mouse.get_pos())
            direction = mousePos - player.position
            angle = direction.angle_to(pygame.Vector2(1, 0))
            toolRotated = pygame.transform.rotate(toolImage, angle - 90)
            
            orbitOffset = pygame.Vector2(60, 0).rotate(-angle)
            toolRect = toolRotated.get_rect(center=player.position + orbitOffset)

            if player.isSwinging:
                if player.swingStep <= 8:
                    angle += 10*player.swingStep
                    toolRotated = pygame.transform.rotate(toolImage, angle - 90)
                    orbitOffset = pygame.Vector2(60, 0).rotate(-angle)
                    toolRect = toolRotated.get_rect(center=player.position + orbitOffset)
                    player.swingStep += 1
                else:
                    angle += 20*(12-player.swingStep)
                    toolRotated = pygame.transform.rotate(toolImage, angle - 90)
                    orbitOffset = pygame.Vector2(60, 0).rotate(-angle)
                    toolRect = toolRotated.get_rect(center=player.position + orbitOffset)
                    player.swingStep += 1

            elif player.swingCooldown > 0:
                player.swingCooldown -= 1

            if player.swingStep == 12:
                player.isSwinging = False
                player.swingStep = 0
                player.swingCooldown = 10
            screen.blit(toolRotated,toolRect)

    def draw_player(player,screen):
        pygame.draw.rect(screen,"blue",[player.position.x-player.SIZE//2,player.position.y-player.SIZE//2,player.SIZE,player.SIZE])

    def draw_player_info(player,screen,heartImage,terrain):
        # Draw health
        pygame.draw.rect(screen,(50,50,50),(50,50,220,70))
        pygame.draw.rect(screen,(150,150,150),(60,60,200,50))
        pygame.draw.rect(screen,(230,50,40),(60,60,2*player.health,50))
        screen.blit(heartImage,(280,50))
        # Draw coordinates
        x = terrain.x // terrain.TILE_SIZE
        y = terrain.y // terrain.TILE_SIZE
        ajoutCoords = len(str(x) + str(y)) - 2 
        pygame.draw.rect(screen,(50,50,50),(50,150,200+ajoutCoords*25,70))
        pygame.draw.rect(screen,(150,150,150),(60,160,180+ajoutCoords*25,50))
        coordinatesText = font.render(f"X:{x} Y:{y}",True,(225,225,225))
        screen.blit(coordinatesText,(70,160))
        # Draw Mouse Coordinates (for UI making)
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        ajoutCoordsMouse = len(str(mouseX) + str(mouseY)) - 2
        pygame.draw.rect(screen,(50,50,50),(50,250,200+ajoutCoordsMouse*25,70))
        pygame.draw.rect(screen,(150,150,150),(60,260,180+ajoutCoordsMouse*25,50))
        coordinatesText = font.render(f"X:{mouseX} Y:{mouseY}",True,(225,225,225))
        screen.blit(coordinatesText,(70,260))


