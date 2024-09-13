import config
from random import randint


class Enemy:
    '''is in charge of enemy AI representations'''
    def __init__(self, name) -> None:
        self.name = name

    def computer_random_move(self, pole):
        '''randomly selects a cell to attack'''
        already_attacked = []
        while True:
            x = randint(0, 9)
            y = randint(0, 9)
            cell = pole.cells[x][y]
            if (x, y) in already_attacked:
                continue
            already_attacked.append((x, y))

            if cell.is_ship and not cell.is_hit:
                # Mark the cell as hit
                cell.is_hit = True
                cell.image = config.hit_image_const
                for ship in pole.ships:
                    if cell in ship.cells_ship:
                        ship.ship_strike()
                        if not ship.is_alive:
                            pole.destruction_of_ship(ship)
                            return
                        return
            
            elif cell.is_hidden:
                pole.cells[x][y].is_hidden = False
                return
            else:
                continue
    
    def computer_hunter_move(self, pole):
        '''Computer behaviour where it chooses a cell to attack 
        based on the last hit to find all the decks of the affected ship faster'''
        pass # the idea is great - I haven't been able to realise it yet


