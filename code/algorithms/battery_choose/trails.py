from copy import copy

from ...classes.grid import Grid
from ...classes.battery import Battery
from ...classes.house import House

""""
Het idee van dit algoritme is als volgt:

Ga alle combinaties van huizen langs en vind de combinatie met de kortste
afstand. Hier kan vervolgens een Trail object van worden gemaakt. Deze houdt
bij welke huizen er aan gekoppeld zijn, met welke kabels deze zijn verbonden
en de totale output van de huizen in deze trail. 
"""

batteries = {
    450: {"type": "Powerstar", "cost": 900},
    900: {"type": "Imerse-II", "cost": 1350},
    1800: {"type": "Imerse-III", "cost": 1800},
}

def trails(grid: Grid) -> Grid:

    # make a shallow copy of the houses list
    houses_copy = copy(grid.houses)

    # go over all houses

        # go over all remaining houses in the shallow copy and find the
        # distance, remove this considered house from the shallow copy

    # connect the closest houses

    # repeat untill all houses are connected

    # look if trails can be combined or 
    

    return grid


class Trail():
    def __init__(self, house1: House, house2: House) -> None:
        self.houses: list[House] = [house1, house2]
        self.total_load = 0.0

        self.battery = batteries[450]

        self.cables: set[str] = {f"{house1.coord_x},{house1.coord_y}"}

        self.connect_house(house2)

    def connect_house(self, house: House) -> None:
        self.houses.append(house)
        self.total_load += house.maxoutput

    def get_distance_to_house(self, house: House) -> int:

        min_distance = 999

        house_x, house_y = house.coord_x, house.coord_y
        
        for cable in self.cables:
            cable_x, cable_y = [int(coord) for coord in cable.split(",")]

            abs_dist_x = abs(cable_x - house_x)
            abs_dist_y = abs(cable_y - house_y)

            distance = abs_dist_x + abs_dist_y

            min_distance = min(min_distance, distance)

        return min_distance

    def add_cables(self, house: House) -> None:
        pass


            