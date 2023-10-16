import pygame
from direction import Direction  
from ship_brain import Brain
from ship_brain import State
from ship_brain import GeneralBrain
from os import urandom
from grid import Grid
from items import *
from random import choices

pygame.init()
  

canvas = pygame.display.set_mode((800, 800))
  
sheep_sprite = pygame.image.load("sprites/Sheep.jpg")
shepperd_sprite = pygame.image.load("sprites/Shepperd.jpg")
cheese_sprite = pygame.image.load("sprites/Cheese.jpg")

shepperd_sprite = pygame.transform.scale(shepperd_sprite, (50, 50))
sheep_sprite = pygame.transform.scale(sheep_sprite, (50, 50))
cheese_sprite = pygame.transform.scale(cheese_sprite, (50, 50))

FPS = 10


def update_screen():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

def show_game_over():
    text = pygame.font.Font(None, 36).render("Game Over", True, (255, 255, 255))
    canvas.blit(text, (250, 250))





grid = Grid(16, 800)

shepperd = Shepperd(0, 5, grid)
current_sheep = Sheep(grid.random_cell(), grid.random_cell())

attack_brain = Brain(0.78)
defense_brain = Brain(0.8)

game_over = False

print_state = False
print_policy = False

manual = False

past_positions = []
past_directions = []
direction = Direction.RIGHT

while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            print(attack_brain.current_policy)
         
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                if (FPS == 10):
                    FPS = 15000
                else:
                    FPS = 10
            elif (event.key == pygame.K_d):
                print_state = not print_state
            elif event.key == pygame.K_p:
                print_policy = not print_policy
            elif (manual):
                if (event.key == pygame.K_a and direction != Direction.RIGHT):
                    direction = Direction.LEFT
                elif (event.key == pygame.K_w and direction != Direction.DOWN):
                    direction = Direction.UP
                elif (event.key == pygame.K_d and direction != Direction.LEFT):
                    direction = Direction.RIGHT
                elif (event.key == pygame.K_s and direction != Direction.UP):
                    direction = Direction.DOWN
        

    

    if (not manual):
        pass
        state = State(shepperd.get_sheep_direction(current_sheep), shepperd.get_queue_directions(past_positions[1:shepperd.sheeps], direction))
        if (print_state):
            print(state)
        direction = attack_brain.choose_direction(state, direction)
        #attack_direction = attack_brain.current_policy.get_action(State(shepperd.get_sheep_direction(current_sheep), set()), direction)
        #defense_direction = defense_brain.current_policy.get_action(State(Direction.UP, shepperd.get_queue_directions(past_positions[3:])), direction)

        

        

    past_directions.insert(0, direction)
    if (len(past_directions) >= 100):
        past_directions.pop()

    shepperd.move(direction)

    
    if (len(past_positions) >= 200):
        past_positions.pop()

    if (shepperd.x_cell == current_sheep.x_cell and shepperd.y_cell == current_sheep.y_cell):
        current_sheep = Sheep(grid.random_cell(), grid.random_cell())
        shepperd.sheeps += 1
        attack_brain.add_reward(50)
        #attack_brain.evaluate()
    else:
        attack_brain.add_reward(-1)

    for i in range(shepperd.sheeps):
        if ((shepperd.x_cell, shepperd.y_cell) == past_positions[i]):
            shepperd = Shepperd(0, 5, grid)
            current_sheep = Sheep(grid.random_cell(), grid.random_cell())
            attack_brain.add_reward(-300)
            attack_brain.evaluate()
            break

    
    past_positions.insert(0, (shepperd.x_cell, shepperd.y_cell))

    if (print_policy):
        print(attack_brain.current_policy)


    canvas.fill((255, 255, 255))
            

    canvas.blit(shepperd_sprite, (grid.from_cell(shepperd.x_cell), grid.from_cell(shepperd.y_cell)))
    for i in range(0, shepperd.sheeps):
        canvas.blit(cheese_sprite, (grid.from_cell(past_positions[i + 1][0]), grid.from_cell(past_positions[i + 1][1])))
            


    canvas.blit(sheep_sprite, (grid.from_cell(current_sheep.x_cell), grid.from_cell(current_sheep.y_cell)))

 
    update_screen()
    
   