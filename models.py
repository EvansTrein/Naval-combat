import pygame
import config
from random import randint

# upload pictures to display hits and ship
hit_image = pygame.image.load(config.hit_image_const)  
hit_image = pygame.transform.scale(hit_image, (40, 40))  
ship_image = pygame.image.load(config.ship_image_const) 
ship_image = pygame.transform.scale(ship_image, (40, 40))

class Cell:
    '''is responsible for representing a cell on the playing field'''
    def __init__(self, name, coords):
        self.name = name  # A1 - J10
        self.coords = coords  # coordinates for a two-dimensional array
        self.is_ship = False
        self.is_hit = False
        self.is_hidden = True
        self.image = None

    def draw(self, screen, x, y, square_size):
        '''method determines how to display a particular cell'''
        if self.is_hidden:
            pygame.draw.rect(screen, (0, 0, 255), (x, y, square_size, square_size))
        elif self.is_ship and self.is_hit:
            screen.blit(hit_image, (x, y))  # Display hit image if ship is hit
        elif self.is_ship:
            screen.blit(ship_image, (x, y))  # Display ship image if ship is not hit
        elif self.is_hit:
            screen.blit(hit_image, (x, y))  # Display hit image if cell is hit but no ship
        else:
            pygame.draw.rect(screen, (200, 200, 200), (x, y, square_size, square_size), 1)

    def __repr__(self) -> str:
        return f'{self.name}, {self.coords}'


class Ship:
    '''is responsible for representing the ship on the playing field'''
    def __init__(self, deck_count) -> None:
        self.deck_count = deck_count
        self.is_alive = True
        self.cells_ship = []  # each ship will store cells in which is present / list of decks

    def ship_strike(self):
        '''this method will be called every time the ship is hit'''
        self.deck_count -= 1
        if self.deck_count == 0:
            self.is_alive = False

    def __repr__(self) -> str:
        return f'{self.cells_ship}, {self.is_alive}'


class Pole:
    '''is responsible for representing the playing field'''

    NAMES_FOR_CELLS = tuple(y + str(x) for x in range(1, 11) for y in ("ABCDEFGHIJ"))

    def __init__(self):
        self.width = 10
        self.height = 10
        self.cells = []  # the field itself is a two-dimensional array
        self.ships = [Ship(4), 
                    Ship(3), Ship(3), 
                    Ship(2), Ship(2), Ship(2),
                    Ship(1), Ship(1), Ship(1), Ship(1)]
    
    def create_pole(self):
        '''this method will create the playing field'''
        for_name = 0
        x = -1
        for _ in range(self.height):
            x += 1
            row = []
            y = 0
            for _ in range(self.width):
                cell_name = Pole.NAMES_FOR_CELLS[for_name]
                cell = Cell(cell_name, (x, y))
                row.append(cell)
                for_name += 1
                y += 1
            self.cells.append(row)
    
    def hide_ships(self):
        '''this method will hide the ships on the playing field'''
        for row in self.cells:
            for x in row:
                x.is_hidden = True

    def is_end(self):
        '''checks that not all ships are destroyed, if they are - the game ends'''
        if all(not ship.is_alive for ship in self.ships):
            return True
        return False
    
    def destruction_of_ship(self, ship):
        '''triggers when the ship is destroyed, opening all neighbouring cells'''
        # coordinates of all neighbouring cells, relative to the ship 
        indxs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for cell in ship.cells_ship:
            x, y = cell.coords
            for i in indxs:
                nx, ny = x + i[0], y + i[1]
                # checking that we stay within the field boundary 
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    self.cells[nx][ny].is_hidden = False

    def init_ships(self):
        '''
        allocation of all ships
        first randomly determines the orientation of the ship
        ships must not touch each other, each ship has 1 free square around it
        '''
        for ship in self.ships:
            while True:
                # choose a random orientation for the ship (horizontal or vertical)
                orientation = randint(0, 1)
                if orientation == 0:  # Horizontal orientation
                    # choose a random row and column for the start of the ship
                    row = randint(0, self.height - 1)
                    col = randint(0, self.width - ship.deck_count)
                    # check if the ship fits within the field boundaries
                    if col + ship.deck_count <= self.width:
                        # check if the ship does not collide with other ships
                        is_valid = True
                        for i in range(ship.deck_count):
                            for cell in [self.cells[row][col + j] for j in range(ship.deck_count)]:
                                if cell.is_ship:
                                    is_valid = False
                                    break
                            if not is_valid:
                                break
                        # check for diagonal cells
                        for i in range(-1, 2):
                            for j in range(-1, ship.deck_count + 1):
                                if i != 0 or j != 0:
                                    if 0 <= row + i < self.height and 0 <= col + j < self.width:
                                        if self.cells[row + i][col + j].is_ship:
                                            is_valid = False
                                            break
                            if not is_valid:
                                break
                        if is_valid:
                            # place the ship on the field
                            for i in range(ship.deck_count):
                                self.cells[row][col + i].is_ship = True
                                self.cells[row][col + i].image = ship_image
                                self.cells[row][col + i].is_hidden = False
                                ship.cells_ship.append(self.cells[row][col + i])
                            break
                else:  # vertical orientation
                    # choose a random row and column for the start of the ship
                    row = randint(0, self.height - ship.deck_count)
                    col = randint(0, self.width - 1)
                    # check if the ship fits within the field boundaries
                    if row + ship.deck_count <= self.height:
                        # check if the ship does not collide with other ships
                        is_valid = True
                        for i in range(ship.deck_count):
                            for cell in [self.cells[row + i][col] for _ in range(self.width)]:
                                if cell.is_ship:
                                    is_valid = False
                                    break
                            if not is_valid:
                                break
                        # check for diagonal cells
                        for i in range(-1, ship.deck_count + 1):
                            for j in range(-1, 2):
                                if i != 0 or j != 0:
                                    if 0 <= row + i < self.height and 0 <= col + j < self.width:
                                        if self.cells[row + i][col + j].is_ship:
                                            is_valid = False
                                            break
                            if not is_valid:
                                break
                        if is_valid:
                            # place the ship on the field
                            for i in range(ship.deck_count):
                                self.cells[row + i][col].is_ship = True
                                self.cells[row + i][col].image = ship_image
                                self.cells[row + i][col].is_hidden = False
                                ship.cells_ship.append(self.cells[row + i][col])
                            break


