import pygame

class BuildingsClass:
    def __init__(self):
        self.hotbar = ["Pipe", "Miner", "Mixer", "Splitter", " Signal", "Wire", "Filter", "Tunnel", "Logic"]
        self.selectedSlot = None
        self.SLOT_SIZE = 100
        self.font = pygame.font.SysFont("Consolas", 14, bold=True)
        self.currentInteractionMode = "Moving" # Or "Building"

    def handle_event(self, event, mousePosition, screen):
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:
                index = event.key - pygame.K_1
                if index < len(self.hotbar):
                    self.currentInteractionMode = "Building"
                    if index == self.selectedSlot:
                        self.currentInteractionMode = "Moving"
                        self.selectedSlot = None
                    else:
                        self.selectedSlot = index
        elif event.type == pygame.MOUSEBUTTONDOWN:
            startHotbarX = (screen.get_width() // 2) - (9 * self.SLOT_SIZE // 2)
            endHotbarX = (screen.get_width() // 2) + (9 * self.SLOT_SIZE // 2)
            startHotbarY = screen.get_height() - self.SLOT_SIZE - 30
            endHotbarY = screen.get_height() - 30
            if startHotbarX <= mousePosition[0] <= endHotbarX and startHotbarY <= mousePosition[1] <= endHotbarY:
                self.selectedSlot = (mousePosition[0] - startHotbarX)//self.SLOT_SIZE
                self.currentInteractionMode = "Building"
                

    def draw_building_bar(self, screen):

        totalWidth = len(self.hotbar) * self.SLOT_SIZE
        startX = (screen.get_width() // 2) - (totalWidth // 2)
        y = screen.get_height() - self.SLOT_SIZE - 30

        backgroundPadding = 10
        backgroundRect = pygame.Rect(startX - backgroundPadding, y - backgroundPadding,
                                     totalWidth + (backgroundPadding * 2), self.SLOT_SIZE + backgroundPadding + 40)
        leftTriangle = [(backgroundRect.left - 40, screen.get_height()), 
                     (backgroundRect.left, backgroundRect.top), 
                     (backgroundRect.left, screen.get_height())]
        
        rightTriangle = [(backgroundRect.right + 40, screen.get_height()), 
                      (backgroundRect.right, backgroundRect.top), 
                      (backgroundRect.right, screen.get_height())]


        pygame.draw.polygon(screen, (40, 44, 52), leftTriangle)
        pygame.draw.rect(screen, (40, 44, 52), backgroundRect)
        pygame.draw.polygon(screen, (40, 44, 52), rightTriangle)


        for i, item in enumerate(self.hotbar):
            x = startX + i * self.SLOT_SIZE

            if self.currentInteractionMode == "Building":
                isSelected = (i == self.selectedSlot)
            else:
                isSelected = False
            backgroundColor = (40, 44, 52) if not isSelected else (60, 70, 90)

            # Draw Slot
            pygame.draw.rect(screen, backgroundColor, (x, y, self.SLOT_SIZE, self.SLOT_SIZE))
            text = self.font.render(item, True, (200, 200, 210))
            textRect = text.get_rect(midbottom=(x + self.SLOT_SIZE//2, y + self.SLOT_SIZE - 5))
            screen.blit(text, textRect)
            numberText = self.font.render(str(i+1), True, (100, 110, 120))
            screen.blit(numberText, (x + 5, y + 5))

