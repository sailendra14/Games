import pygame
import random
import os

pygame.mixer.init()

pygame.init()

#Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
rc = (10, 200, 200)
gm_color = (230, 200, 230)
gp_color = (9, 200, 40)

#Creating Windows
screen_width = 700
screen_Height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_Height))

#Background image
# bgimg = pygame.image.load("")
# bgimg = pygame.transform.scale(bgimg, (screen_width, screen_Height)).convert_alpha()

#Game Title
pygame.display.set_caption("Snake - Searching For Food")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, black, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(rc)
        text_screen("Welcome to Snakes", black, 200, 250)
        text_screen("Press Space Bar To Play", black, 170, 280)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60) # fps = 60

# Game loop
def gameloop():
    # Game Specific Variables
    exit_game = False
    game_over = False
    snake_x = 30
    snake_y = 40
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_Height / 2)
    score = 0

    init_velocity = 5
    velocity_x = 0
    velocity_y = 0

    snk_list = []
    snk_length = 1
    snake_size = 15
    fps = 20

    # Check if highscore file is exists of not?
    if(not os.path.exists("hs.txt")):
        with open("hs.txt", "w")as f:
            f.write("0")

    with open("hs.txt", 'r') as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("hs.txt", 'w') as f:
                f.write(str(highscore))
            gameWindow.fill(gm_color) #game over color
            text_screen("Game Over! Press Enter to Continue", red, 40, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:  # number represents sensitivity
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_Height / 2)
                snk_length += 5
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(gp_color) #game play color
            # gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "   Highscore: " + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[: -1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_Height:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, red, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()