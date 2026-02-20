import pygame


class DayNightCycleClass:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.dayLength = 30
        self.timer = 0
        self.borderX = SCREEN_WIDTH - 2*(SCREEN_WIDTH // 10)
        self.state = "day"
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.COLOR_DAY = (255, 191, 0) 
        self.COLOR_NIGHT = (40, 40, 150)
        self.nightOverlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.nightOverlay.fill((0, 0, 0, 0))
        self.nightTransparency = 0
        self.dayToNightBlending = False
        self.fadeStart = 7
        self.maxDarkness = 174

    def update(self, dividedTime):
        self.timer += dividedTime

        if self.timer >= self.dayLength:
            self.timer = 0
            self.state = "night" if self.state == "day" else "day"
        fade_start_time = self.dayLength - self.fadeStart 
        
        if self.state == "day":
            if self.timer > fade_start_time:
                fade_progress = (self.timer - fade_start_time) / self.fadeStart
                self.nightTransparency = int(fade_progress * self.maxDarkness)
            else:
                self.nightTransparency = 0
                
        elif self.state == "night":
            if self.timer > fade_start_time:
                fade_progress = (self.timer - fade_start_time) / self.fadeStart
                self.nightTransparency = int(self.maxDarkness - (fade_progress * self.maxDarkness))
            else:
                self.nightTransparency = self.maxDarkness

        self.nightOverlay.fill((0, 0, 0, self.nightTransparency))

            

    def draw(self, screen):
        screen.blit(self.nightOverlay, (0, 0))
        pygame.draw.rect(screen, (50, 50, 50), (self.borderX, 50, 220, 70))

        if self.state == "day":
            current_label = "DAY"
            bar_color = self.COLOR_DAY
        else:
            current_label = "NIGHT"
            bar_color = self.COLOR_NIGHT

        time_percent = self.timer / self.dayLength
        bar_width = int(200 * time_percent) 
        pygame.draw.rect(screen, bar_color, (self.borderX + 10, 60, bar_width, 50))

        text_surf = self.font.render(current_label, True, (255, 255, 255))
        screen.blit(text_surf, (self.borderX + 20, 70))
        