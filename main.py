import pygame


image_path = '/date/data/com.Artonkes.Artonkes/files/app/'
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618,359))
pygame.display.set_caption("Srty")
icon = pygame.image.load(image_path + "images/game.png")
pygame.display.set_icon(icon)

bg = pygame.image.load(image_path + "images/1670754026.png").convert()


aaa = pygame.image.load(image_path + 'images/player_left/left2.png').convert_alpha()
aaa_list_in_game = []


wal_left = [
    pygame.image.load(image_path + 'images/player_left/left.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_left/left2.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_left/left3.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_left/left4.png').convert_alpha()
]

wal_right = [
    pygame.image.load(image_path + 'images/player_rigth/rigth.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_rigth/right2.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_rigth/right3.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_rigth/right4.png').convert_alpha()
]


pac = 0
bg_x = 0
bg_sound = pygame.mixer.Sound(image_path + 'music/atak.mp3')
bg_sound.play()

player_run = 5
player_x = 150
player_y = 250

is_jump = False
jump_count = 8

bullets_type = 5
bullet = pygame.image.load(image_path + 'images/atata.png').convert()
bullets = []

label = pygame.font.Font(image_path + 'font/RobotoMono-Bold.ttf', 40)
lose_label = label.render('You deat', True, ('red'))
restart_label = label.render('Restart', True, ('white'))
restart_label_rect = restart_label.get_rect(topleft=(180,200))



gameplay = True

aaa_time = pygame.USEREVENT + 1
pygame.time.set_timer(aaa_time, 5000)

running = True
while running:

    screen.blit(bg, (bg_x,0))
    screen.blit(bg, (bg_x+618,0))

    if gameplay:
        player_rect = wal_left[0].get_rect(topleft=(player_x,player_y))
        if aaa_list_in_game:
            for (i, el) in enumerate (aaa_list_in_game):
                screen.blit(aaa, el)
                el.x -= 10

                if el.x < -10:
                    aaa_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 100:
            player_x -= player_run
        elif keys[pygame.K_RIGHT] and player_x < 500:
            player_x += player_run

        if keys[pygame.K_LEFT]:
            screen.blit(wal_left[pac], (player_x,player_y))
        else:
            screen.blit(wal_right[pac], (player_x,player_y))

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8 :
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if pac == 3:
            pac = 0
        else:
            pac += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0

        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 630:
                    bullets.pop(i)

                if aaa_list_in_game:
                    for (index, aaa_el) in enumerate(aaa_list_in_game):
                        if el.colliderect(aaa_el):
                            aaa_list_in_game.pop(index)
                            bullets.pop(i)
                            bg_sound.play()


    else:
        screen.fill('black')
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)
        bg_sound.play()

        mous = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mous) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            aaa_list_in_game.clear()
            bullets.clear()
            bullets_type = 5
            bg_sound.play()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == aaa_time:
            aaa_list_in_game.append(aaa.get_rect(topleft=(620,250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_UP and bullets_type > 0:
            bullets.append(bullet.get_rect(topleft=(player_x+10,player_y)))
            bullets_type -= 1
            bg_sound.play()

    clock.tick(15)