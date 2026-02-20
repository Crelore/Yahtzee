import random

import pygame

pygame.init()

WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Yatzy")
timer = pygame.time.Clock()
fps = 60
background_color = (128,128, 128)
white = (255, 255, 255)
black = (0, 0 ,0)


font = pygame.font.SysFont(None, 36)

class Dice:
    def __init__(self, x, y, num, key):
        self.x = x
        self.y = y
        self.number = num
        self.key = key
        self.dice = ""            
        self.held = False          
    
    def draw(self):
        
        fill = (200, 200, 200) if self.held else white
        
        self.dice = pygame.draw.rect(screen, fill, [self.x, self.y, 100, 100], 0 ,5)
        
        if self.held:
            pygame.draw.rect(screen, (0, 255, 0), [self.x, self.y, 100, 100], 4, 5)

        
        if self.number == 1 :
            pygame.draw.circle(screen, black, (self.x + 50, self.y + 50), 10)
        if self.number == 2:
            pygame.draw.circle(screen, black, (self.x + 20, self.y + 20), 10)
            pygame.draw.circle(screen, black, (self.x + 80, self.y + 80), 10)
        if self.number == 3:
            pygame.draw.circle(screen, black, (self.x + 20, self.y + 20), 10)
            pygame.draw.circle(screen, black, (self.x + 50, self.y + 50), 10)
            pygame.draw.circle(screen, black, (self.x + 80, self.y + 80), 10)
        if self.number == 4:
            pygame.draw.circle(screen, black, (self.x +20, self.y + 20), 10)
            pygame.draw.circle(screen, black, (self.x +20, self.y + 80), 10)
            pygame.draw.circle(screen, black, (self.x +80, self.y + 80), 10)
            pygame.draw.circle(screen, black, (self.x +80, self.y + 20), 10)
        if self.number == 5:
            pygame.draw.circle(screen, black, (self.x + 20, self.y + 20), 10)
            pygame.draw.circle(screen, black, (self.x + 20, self.y + 80), 10)
            pygame.draw.circle(screen, black, (self.x + 50, self.y + 50), 10)
            pygame.draw.circle(screen, black, (self.x + 80, self.y + 80), 10)
            pygame.draw.circle(screen, black, (self.x + 80, self.y + 20), 10)
        if self.number == 6:
            pygame.draw.circle(screen, black, (self.x + 20, self.y + 20), 10)
            pygame.draw.circle(screen, black, (self.x + 20, self.y + 80), 10)
            pygame.draw.circle(screen, black, (self.x + 20, self.y + 50), 10)
            pygame.draw.circle(screen, black, (self.x + 80, self.y + 80), 10)
            pygame.draw.circle(screen, black, (self.x + 80, self.y + 50), 10)
            pygame.draw.circle(screen, black, (self.x + 80, self.y + 20), 10)




dice_positions = [10, 130, 250, 370, 490]
dice_list = [Dice(x, 50, random.randint(1, 6), i) for i, x in enumerate(dice_positions)]


rolls_remaining = 3  



running = True
while running:
    timer.tick(fps)
    screen.fill(background_color)

    
    info = f"Rolls remaining: {rolls_remaining} (SPACE = Roll, R = Reset)"
    text_surf = font.render(info, True, white)
    screen.blit(text_surf, (10, 10))

    line_y = 40
    pygame.draw.line(screen, black, (0, line_y), (WIDTH, line_y), 2)

    line_y = 160
    pygame.draw.line(screen, black, (0, line_y), (WIDTH, line_y), 2)
  
    for dye in dice_list:
        dye.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            mouse_pos = event.pos
            for dye in dice_list:
                if dye.dice.collidepoint(mouse_pos):
                    dye.held = not dye.held
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                
                if rolls_remaining > 0:
                    for dye in dice_list:
                        if not dye.held:
                            dye.number = random.randint(1, 6)
                    rolls_remaining -= 1
            elif event.key == pygame.K_r:
                
                rolls_remaining = 3
                for dye in dice_list:
                    dye.held = False
                    dye.number = random.randint(1, 6)

    pygame.display.flip()
pygame.quit()