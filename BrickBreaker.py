import pygame
import random

pygame.init()

timer= pygame.time.Clock()
fps=60
White= (255,255,255)
Grey= (128,128,128)
Black= (0,0,0)
red= (255,0,0)
green= (0,255,0)
orange= (255,128,0)
blue= (0,0,255)
purple=(255,0,255)
sblue= (127, 215, 240)

WIDTH= 500
HEIGHT= 720
player_x= 200
player_speed= 10
player_direction= 0
 
ball_x= WIDTH/2
ball_y= HEIGHT-30
ball_x_direction=0
ball_y_direction=0
ball_x_speed=5
ball_y_speed=5

board = []
create_new = True
colors= [red, orange, green, blue, purple]
screen= pygame.display.set_mode([WIDTH, HEIGHT])
active= False
score =0

font= pygame.font.Font('freesansbold.ttf', 30)


def create_new_board():
    board = []
    rows= random.randint(4, 8)
    for i in range(rows):
        row= []
        for j in range(5):
            row.append(random.randint(1, 5))
        board.append(row)
    return board

def draw_board(board):
    board_squares= []
    for i in range (len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0: 
                piece= pygame.draw.rect(screen, colors[(board[i][j]) -1], [j * 100, i*40, 99, 38],0,5)
                pygame.draw.rect(screen, Black, [j * 100, i*40, 99, 38], 3 , 3 )
                top= pygame.rect.Rect((j * 100, i * 40), (99, 1))
                bottom= pygame.rect.Rect((j * 100, (i * 40) + 37), (99, 1))
                left= pygame.rect.Rect((j * 100, i * 40), (37, 1))
                right= pygame.rect.Rect(((j * 100) +97 , i * 40), (37, 1))
                board_squares.append([top, bottom, left, right, (i,j)])
    return board_squares


run= True 
while run:
    screen.fill(sblue)
    timer.tick(fps)
    if create_new:
        board= create_new_board()
        create_new= False
    squares= draw_board(board)

    player= pygame.draw.rect(screen, Black,[player_x, HEIGHT- 20, 100,13], 0 ,3)
    ball = pygame.draw.circle(screen, White, (ball_x, ball_y), 10)
    pygame.draw.circle(screen, Black, (ball_x, ball_y),10 ,2)


    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            run= False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not active:
                active = True
                ball_y_direction= -1
                ball_x_direction= random.choice([1, 1])
                score =0
            if event.key == pygame.K_RIGHT and active:
                player_direction = 1
            if event.key == pygame.K_LEFT and active:
                player_direction = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_direction = 0
            if event.key == pygame.K_LEFT:
                player_direction = 0

    if ball_x <= 10 or ball_x>= WIDTH-10:
        ball_x_direction *= -1

    if player_x <= -30 or player_x >= WIDTH-70:
        player_direction *= -1

    for i in range(len(squares)):
        if ball.colliderect(squares[i][0]) or ball.colliderect(squares[i][1]):
            ball_y_direction *= -1
            board[squares[i][4][0]][squares[i][4][1]] -= 1
            score +=1
        if (ball.colliderect(squares[i][2]) and ball_x_direction == 1) or (ball.colliderect(squares[i][3]) and ball_x_direction == -1):
            ball_x_direction *= -1
            board[squares[i][4][0]][squares[i][4][1]] -= 1
            score += 1

    if ball.colliderect(player):
        if player_direction == ball_x_direction:
            ball_x_speed += 1
        elif player_direction == -ball_x_direction and ball_x_speed > 1:
            ball_x_speed -= 1
        elif player_direction == -ball_x_direction and ball_x_speed == 1:
            ball_x_direction *= -1


        ball_y_direction *= -1

    
    ball_y += ball_y_direction * ball_y_speed
    ball_x += ball_x_direction * ball_x_speed
    player_x += player_direction * player_speed

    if ball_y <=10:
        ball_y= 10
        ball_y_direction *= -1


    if ball_y >= HEIGHT-10 or len(squares)== 0:
        active= False
        player_x= 200
        player_speed= 8
        player_direction= 0
        
        ball_x= WIDTH/2
        ball_y= HEIGHT-30
        ball_x_direction=0
        ball_y_direction=0
        ball_x_speed=5
        ball_y_speed=5
        create_new= True

    
    score_text= font.render(f'Score {score}', True, Black)
    screen.blit(score_text, (200,5))
    score_text= font.render(f'Score {score}', True, White)
    screen.blit(score_text, (201,5))



    if not active:
        start_text= font.render("PRESS SPACE TO START", True, Black)
        screen.blit(start_text, (70,320))

    pygame.display.flip()
pygame.quit()
