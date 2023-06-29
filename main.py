import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite): #inherits from another class
    def __init__(self):
        super().__init__() #we're initializing the sprite class right inside of this class as well so we can access it
        #two attributes at the very minimum: self.image and self.rect
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0 #we will use to pick either player_walk_1 surface or player_walk_2 surface
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index] #surface that will be displayed by default, direct is where it's going to go
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.25) #value 0-1, 1 being full sound

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type): #type is fly or snail
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/enemies/fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/enemies/fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/enemies/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/enemies/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill() #destroys this obstacle sprite


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time  #gives time in milliseconds
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64)) #current_time is an integer, but the function .render() wants a string
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list: #if python finds an empty list, it will consider this false
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
            # screen.blit(snail_surface, obstacle_rect) #we are moving the rectangle, and drawing the surface in the same position

        #LIST COMPREHENSION
        #get obstacle list, assign it a new list already, checks all of the rectangles then sees if it is too far to the left
        #only covers the existing list, we only want to copy an item if obstacle x is greater than a certain position
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
                #local scope: game_active is in the global scope, local to global scope --> return statement
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): #3 arguments: sprite, group, boolean
        obstacle_group.empty()
        return False
    else:
        return True
    #if set to true, if snail collides with player, snail deleted, if false snail will NOT be deleted
    #returns a list, if it doesn't collect anything, returns empty list
    


def player_animation():
    global player_surface, player_index
    #play walking animation if the player is on floor
    #display the jump surface when player is not on floor
    if player_rect.bottom < 300:
        #jump
        player_surface = player_jump
    else:
        #walk
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        #list with 2 walk surfaces [w1,w2]; by default, w1 is index 0, increase walk index by very small increments so its not too fast
        player_surface = player_walk[int(player_index)] #after we get past 1, we want to go back to 0


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
#create font using pygame.font.Font(font type, font size) - 2 arguments, can be placed anywhere
test_font = pygame.font.Font('fonts/Pixeltype.ttf', 50) #None is the default font
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.10)
bg_music.play(loops = -1) #telling pygame to play this sound forever and restart if it ends


#Groups
player = pygame.sprite.GroupSingle()
player.add(Player()) #add an instance of our player into our group

obstacle_group = pygame.sprite.Group()

# testing adding surfaces to display surface
# test_surface = pygame.Surface((100,200))
# test_surface.fill('red')

#testing adding images to display surface
#any time you import an image to PyGame, it will be on a SEPARATE NEW SURFACE
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

#Any time you want to create text, you must create an image of the text, then place that on the display surface
# score_surface = test_font.render('My Game', False, (64,64,64)) #rgb tuple for 64, 64, 64
# score_rect = score_surface.get_rect(center = (400, 50))
#requires 3 arguments ('text you want to display', Anti-Alias (smooths the edges of the text, but because we're in pixelart, set to False), color)

#OBSTACLES
#SNAIL
snail_frame_1 = pygame.image.load('graphics/enemies/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/enemies/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index] #default snail

#FLY
fly_frame_1 = pygame.image.load('graphics/enemies/fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/enemies/fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

#PLAYER
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 #we will use to pick either player_walk_1 surface or player_walk_2 surface
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))

#GRAVITY AND JUMP MECHANICS
player_gravity = 0

#INTRO SCREEN
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render(f'Pix Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,50))

game_message = test_font.render(f'Press space to start', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 340))
game_message_rect_score = game_message.get_rect(center = (400, 370))

#TIMER
obstacle_timer = pygame.USEREVENT + 1 #always + 1 because there are some events that are reserved for pygame itself, so avoid conflicts
pygame.time.set_timer(obstacle_timer, 1500) #2 arguments, the event we want to trigger, and how often we want to trigger it in milliseconds

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos)  and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail']))) #this choice method will choose one of these 4 items, percentage 75% chance to get snail, 25% chance to get fly
                # if randint(0,2): #returns either 0 or 1, 0 for False, 1 for True
                #     obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100), 300)))
                # else: 
                #     obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100), 210)))
                #randint from random module gets a random integer from two numbers and we can use that to give variety to our spawn location
                #creates our list, but we need the list to move
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        #OUR GAME
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        #pygame.draw is the module, .rect() is the shape you want it to draw
        # pygame.draw.rect(screen, '#c0e8ec', score_rect) #needs 3 arguments (surface to draw on, color, rectangle we want to draw, width(optional), border-radius(optional))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) #to fill the center, we can just draw another rectangle without the width
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # snail_x_pos -= 3
        # if snail_x_pos < -100:
        #     snail_x_pos = 800 --> no longer need this as we switched to moving the surface with rectangles
        # snail_rect.x -= 5
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)
        # print(player_rect.left) prints out the left side position of the rectangle in the console
        # player_rect.left += 1 ; moves the rectangle that contains the surface

        #PLAYER CODE
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surface, player_rect)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #OBSTACLE MOVEMENT
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        #runs the function, takes obstacle rect list, a bit further to the left, then we take this new list, to overwrite the list

        #COLLISIONS
        game_active = collision_sprite()
        #this collisions returns True or False, if our player_rect has a collision with obstacle, returns False, and therefore makes
        #game_active False, going to else statement

    #START SCREEN
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear() #removes all items inside rect list so enemies respawn further away again
        player_rect.midbottom = (80,300) #resets player to the bottom again
        player_gravity = 0 #resets gravity so it doesnt fall through
        screen.blit(game_name, game_name_rect)
        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(game_message, game_message_rect_score)




    pygame.display.update() #anything we do inside this while loop, it will update the display
    clock.tick(60) #setting max amount of loops to 60 times a second
