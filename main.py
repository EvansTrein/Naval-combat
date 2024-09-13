import pygame
import config
from enemy import Enemy
from models import Pole, hit_image
from victory_screen import victory

# initialises Pygame
pygame.init()
# creating the main window for the game 
screen = pygame.display.set_mode((1100, 1000))

# initialise your own and the enemy's field, set up ships
my_pole = Pole()
my_pole.create_pole()
my_pole.init_ships()
enemy_pole = Pole()
enemy_pole.create_pole()
enemy_pole.init_ships()
enemy_pole.hide_ships()  # hide the enemy ships so we can't see them when we play

# create someone to play with
enemy = Enemy('Kyle')

# set up field dimensions and positions
square_size = 40
field_width = 10 * square_size
field_height = 10 * square_size
field1_x = (1100 - field_width) // 2
field1_y = 50  
field2_x = field1_x
field2_y = 550  

# set up font for labels
font = pygame.font.Font(None, config.TYPEFACE)

GAME = True

# game logic
while GAME:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get the mouse position
            mouse_x, mouse_y = event.pos

            # check if the click is within the enemy field
            if field1_x <= mouse_x <= field1_x + field_width and field1_y <= mouse_y <= field1_y + field_height:
                # calculate the cell coordinates
                cell_x = (mouse_x - field1_x) // square_size
                cell_y = (mouse_y - field1_y) // square_size

                # get the cell object
                cell = enemy_pole.cells[cell_y][cell_x]

                # open the cell
                cell.is_hidden = False

                # check if the cell is a ship
                if cell.is_ship:
                    # mark the cell as hit
                    cell.is_hit = True
                    cell.image = hit_image
                    for ship in enemy_pole.ships:
                        if cell in ship.cells_ship:
                            ship.ship_strike()
                            # if a ship is destroyed, opens all its neighbouring cells 
                            if not ship.is_alive:
                                enemy_pole.destruction_of_ship(ship)
                                
                # checking to see if the person has won
                if enemy_pole.is_end():
                    config.WINNER = 'Human'
                    GAME = False

                # now it's the computer's turn
                enemy.computer_random_move(my_pole)

                # checking to see if the computer has won
                if my_pole.is_end():
                    config.WINNER = 'Computer'
                    GAME = False
                

    # clear screen and draw background
    screen.fill((50, 50, 50))

    # draw row and column labels for both fields
    for i in range(10):
        label = font.render(str(i+1), True, (255, 255, 255))
        screen.blit(label, (field1_x - 30, field1_y + i * square_size + 10))
        screen.blit(label, (field2_x - 30, field2_y + i * square_size + 10))

    for i in range(10):
        label = font.render(chr(ord('A') + i), True, (255, 255, 255))
        screen.blit(label, (field1_x + i * square_size + 10, field1_y - 30))
        screen.blit(label, (field2_x + i * square_size + 10, field2_y - 30))

    # field rendering
    for i in range(10):
        for j in range(10):
            cell = my_pole.cells[i][j]
            cell.draw(screen, field2_x + j * square_size, field2_y + i * square_size, square_size)
        
            cell = enemy_pole.cells[i][j]
            cell.draw(screen, field1_x + j * square_size, field1_y + i * square_size, square_size)

    # update the game screen
    pygame.display.flip()

victory()