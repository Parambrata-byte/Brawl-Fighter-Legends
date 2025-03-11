import pygame
from fighter import Fighter
import sys

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72,56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]
clock = pygame.time.Clock()  # To control FPS

score = [0,0]
round_over = False
round_over_cd = 5000
intro_count = 4
last_count_tick = pygame.time.get_ticks()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawl Fighter Legends")

background = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

Warrior_sheet = pygame.image.load("./assets/images/warrior/Sprites/warrior.png").convert_alpha()
Wizard_sheet = pygame.image.load("./assets/images/wizard/Sprites/wizard.png").convert_alpha()

Warrior_animation_steps = [10,8,1,7,7,3,7]
Wizard_animation_steps = [8,8,1,8,8,3,7]

victory_img = pygame.image.load("./assets/images/icons/victory.png")

count_font = pygame.font.Font("./assets/fonts/turok.ttf",80)
score_font = pygame.font.Font("./assets/fonts/turok.ttf",40)

def draw_bg():
    scaled_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

def draw_health(health,x,y):
    ratio = health / 100
    pygame.draw.rect(screen,"White",(x-5,y-5,410,40))
    pygame.draw.rect(screen,"Red",(x,y,400,30))
    pygame.draw.rect(screen,"Yellow",(x,y,400*ratio,30))

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

# fighter instance
fighter_1 = Fighter(1,200,310,WARRIOR_DATA,Warrior_sheet,Warrior_animation_steps,False)
fighter_2 = Fighter(2,700,310,WIZARD_DATA,Wizard_sheet,Wizard_animation_steps,True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Fixed the variable name

    draw_bg()

    draw_health(fighter_1.health,20,20)
    draw_health(fighter_2.health,580,20)

    draw_text(f'{str(score[0])}-{str(score[1])}',score_font,(255,255,255),480,20)

    if intro_count <= 0:
        fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_2)
        fighter_2.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_1)
    else:
        draw_text(str(intro_count),count_font,(255,0,0),SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        if(pygame.time.get_ticks() - last_count_tick) >= 1000:
            intro_count -= 1
            last_count_tick = pygame.time.get_ticks()


    fighter_1.update()
    fighter_2.update()

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        if fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img,(360,150))
        if pygame.time.get_ticks() - round_over_time >= round_over_cd:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1,200,310,WARRIOR_DATA,Warrior_sheet,Warrior_animation_steps,False)
            fighter_2 = Fighter(2,700,310,WIZARD_DATA,Wizard_sheet,Wizard_animation_steps,True)


    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()