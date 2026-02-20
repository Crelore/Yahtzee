import random
import pygame
from Yatzee import Yatzee   



pygame.init()

WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Yatzy")
timer = pygame.time.Clock()
fps = 60
background_color = (128, 128, 128)
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont(None, 36)

class Dice:
    def __init__(self, x, y, num, key):
        self.x = x
        self.y = y
        self.number = num
        self.key = key
        self.dice = ""
        self.held = False

    #draws the dice
    def draw(self):
        fill = (200, 200, 200) if self.held else white
        self.dice = pygame.draw.rect(screen, fill, [self.x, self.y, 100, 100], 0, 5)
        if self.held:
            pygame.draw.rect(screen, (0, 255, 0), [self.x, self.y, 100, 100], 4, 5)
        if self.number == 1:
            pygame.draw.circle(
                screen, black, (self.x + 50, self.y + 50), 10
            )
        if self.number == 2:
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 20), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 80), 10
            )
        if self.number == 3:
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 20), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 50, self.y + 50), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 80), 10
            )
        if self.number == 4:
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 20), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 80), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 80), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 20), 10
            )
        if self.number == 5:
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 20), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 80), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 50, self.y + 50), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 80), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 20), 10
            )
        if self.number == 6:
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 20), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 80), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 20, self.y + 50), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 80), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 50), 10
            )
            pygame.draw.circle(
                screen, black, (self.x + 80, self.y + 20), 10
            )


dice_positions = [10, 130, 250, 370, 490]
dice_list = [
    Dice(x, 50, random.randint(1, 6), i)
    for i, x in enumerate(dice_positions)
]

yatzee = Yatzee([])        
rolls_remaining = 3

running = True
while running:
    timer.tick(fps)
    screen.fill(background_color)

   
    if yatzee.is_complete():
        # once all boxes are filled, show completion message
        info = "Game complete! (R = Restart)"
    else:
       
        info = f"Rolls remaining: {rolls_remaining} (SPACE = Roll, R = Reset)"
      
    text_surf = font.render(info, True, white)
    screen.blit(text_surf, (10, 10))

    
    line_y = 40
    pygame.draw.line(screen, black, (0, line_y), (WIDTH, line_y), 2)
    line_y = 160
    pygame.draw.line(screen, black, (0, line_y), (WIDTH, line_y), 2)

    
    for dye in dice_list:
        dye.draw()

    score_rects = []
    y = 200
    for i, line in yatzee.get_lines():
        surf = font.render(line, True, white)
        rect = surf.get_rect(topleft=(10, y))
        screen.blit(surf, rect)
        score_rects.append((rect, i))
        y += 24

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            # toggle die hold if clicked
            for dye in dice_list:
                if dye.dice.collidepoint(mouse_pos):
                    dye.held = not dye.held
            # allow scoring clicks while game is still in progress
            if not yatzee.is_complete():
                for rect, i in score_rects:
                    if i is not None and rect.collidepoint(mouse_pos):
                        # don't score a category that's already filled
                        val = None
                        if i in yatzee.uppercategories:
                            val = yatzee.uppercategories[i][2]
                        elif i in yatzee.lowercategories:
                            val = yatzee.lowercategories[i][2]
                        if val is not None and val != "-":
                            break
                        # feed current dice values to model and record score
                        values = [d.number for d in dice_list]
                        yatzee.set_dice(values)
                        try:
                            yatzee.score_category(i)
                        except Exception as e:
                            print("scoring error:", e)
                        # reset state for next turn
                        rolls_remaining = 3
                        for d in dice_list:
                            d.held = False
                            d.number = random.randint(1, 6)
                        break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not yatzee.is_complete():
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
                yatzee = Yatzee([])

    pygame.display.flip()

pygame.quit()