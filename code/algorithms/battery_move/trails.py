from ...classes.grid import Grid
from ...classes.battery import Battery
from ...classes.house import House

def trails(grid: Grid) -> Grid:

    # go over all houses

    # search for the closest house and its distance to it

    # connect the closest houses

    # repeat untill all houses are connected

    # look if trails can be combined or 
    

    return grid


class Trail():
    def __init__(self) -> None:
        self.houses: list[House] = []
        self.total_load = 0.0

    def connect_house(self, house: House) -> None:
        self.houses.append(house)
        self.total_load += house.maxoutput

    def get_distance_to_house(self, house: House) -> None:
        
        for trail_house in self.houses:
            trail_x, trail_y = trail_house.coord_x, trail_house.coord_y
            