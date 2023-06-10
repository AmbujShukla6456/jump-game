import pygame
from sys import exit
from random import randint

pygame.init()
screen=pygame.display.set_mode((800,400))
pygame.display.set_caption('Jumper')
clock=pygame.time.Clock()
game=0
score=0
start_time=0
gravity=0

jumpsound=pygame.mixer.Sound('audio/jump.mp3')
jumpsound.set_volume(0.5)

music=pygame.mixer.Sound('audio/music.wav')
music.set_volume(0.4)

text=pygame.font.Font('font/Pixeltype.ttf',50)
text1=pygame.font.Font('font/Pixeltype.ttf',50)

sky_surface=pygame.image.load('graphics/Sky.png').convert()
ground_surface=pygame.image.load('graphics/ground.png').convert()

def display_score():
    if game != 0:
        score=int(pygame.time.get_ticks()/1000)-start_time
    else:
        score=0
    score_surface=text.render(f'Score : {score}',0,'black')
    score_rect=score_surface.get_rect(center=(410,50))
    screen.blit(score_surface,score_rect)
    return score

def obstacle_move(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)

        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else : return []

def player_animation():
    global player_surf, player_index
     
    if player_rect.bottom <300:
        player_surf=player_jump
    else:
        player_index+=0.1
        if player_index >= len(player_walk): player_index=0
        player_surf=player_walk[int(player_index)]

play_surf=text1.render("PRESS X TO START",1,"BLACK")
play_rect=play_surf.get_rect(center=(400,300))

snail_frame1=pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2=pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_index=0
snail_frame=[snail_frame1,snail_frame2]
snail_surf=snail_frame[snail_index]

fly_frame1=pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame2=pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_index=0
fly_frame=[fly_frame1,fly_frame2]
fly_surf=fly_frame[fly_index]

player_walk1=pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2=pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_jump=pygame.image.load('graphics/player/jump.png').convert_alpha()
player_index=0
player_walk=[player_walk1,player_walk2]
player_surf=player_walk[player_index]
player_rect=player_surf.get_rect(midbottom=(40,300))

player_stand=pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect=player_stand.get_rect(center=(400,150))

pygame.display.set_icon(player_stand)

obstacle_timer=pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1200)

obstacle_rect_list=[]

snail_timer=pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,300)

fly_timer=pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer,200)

while 1:    
    y=(0,0)
    if game:
        music.play(loops=-1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player_rect.bottom == 300: 
                    gravity=-20
                    jumpsound.play()
            if event.key == pygame.K_x:
                game=1
                start_time=int(pygame.time.get_ticks()/1000)
        
        if event.type == obstacle_timer and game:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1100),300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900,1100),220)))
        
        if event.type == snail_timer and game:
            if snail_index==0: snail_index=1
            else: snail_index=0
            snail_surf=snail_frame[snail_index]
        if event.type == fly_timer and game:
            if fly_index==0: fly_index=1
            else: fly_index=0
            fly_surf=fly_frame[fly_index]
    
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))

    if game:
        display_score()

        gravity +=1
        player_rect.y += gravity
        if player_rect.bottom >= 300: player_rect.bottom=300
        player_animation()
        screen.blit(player_surf,player_rect)

        obstacle_rect_list=obstacle_move(obstacle_rect_list)

        for obstacle_rect in obstacle_rect_list:
            if player_rect.colliderect(obstacle_rect):
                game=0
                obstacle_rect.x=-900
    
    else:
        screen.fill((92,129,162))
        display_score()
        screen.blit(player_stand,player_stand_rect)
        screen.blit(play_surf,play_rect)
    
    pygame.display.update()
    clock.tick(60)