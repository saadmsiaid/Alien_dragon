import pygame, sys, random, button
from pygame.math import Vector2
from moviepy.editor import VideoFileClip
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.head_up = pygame.image.load('res/Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('res/Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('res/Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('res/Graphics/head_left.png').convert_alpha()
        self.tail_up = pygame.image.load('res/Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('res/Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('res/Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('res/Graphics/tail_left.png').convert_alpha()
        self.body_vertical = pygame.image.load('res/Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('res/Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('res/Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('res/Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('res/Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('res/Graphics/body_bl.png').convert_alpha()
        self.bg_sound=pygame.mixer.Sound('res/sound/evil-cue-111895.mp3')
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    def add_block(self):
        self.new_block = True
    def play_bg_sound(self):
        self.bg_sound.play()
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
class ALIEN:
    def __init__(self):
        self.randomize()
    def draw_alien(self):
        alien_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(alien, alien_rect)
    def randomize(self):
        self.x = random.randint(0, cell_width - 1)
        self.y = random.randint(0, cell_height - 1)
        self.pos = Vector2(self.x, self.y)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.alien = ALIEN()
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    def draw_elements(self):
        self.alien.draw_alien()
        self.snake.draw_snake()
        self.draw_score()
    def check_collision(self):
        if self.alien.pos == self.snake.body[0]:
            self.alien.randomize()
            self.snake.add_block()
        for block in self.snake.body[1:]:
            if block == self.alien.pos:
                self.alien.randomize()
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_width or not 0 <= self.snake.body[0].y < cell_height:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    def game_over(self):
        self.snake.reset()
    def draw_score(self):
        global memo
        score_text = str(len(self.snake.body) - 3)
        memo=len(self.snake.body) - 3
        score_surface = game_font.render(score_text, True, (250,50, 50))
        score_x = int(100)
        score_y = int(30)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        alien_rect = alien.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(alien_rect.left, alien_rect.top, alien_rect.width + score_rect.width + 2,alien_rect.height)
        pygame.draw.rect(screen, (0,0,0), bg_rect,2)
        screen.blit(score_surface, score_rect)
        screen.blit(alien, alien_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 3)
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
muet=True
cell_size = 50
cell_width=25
cell_height=14
screen = pygame.display.set_mode((1366,768))
clock = pygame.time.Clock()
alien = pygame.image.load('res/Graphics/alien.png').convert_alpha()
game_font = pygame.font.Font('res/Font/who asks satan.ttf', 60)
BackGround = Background('res/media/bg.jpg')
menu_state = "main"
resume_img = pygame.image.load("res/Graphics/button_resume.png").convert_alpha()
options_img = pygame.image.load("res/Graphics/button_options.png").convert_alpha()
quit_img = pygame.image.load("res/Graphics/button_quit.png").convert_alpha()
easy_img = pygame.image.load('res/Graphics/easy.png').convert_alpha()
medium_img = pygame.image.load('res/Graphics/medium.png').convert_alpha()
hard_img = pygame.image.load('res/Graphics/hard.png').convert_alpha()
back_img = pygame.image.load('res/Graphics/button_back.png').convert_alpha()
muet_img = pygame.image.load('res/Graphics/button_muet.png')
muet_button = button.Button(700,475,muet_img,1)
resume_button = button.Button(550, 150, resume_img, 1)
options_button = button.Button(540, 275, options_img, 1)
quit_button = button.Button(580, 400, quit_img, 1)
easy_button = button.Button(550, 100, easy_img, 1)
medium_button = button.Button(560, 225, medium_img, 1)
hard_button = button.Button(550, 350, hard_img, 1)
back_button = button.Button(600, 500, back_img, 1)
memo=0
topmemo=0
SCREEN_UPDATE = pygame.USEREVENT
play_speed=150
pygame.time.set_timer(SCREEN_UPDATE, play_speed)
video = VideoFileClip("res/media/final.mp4")
video.preview(fullscreen=True)
main_game = MAIN()
game_paused=False
run = True
start=True
def mode(niv):
    if niv==1:
        play_speed=200
    elif niv==2:
        play_speed=125
    elif niv==3:
        play_speed=70
    pygame.time.set_timer(SCREEN_UPDATE, play_speed)
while True:
    while start:
        if memo >= topmemo:
            topmemo = memo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 00)
                if event.key == pygame.K_SPACE:
                    game_paused = True
                    start=False
                    run=True
        screen.blit(BackGround.image, BackGround.rect)
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)
    while run:
        screen.blit(BackGround.image, BackGround.rect)
        if game_paused == True:
            if menu_state == "main":
                text = game_font.render("YOUR BEST KIILS SCORE   "+str(topmemo),1, True, (255,50,20))
                screen.blit(text, (400, 30))
                if resume_button.draw(screen):
                    game_paused = False
                    run = False
                    start = True
                if options_button.draw(screen):
                    menu_state = "options"
                if quit_button.draw(screen):
                    pygame.quit()
                    sys.exit()
            if menu_state == "options":
                if easy_button.draw(screen):
                    mode(1)
                    menu_state = "main"
                if muet_button.draw(screen):
                    muet=False
                    menu_state = "main"
                if medium_button.draw(screen):
                    mode(2)
                    menu_state = "main"
                if hard_button.draw(screen):
                    mode(3)
                    menu_state = "main"
                if back_button.draw(screen):
                    menu_state = "main"
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = False
                    run = False
                    start = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()