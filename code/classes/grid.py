from .house import House
from .battery import Battery
import numpy as np
import sys

class Grid:
    def __init__(self, district: str):
        file_batteries: str = "data/district_" + district + "/district-" + district + "_batteries.csv"
        file_houses: str= "data/district_" + district + "/district-" + district + "_houses.csv"

        self.district = district
        self.batteries: list[Battery] = self.read_batteries(file_batteries)
        self.houses: list[House] = self.read_houses(file_houses)

        self.grid = self.init_grid()

        self.cost = 0

    def read_batteries(self, filename) -> list[Battery]:
        batteries: list[Battery] = []

        with open(filename) as f:
            for line in f:
                if line == "positie,capaciteit\n":
                    pass
                else:
                    data = self.split_line_in_file(line)
                        
                    batteries.append(Battery(data[0], data[1], data[2]))

        return batteries

    def read_houses(self, filename) -> list[House]:
        houses: list[House] = []

        with open(filename) as f:
            for line in f:
                if line == "x,y,maxoutput\n":
                    pass
                else:
                    data = self.split_line_in_file(line)
                        
                    houses.append(House(data[0], data[1], data[2]))

        return houses

    def split_line_in_file(self, line: str) -> tuple[int, int, float]:
        line = line.replace("\"", "")
        line = line.replace("\n", "")
        values: list[str] = line.split(",")

        x = int(values[0])
        y = int(values[1])
        capacity = float(values[2])
                        
        return (x, y, capacity)

    def init_grid(self):
        size_grid: tuple(int, int) = self.size_grid()

        grid: list[list[tuple[str, int]]] = np.zeros((size_grid[0], size_grid[1]), dtype=tuple)

        for battery in self.batteries:
            grid[battery.coord_y][battery.coord_x] = battery

        for house in self.houses:
            grid[house.coord_y][house.coord_x] = house

        return grid

    def size_grid(self):
        max_x: int = 0
        max_y: int = 0

        all: list[object] = self.batteries + self.houses

        for obj in all:
            if obj.coord_x > max_x:
                max_x = obj.coord_x
            if obj.coord_x > max_y:
                max_y = obj.coord_y

        # change max values to fit our own representation of the data
        max_x = max_x + 1
        max_y = max_y + 1

        return (max_x, max_y)

    def print_grid(self):
        np.set_printoptions(threshold=sys.maxsize)
        print(self.grid)

    def add_cost(self, cost):
        self.cost = cost