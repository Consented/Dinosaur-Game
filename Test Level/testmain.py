import pygame
from sys import exit

from pygame.locals import *


#   #   #Initialising
pygame.init()

WINDOW_SIZE = (1200,600)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
WINDOW = pygame.Surface((1600,800))

CLOCK = pygame.time.Clock()

pygame.display.set_caption("Level 1 Test")


#   #   #Variables
###Game
scroll = [0,0]
moving_right = False
moving_left = False
moving_up = False
moving_down = False
###Rects
l1rect1 = pygame.image.load("collision_rectangles/l1rect1.png")
l1rect1_rect =l1rect1.get_rect(topleft=(-300,340))
l1rect2 = pygame.image.load("collision_rectangles/l1rect2.png")
l1rect2_rect = l1rect2.get_rect(topleft=(505,340))
l1rect3_rect = l1rect1.get_rect(topleft=(505,940))







level_rects = [l1rect1_rect, l1rect2_rect, l1rect3_rect]

###Images
bg1Walk = pygame.image.load("Test Background Assets/_0003_walkable-ground-layer-1.png").convert_alpha() # loads the image from the corresponding file path
bg1Water = pygame.image.load("Test Background Assets/Test-Game_0004_water-layer-2.png").convert_alpha() # .convert_alpha() just gives x10 fps :D
bg1InsideGround = pygame.image.load("Test Background Assets/_0005_inside-ground-layer-3.png").convert_alpha()
bg2 = pygame.image.load("Test Background Assets/_0006_background-1-layer-4.png").convert_alpha()
bg3 = pygame.image.load("Test Background Assets/_0007_background-2-layer-5.png").convert_alpha()
bg4 = pygame.image.load("Test Background Assets/_0008_background-3-mountains-layer-6.png").convert_alpha()
bg5 = pygame.image.load("Test Background Assets/Test-Game_0009_clouds.png").convert_alpha()
bg6 = pygame.image.load("Test Background Assets/Test-Game_0010_background-color.png").convert_alpha()

###Player
player_img = pygame.image.load("playerplaceholder.png").convert_alpha()
player_rect = player_img.get_rect(center = (0,300)) #Draws rectangle around the player_img and places the centre of the rectangle at (0, 300)

debug = True

#FONT =  pygame.font.Font("data/fonts/Pixeltype.ttf", 50)


#   #   #Functions
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0] #Move on x-axis
    hit_list = collision_test(rect, tiles) #Find colliding tiles
    for tile in hit_list: # Loop for each colliding tile
        if movement[0] > 0: #If moving right
            rect.right = tile.left # Set right edge of rectangle to left edge of colliding tile
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1] # Move on y-axis
    hit_list = collision_test(rect, tiles) #Find colliding tiles
    for tile in hit_list: # Loop for each colliding tile
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types #return rect and collision dict

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def scrollfunc(scroll):
    scroll[0] += (player_rect.x - scroll[0]- 200) /20
    scroll[1] += (player_rect.y - scroll[1]- 100) /20
    return scroll

#   #   #Main loop
#Rect(0,340,550,20)




while True:
    for event in pygame.event.get():
        if event.type == QUIT:
           pygame.quit()
           exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                moving_up = True
            if event.key == K_DOWN:
                moving_down = True
            if event.key == K_b:
                debug = not debug
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_up = False
            if event.key == K_DOWN:
                moving_down = False

    player_movement = [0, 0] #Player movement is reset every frame and then adjusted depending on inputs
    if moving_right:
        player_movement[0] += 10
    if moving_left:
        player_movement[0] -= 10
    if moving_down:
        player_movement[1] += 10
    if moving_up:
        player_movement[1] -= 10


    player_rect, collisions = move(player_rect, player_movement, level_rects)




    scroll = scrollfunc(scroll)



    ###Level
    #Background
    WINDOW.fill((75,75,75))
    WINDOW.blit(bg6, (0-scroll[0],0-scroll[1]))
    WINDOW.blit(bg4, (0-scroll[0]*0.25,300-scroll[1]))
    WINDOW.blit(bg3, (0-scroll[0]*0.5,300-scroll[1]))
    WINDOW.blit(bg2, (0-scroll[0]*0.75,300-scroll[1]))
    WINDOW.blit(bg1InsideGround, (0-scroll[0],300-scroll[1]))
    WINDOW.blit(bg1Water, (0-scroll[0],300-scroll[1]))
    WINDOW.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    WINDOW.blit(bg1Walk, (0-scroll[0],300-scroll[1]))


    #Rectangles - For Debugging
    if debug:
        WINDOW.blit(l1rect1, (l1rect1_rect.x - scroll[0], l1rect1_rect.y - scroll[1]))
        WINDOW.blit(l1rect2, (l1rect2_rect.x - scroll[0], l1rect2_rect.y - scroll[1]))
        WINDOW.blit(l1rect1, (l1rect3_rect.x - scroll[0], l1rect3_rect.y - scroll[1]))







    #Everything is "blitted" onto a seperate surface and then scaled and displayed
    surface = pygame.transform.scale(WINDOW, WINDOW_SIZE)
    SCREEN.blit(surface, (0,0))
    print(player_rect.y)

    #print(CLOCK.get_fps())

    pygame.display.update()#Updates the game loop
    CLOCK.tick(60)#Sets max frames
