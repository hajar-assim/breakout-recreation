#December 16, 2019
#Final Project - Breakout

#IMPORTING LIBRARIES-----
import pygame
import sys
import time
import random

#INITIALIZING SCREEN SIZE-----
pygame.init()
screen_size = (597, 700)
screen = pygame.display.set_mode((screen_size),0)
pygame.display.set_caption("BREAKOUT")
pygame.mixer.pre_init(44100, 16, 2, 4096)

#retrieve screen measurements
screen_w = screen.get_width()
screen_h = screen.get_height()

#retrieve position of center of screen
center_x = int(screen_w/2)
center_y = int(screen_h/2)

#COLOURS-----
WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
PURPLE = (154, 136, 180)
MELLOW = (222,222,222)

#BACKGROUND-----
screen.fill(WHITE)
pygame.display.update()


#PICTURES-----
#background options
background1 = pygame.image.load("space_background5.png")
background2 = pygame.image.load("sky_background.png")
#block options - night
n_easy_block_image = pygame.image.load("n1b.png")
n_medium_block_image = pygame.image.load("n2b.png")
n_hard_block_image = pygame.image.load("n3b.png")
n_metal_block_image = pygame.image.load("n4b.png")
#block options - sky
s_easy_block_image = pygame.image.load("s1b.png")
s_medium_block_image = pygame.image.load("s2b.png")
s_hard_block_image = pygame.image.load("s3b.png")
s_metal_block_image = pygame.image.load("s4b.png")
#other options
s_paddle_image = pygame.image.load("sky_paddle.png")
s_long_paddle_image = pygame.image.load("long_sky_paddle.png")
n_paddle_image = pygame.image.load("night_paddle.png")
ball_image = pygame.image.load("ball.png")
power_up_image = pygame.image.load("powerupball.png")
#life options
life_monitor5 = pygame.image.load("bar5.png")
life_monitor4 = pygame.image.load("bar4.png")
life_monitor3 = pygame.image.load("bar3.png")
life_monitor2 = pygame.image.load("bar2.png")
life_monitor1 = pygame.image.load("bar1.png")
life_monitor0 = pygame.image.load("bar0.png")
#buttons
button1_image = pygame.image.load("manual.png")
button2_image = pygame.image.load("customize.png")
button3_image = pygame.image.load("start.png")

#SOUNDS-----
pygame.mixer.music.load("backgroundmusic.mp3")
pygame.mixer.music.play(-1, 0.0)
paddle_hit_sound = pygame.mixer.Sound("paddlehitsound.wav")
block_hit_sound = pygame.mixer.Sound("blockhitsound.wav")
game_over_sound = pygame.mixer.Sound("gameoversound.wav")
life_lost_sound = pygame.mixer.Sound("lifelostsound.wav")
power_up_e_sound = pygame.mixer.Sound("powerupsound.wav")
power_up_a_sound = pygame.mixer.Sound("poweruplife.wav")
power_up_s_sound = pygame.mixer.Sound("powerupslow.wav")
menu_change_sound = pygame.mixer.Sound("buttonpress.wav")
background_change_sound = pygame.mixer.Sound("backgroundchangesound.wav")



#current image selected
background_image = background1
paddle_image = n_paddle_image
easy_block_image = n_easy_block_image
medium_block_image = n_medium_block_image
hard_block_image = n_hard_block_image
metal_block_image = n_metal_block_image
life_monitor_list = [life_monitor5,life_monitor4,life_monitor3,life_monitor2,life_monitor1,life_monitor0]

#SPEED-----
clock = pygame.time.Clock()
FPS = 60 #set frames per second
speed = [4,4]
paddle_speed = 6
power_up_speed = 1.5

# -------------------------VARIABLES-------------------------
#paddle/powerup/ball speed
paddle_dx = 0
paddle_dy = 0
power_up_dx = 0
power_up_dy = 0
ball_dx = 0
ball_dy = 0

#life bar
life_bar = 0

#power_ups
power_up_var = 0

#random num list
pygame.display.update()
rand_list = range(12, 580)

#fonts/text
BIG_FONT = pygame.font.Font("myfont.ttf",70)
NORMAL_FONT = pygame.font.Font("myfont.ttf",30)

# -------------------------FUNCTIONS/CLASSES-------------------------
#repeated values for the blocks combined into class
class Object:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
blue_block = Object(5, 172, 40, 10)
purple_block = Object(5, 148, 40, 10)
pink_block = Object(5, 124, 40, 10)
metal_block = Object(5, 112, 40, 10)
life_monitor_fun = Object(420, 10, 160, 30)
paddle = Object(center_x, 600, 78, 13)
ball = Object(center_x, center_y, 12, 12)
button1 = Object(10,300,210,60)
button2 = Object(10,370,210,60)
button3 = Object(10,440,210,60)
##backbutton = Object()


#rects
paddle = pygame.Rect(paddle.x, paddle.y, paddle.w, paddle.h)
ball = pygame.Rect(ball.x, ball.y, ball.w, ball.h)
power_up_rect = pygame.Rect(ball.x, ball.y, ball.w, ball.h)
life_monitor_rect = pygame.Rect(life_monitor_fun.x, life_monitor_fun.y, life_monitor_fun.w, life_monitor_fun.h)
button1_rect = pygame.Rect(button1.x,button1.y,button1.w,button1.h)
button2_rect = pygame.Rect(button2.x,button2.y,button2.w,button2.h)
button3_rect = pygame.Rect(button3.x,button3.y,button3.w,button3.h)

# -------------------------ARRAYS-------------------------

#empty array to store rects for each block row of level
blue_blocks = []
purple_blocks = []
pink_blocks = []
metal_blocks = []

#layout of blocks for each level
#layout of blocks for each level
blue_block_array = [
"B B B B B B B B B B B B B B",
"B B B B B B B B B B B B B B",
]

purple_block_array = [
"P P P P P P P P P P P P P P",
"P P P P P P P P P P P P P P",
]

pink_block_array = [
"I I I I I I I I I I I I I I",
"I I I I I I I I I I I I I I",
]

metal_block_array = [
"M M M M M M M M M M M M M M",
]

# -------------------------CREATING BLOCK RECTS-------------------------

#read the array and create the appropriate Rects FOR EACH LEVEL, store them in the walls array
for row in blue_block_array: #easy/blue
    for col in row:
        if col == "B":
            blue_block_rect = pygame.Rect(blue_block.x, blue_block.y, blue_block.w, blue_block.h)
            blue_blocks.append(blue_block_rect)
        blue_block.x += 21
    blue_block.y += 12
    blue_block.x = 5 #distance from x (0)
    
for row in purple_block_array:
    for col in row:
        if col == "P":
            purple_block_rect = pygame.Rect(purple_block.x, purple_block.y, purple_block.w, purple_block.h)
            purple_blocks.append({"rect": purple_block_rect, "strength": 2})
        purple_block.x += 21
    purple_block.y += 12
    purple_block.x = 5

for row in pink_block_array:
    for col in row:
        if col == "I":
            pink_block_rect = pygame.Rect(pink_block.x, pink_block.y, pink_block.w, pink_block.h)
            pink_blocks.append({"rect": pink_block_rect, "strength": 3})
        pink_block.x += 21
    pink_block.y += 12
    pink_block.x = 5

for row in metal_block_array:
    for col in row:
        if col == "M":
            metal_block_rect = pygame.Rect(metal_block.x, metal_block.y, metal_block.w, metal_block.h)
            metal_blocks.append({"rect": metal_block_rect, "strength": 4})
        metal_block.x += 21
    metal_block.y += 12
    metal_block.x = 5


# -------------------------LOOPS-------------------------
main = True
intro_screen = True
game_screen = False
manual = False

initiate_power_up = False
draw_power_up = False
power_up_a = False
power_up_s = False
power_up_e = False

fill_bricks = False
remove_life = False

game_over_text = False

# ---------------------START---------------------
while main:
    while intro_screen:
        #erases gameover text
        game_over_text = False
        #makes title for BREAKOUT
        title_position = [[10,10]]
        title_lines = ["BREAKOUT"]
        game_intro_text_positions = [[10,200],[10,220],[10,240],[10,260],[button2.x + 215, button2.y + 10], [button2.x + 215, button2.y + 30],
                                     [button3.x + 215, button3.y + 15], [button1.x + 215, button1.y + 15]]
        game_intro_text_lines = ["Welcome to Breakout, a single-player",
                                 "game where the objective of the",
                                 "game is to pass the level by breaking",
                                 "all the bricks.", "- press [s/n] to", "choose sky/night mode.", "- press [p] to play", "- press [i] for manual"]

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                game = False
                main = False
                pygame.quit()
                sys.exit()
                
                #pressing start options
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu_change_sound.play()
                    fill_bricks = True
                    game_screen = True
                    intro_screen = False
                    draw_power_up = False
                    #sets ball to center when the game is started
                    ball.x = center_x
                    ball.y = center_y
                if event.key == pygame.K_n:
                    background_change_sound.play()
                    paddle_image = n_paddle_image
                    background_image = background1
                    easy_block_image = n_easy_block_image
                    medium_block_image = n_medium_block_image
                    hard_block_image = n_hard_block_image
                    metal_block_image = n_metal_block_image
                if event.key == pygame.K_s:
                    background_change_sound.play()
                    paddle_image = s_paddle_image
                    background_image = background2
                    easy_block_image = s_easy_block_image
                    medium_block_image = s_medium_block_image
                    hard_block_image = s_hard_block_image
                    metal_block_image = s_metal_block_image
                if event.key == pygame.K_i:
                    menu_change_sound.play()
                    intro_screen = False
                    manual = True

                    
##            elif event.type == pygame.MOUSEBUTTONDOWN:
##                #retrieve x & y pos of mouse click
##                mouse_x, mouse_y = event.pos
##
##                if button3_rect.collidepoint(mouse_x, mouse_y):
##                    start_screen = False
##                    game_screen = True
##            
        #constrain this loop to the specified FPS
        clock.tick(FPS)

        #removes screen trail
        screen.fill(MELLOW)

        #PADDLE EVENTS-----

        #store old paddle positions
        old_paddle_x = paddle.x
        old_paddle_y = paddle.y

        #moving the paddle rect
        paddle.move_ip(paddle_dx, paddle_dy)

        #automatic moving of paddle for start screen
        if ball.x < paddle.x:
            paddle_dx = -paddle_speed
        if ball.x > paddle.x:
            paddle_dx = paddle_speed

        #check to see if rect has left screen
        if paddle.left < 0 or paddle.right > screen_w:
            paddle.x = old_paddle_x

        #BALL EVENTS-----

        #moving ball
        ball = ball.move(speed)

        #collision bounce left & right
        if ball.left < 0 or ball.right > screen_w:
            speed[0] = -speed[0]

        #collision bounce top & bottom
        if ball.top < 0 or ball.bottom > screen_h:
            speed[1] = -speed[1]
        #collision of ball with paddle
        if paddle.colliderect(ball):
            speed[1] = -speed[1]

        #BLOCKS EVENTS-----
            
        #editing dictionaries according to collision
           
        for block in blue_blocks:
            if block.colliderect(ball):
                speed[1] = -speed[1]
                blue_blocks.remove(block)
                
        for block in purple_blocks:
            if block["rect"].colliderect(ball):
                speed[1] = -speed[1]
                block["strength"] -= 1
                if block["strength"] <= 0:
                    purple_blocks.remove(block)

        for block in pink_blocks:
            if block["rect"].colliderect(ball):
                speed[1] = -speed[1]
                block["strength"] -= 1
                if block["strength"] <= 0:
                    pink_blocks.remove(block)
                    
        for block in metal_blocks:
            if block["rect"].colliderect(ball):
                speed[1] = -speed[1]
                block["strength"] -= 1
                if block["strength"] <= 0:
                    metal_blocks.remove(block)
                

    # -------------------------START - BLIT/DRAWING-------------------------

        #drawing paddle/ball inside rect
        screen.blit(paddle_image, paddle)
        screen.blit(ball_image, ball)
        screen.blit(button1_image, button1_rect)
        screen.blit(button2_image, button2_rect)
        screen.blit(button3_image, button3_rect)
        
            
        #draws blocks and applies transparency as needed
        for block in blue_blocks:
            screen.blit(easy_block_image, block)

        for block in purple_blocks:
            alpha = 255 * block["strength"] // 2 #number will always remain under 255 until it is hit two times
            if alpha < 255: #if the number is below 255, it will add a white color on top to resemble transparency per hit
                transp_image = medium_block_image.copy().convert_alpha() #creates a new copy of the image to support per pixel alpha
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN) #using pygame.Surface.fill to fill the surface, but set the special blending flag ^ so that texture is calculated the minimum of the pixel color and (255, 255, 255, alpha)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(medium_block_image, block["rect"]) #once hit three times, block removed
                
        for block in pink_blocks:
            alpha = 255 * block["strength"] // 3
            if alpha < 255: 
                transp_image = hard_block_image.copy().convert_alpha() 
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(hard_block_image, block["rect"])
                
        for block in metal_blocks:
            alpha = 255 * block["strength"] // 4
            if alpha < 255: 
                transp_image = metal_block_image.copy().convert_alpha() 
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(metal_block_image, block["rect"])
            
        #draws instructions    
        for line, pos in zip(game_intro_text_lines, game_intro_text_positions):
            text = NORMAL_FONT.render(line, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.topleft = pos
            screen.blit(text, text_rect)
            
        #draws title    
        for line, pos in zip(title_lines, title_position):
            text = BIG_FONT.render(line, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.topleft = pos
            screen.blit(text, text_rect)

        #updating the screen
        pygame.display.update()

    # ---------------------MANUAL SCREEN---------------------
    while manual:
        ins_text_positions = [[10,10],[10,200],[10,225],[10,250],[10,275],[10,325],[10,350],[10,375],[10,400],[10,425],[10,450],[10,500]]
        ins_text_lines = ["WELCOME TO BREAKOUT.",
                          "This is single-player game where the",
                          "objective is to win by hitting the ",
                          "blocks with your paddle. You can control",
                          "your paddle using the left/right arrows.",
                          "There are also power ups, like these:     ",
                          "that are available. They come at random.",
                          "To use a power-up, you must catch it in the air.",
                          "You can only use one power-up at a time!",
                          "The available power-ups in this game are:",
                          "life addition, paddle growth, and time slow.",
                          "- press [b] to go back to menu."]

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                game = False
                manual = False
                main = False
                pygame.quit()
                sys.exit()
                
            #moving paddle with keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    menu_change_sound.play()
                    manual = False
                    intro_screen = True

        #constrain this loop to the specified FPS
        clock.tick(FPS)
            
        #removes screen trail
        screen.fill(MELLOW)
        #PADDLE EVENTS-----

        #store old paddle positions
        old_paddle_x = paddle.x
        old_paddle_y = paddle.y

        #moving the paddle rect
        paddle.move_ip(paddle_dx, paddle_dy)

        #automatic moving of paddle for start screen
        if ball.x < paddle.x:
            paddle_dx = -paddle_speed
        if ball.x > paddle.x:
            paddle_dx = paddle_speed

        #check to see if rect has left screen
        if paddle.left < 0 or paddle.right > screen_w:
            paddle.x = old_paddle_x

        #BALL EVENTS-----

        #moving ball
        ball = ball.move(speed)

        #collision bounce left & right
        if ball.left < 0 or ball.right > screen_w:
            speed[0] = -speed[0]

        #collision bounce top & bottom
        if ball.top < 0 or ball.bottom > screen_h:
            speed[1] = -speed[1]
        #collision of ball with paddle
        if paddle.colliderect(ball):
            speed[1] = -speed[1]

        #BLOCKS EVENTS-----
            
        #editing dictionaries according to collision
           
        for block in blue_blocks:
            if block.colliderect(ball):
                speed[1] = -speed[1]
                blue_blocks.remove(block)
                
        for block in purple_blocks:
            if block["rect"].colliderect(ball):
                speed[1] = -speed[1]
                block["strength"] -= 1
                if block["strength"] <= 0:
                    purple_blocks.remove(block)

        for block in pink_blocks:
            if block["rect"].colliderect(ball):
                speed[1] = -speed[1]
                block["strength"] -= 1
                if block["strength"] <= 0:
                    pink_blocks.remove(block)
                    
        for block in metal_blocks:
            if block["rect"].colliderect(ball):
                speed[1] = -speed[1]
                block["strength"] -= 1
                if block["strength"] <= 0:
                    metal_blocks.remove(block)
                

    # -------------------------START - BLIT/DRAWING-------------------------

        #drawing paddle/ball inside rect
        screen.blit(paddle_image, paddle)
        screen.blit(ball_image, ball)
        
            
        #draws blocks and applies transparency as needed
        for block in blue_blocks:
            screen.blit(easy_block_image, block)

        for block in purple_blocks:
            alpha = 255 * block["strength"] // 2 #number will always remain under 255 until it is hit two times
            if alpha < 255: #if the number is below 255, it will add a white color on top to resemble transparency per hit
                transp_image = medium_block_image.copy().convert_alpha() #creates a new copy of the image to support per pixel alpha
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN) #using pygame.Surface.fill to fill the surface, but set the special blending flag ^ so that texture is calculated the minimum of the pixel color and (255, 255, 255, alpha)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(medium_block_image, block["rect"]) #once hit three times, block removed
                
        for block in pink_blocks:
            alpha = 255 * block["strength"] // 3
            if alpha < 255: 
                transp_image = hard_block_image.copy().convert_alpha() 
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(hard_block_image, block["rect"])
                
        for block in metal_blocks:
            alpha = 255 * block["strength"] // 4
            if alpha < 255: 
                transp_image = metal_block_image.copy().convert_alpha() 
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(metal_block_image, block["rect"])
            
        #draws power up example
        power_up_rect.x = 490
        power_up_rect.y = 330
        draw_power_up = True
        
        #blit instructions
        for line, pos in zip(ins_text_lines, ins_text_positions):
            text = NORMAL_FONT.render(line, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.topleft = pos
            screen.blit(text, text_rect)
            
        if draw_power_up == True:
            screen.blit(power_up_image, power_up_rect)
            
        pygame.display.update()

                    
    # ---------------------GAME SCREEN---------------------
        #constrain this loop to the specified FPS
    while game_screen:
        pygame.mixer.music.set_volume(0.07) #sets background volume so you can hear the sound effects
        power_up_dy = power_up_speed
##        #set ball starting points
##        reset_ball = True
##        if reset_ball == True:            
##            ball_x = center_x - 50
##            ball_y = center_y - 50
##            reset_ball = False
        #text
        title_position = [[10,10]]
        title_lines = ["BREAKOUT"]
        gameover_position = [[center_x - 200, center_y], [center_x - 220, center_y + 60]]
        gameover_lines = ["GAME OVER!", "Play again? (y/n)"]
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                game = False
                main = False
                pygame.quit()
                sys.exit()
                
            #moving paddle with keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_dx = -paddle_speed
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = paddle_speed
                elif event.key == pygame.K_s:
                    ball_movement = True
                    #ball movement initiated when spacebar is pressed
                elif event.key == pygame.K_SPACE:
                    ball_dx = 4
                    ball_dy = 4
                    draw_power_up = False
                    power_up_a = False
                    power_up_s = False
                    power_up_e = False
                elif event.key == pygame.K_y:
                    menu_change_sound.play()
                    game_screen = False
                    intro_screen = True
                elif event.key == pygame.K_n:
                    menu_change_sound.play()
                    game = False
                    main = False
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.KEYUP:
            paddle_dx = 0

        #constrain this loop to the specified FPS
        clock.tick(FPS)

        #removes screen trail
        screen.fill(WHITE)
        screen.blit(background_image, [0, 0])

        #PADDLE EVENTS-----

        #store old paddle positions
        old_paddle_x = paddle.x
        old_paddle_y = paddle.y

        #moving the paddle rect
        paddle.move_ip(paddle_dx, paddle_dy)

        #check to see if rect has left screen
        if paddle.left < 0 or paddle.right > screen_w:
            paddle.x = old_paddle_x

        #BALL EVENTS-----

        #move the ball
        ball.move_ip(ball_dx, ball_dy)
        
        #collision bounce left & right
        if ball.left < 0 or ball.right > screen_w:
            ball_dx = -ball_dx

        #collision of ball with paddle
        if paddle.colliderect(ball):
            ball_dy = -ball_dy
            paddle_hit_sound.play()

        #collision with top
        if ball.top < 0:
            ball_dy = -ball_dy

        #collision with bottom - life removed
        if ball.bottom > screen_h + 20:
            life_lost_sound.play()
            remove_life = True
            #when ball hits bottom, remove life, reset ball to center, remove movement.
            if remove_life == True:
                life_bar += 1
                ball.x = center_x
                ball.y = center_y
                ball_dx = 0
                ball_dy = 0
                remove_life = False
                power_up_a = False
                power_up_s = False
                power_up_e = False
                draw_power_up = False

        if life_bar == 5:
            game_over_animation = True
            if game_over_animation == True:
                game_over_sound.play()
                ball.x = 1
                ball.y = 1
                game_over_text = True
                life_bar = 0
                game_over_animation = False
                

        #POWER UP EVENTS-----minjew
        # -------------------------POWER UPS-------------------------
        #chooses random power up from list
        rand_int = random.choice(rand_list)
        
        #power up 'e' - expands the paddle
        if power_up_e == True:
            paddle_image = s_long_paddle_image
            paddle.w = 120
            power_up_s = False
            power_up_a = False
        else:
            paddle_image = s_paddle_image
            paddle.w = 78

        #power up 's' - slows down the speed of the ball
        if power_up_s == True:
            FPS = 45
            power_up_e = False
            power_up_a = False
            paddle_image = s_paddle_image
        else:
            FPS = 60


        #power up 'a' - adds an extra life
        if power_up_a == True:
            if life_bar != 0:
                life_bar = life_bar - 1
            paddle_image = s_paddle_image
            power_up_a = False
            power_up_s = False
            power_up_e = False
            
        #moving the power up rect
        power_up_rect.move_ip(power_up_dx, power_up_dy)
        
        #activate power up if collision is 10x
        if power_up_var > 9:
            #chooses random coordinates to place power up
            initiate_power_up = True
            power_up_var = 0
            
        if initiate_power_up == True:
            power_up_rect.x = rand_int
            power_up_rect.y = 50
            draw_power_up = True
            initiate_power_up = False

        #activate power_up if it's caught
        if paddle.contains(power_up_rect):
            power_up_rect.x = 10
            power_up_rect.y = 10
            draw_power_up = False #erases power up when caught
            power_up_list = [1,2,3] #power up list
            power_up_num = random.choice(power_up_list) #chooses random power up
            print(power_up_num)
            if power_up_num == 1: #activates
                power_up_e = False
                power_up_s = False
                power_up_a = True
                power_up_a_sound.play()
            if power_up_num == 2:
                power_up_e = False
                power_up_a = False
                power_up_s = True
                power_up_s_sound.play()
            if power_up_num == 3:
                power_up_s = False
                power_up_a = False
                power_up_e = True
                power_up_a_sound.play()
            power_up_num = None


        #BLOCKS EVENTS-----
            
        #editing dictionaries according to collision
           
        for block in blue_blocks:
            if block.colliderect(ball):
                ball_dy = -ball_dy
                blue_blocks.remove(block)
                power_up_var += 1
                print(power_up_var)
                block_hit_sound.play()
                
        for block in purple_blocks:
            if block["rect"].colliderect(ball):
                ball_dy = -ball_dy
                power_up_var += 1
                print(power_up_var)
                block_hit_sound.play()
                block["strength"] -= 1
                if block["strength"] <= 0:
                    purple_blocks.remove(block)

        for block in pink_blocks:
            if block["rect"].colliderect(ball):
                ball_dy = -ball_dy
                power_up_var += 1
                print(power_up_var)
                block_hit_sound.play()
                block["strength"] -= 1
                if block["strength"] <= 0:
                    pink_blocks.remove(block)
                    
        for block in metal_blocks:
            if block["rect"].colliderect(ball):
                ball_dy = -ball_dy
                power_up_var += 1
                print(power_up_var)
                block_hit_sound.play()
                block["strength"] -= 1
                if block["strength"] <= 0:
                    metal_blocks.remove(block)

    # -------------------------CREATING BLOCK RECTS-------------------------

        if fill_bricks == True:
            #read the array and create the appropriate Rects FOR EACH LEVEL, store them in the walls array
            for row in blue_block_array: #easy/blue
                for col in row:
                    if col == "B":
                        blue_block_rect = pygame.Rect(blue_block.x, blue_block.y, blue_block.w, blue_block.h)
                        blue_blocks.append(blue_block_rect)
                    blue_block.x += 21
                blue_block.y += 12
                blue_block.x = 5 #distance from x (0)
                
            for row in purple_block_array:
                for col in row:
                    if col == "P":
                        purple_block_rect = pygame.Rect(purple_block.x, purple_block.y, purple_block.w, purple_block.h)
                        purple_blocks.append({"rect": purple_block_rect, "strength": 2})
                    purple_block.x += 21
                purple_block.y += 12
                purple_block.x = 5

            for row in pink_block_array:
                for col in row:
                    if col == "I":
                        pink_block_rect = pygame.Rect(pink_block.x, pink_block.y, pink_block.w, pink_block.h)
                        pink_blocks.append({"rect": pink_block_rect, "strength": 3})
                    pink_block.x += 21
                pink_block.y += 12
                pink_block.x = 5

            for row in metal_block_array:
                for col in row:
                    if col == "M":
                        metal_block_rect = pygame.Rect(metal_block.x, metal_block.y, metal_block.w, metal_block.h)
                        metal_blocks.append({"rect": metal_block_rect, "strength": 4})
                    metal_block.x += 21
                metal_block.y += 12
                metal_block.x = 5
            fill_bricks = False

    # -------------------------BLIT/DRAWING-------------------------

        #drawing all rects
        #gameover text
        if game_over_text == True:
            for line, pos in zip(gameover_lines, gameover_position):
                    text = BIG_FONT.render(line, True, (0, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.topleft = pos
                    screen.blit(text, text_rect)
                
        screen.blit(ball_image, ball)
        screen.blit(life_monitor_list[life_bar], life_monitor_rect)
        if draw_power_up == True:
            screen.blit(power_up_image, power_up_rect)
        screen.blit(paddle_image, paddle)
            
        #draws blocks and applies transparency as needed
        for block in blue_blocks:
            screen.blit(easy_block_image, block)

        for block in purple_blocks:
            alpha = 255 * block["strength"] // 2 #number will always remain under 255 until it is hit two times
            if alpha < 255: #if the number is below 255, it will add a white color on top to resemble transparency per hit
                transp_image = medium_block_image.copy().convert_alpha() #creates a new copy of the image to support per pixel alpha
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN) #using pygame.Surface.fill to fill the surface, but set the special blending flag ^ so that texture is calculated the minimum of the pixel color and (255, 255, 255, alpha)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(medium_block_image, block["rect"]) #once hit three times, block removed
                
        for block in pink_blocks:
            alpha = 255 * block["strength"] // 3
            if alpha < 255: 
                transp_image = hard_block_image.copy().convert_alpha() 
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(hard_block_image, block["rect"])
                
        for block in metal_blocks:
            alpha = 255 * block["strength"] // 4
            if alpha < 255: 
                transp_image = metal_block_image.copy().convert_alpha() 
                transp_image.fill((255, 255, 255, alpha), special_flags = pygame.BLEND_RGBA_MIN)
                screen.blit(transp_image, block["rect"])
            else:
                screen.blit(metal_block_image, block["rect"])
            
        #draws title
        for line, pos in zip(title_lines, title_position):
            text = BIG_FONT.render(line, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.topleft = pos
            screen.blit(text, text_rect)

        #updating the screen
        pygame.display.update()

pygame.quit()
sys.exit()

# -------------------------CREDITS-------------------------
# transparency not done by me solely, got help from friend
#background - https://www.wallpaperflare.com/dragon-flying-above-sky-artwork-wallpaper-181535
#sounds = https://themushroomkingdom.net/media/smw/wav
#block/paddle/ball/powerup pictures were created on pixilart.com by myself
