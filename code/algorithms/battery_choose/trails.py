from copy import copy

from ...classes.grid import Grid
from ...classes.battery import Battery
from ...classes.house import House

""""
NOTE: Dit algoritme is niet afgemaakt, maar was bedoeld voor de laatste
gradatie van de case, waarin batterijen zelf gekozen en geplaatst mochten
worden uit een bepaalde selectie. 

Het idee van dit algoritme is als volgt:

Maak van elk huis een Trail object. Deze houdt bij welke huizen er aan
gekoppeld zijn, met welke kabels deze zijn verbonden en de totale output van de
huizen in deze trail. Deze trail houdt ook bij welke batterij nodig is om aan
de output te voldoen. Hiermee kan dus ook de kosten van de trail worden
bepaald. 

Vervolgens kan naar elke combinatie van trails worden gekeken en kan worden
nagegaan welke combinatie de kosten het meeste mindert. Hierbij wordt gekeken
naar de kosten van de kabels om de trails te verbinden en de besparing van
kosten door een batterij te delen. 

Dit wordt herhaald totdat er geen mogelijke combinaties van trails meer zijn
die de kosten verbeteren.
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


            