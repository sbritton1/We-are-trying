from .house import House
from .battery import Battery
import numpy as np
import sys
from typing import Union

class Grid:
    """
    Class to read out files and store its contents
    """

    def __init__(self, district: str):
        """
        Class initializer.
        Pre: district is a string of a number
        Post: self variables created
        """

        # create file paths to where the data is stored
        file_batteries: str = "data/district_" + district + "/district-" + district + "_batteries.csv"
        file_houses: str= "data/district_" + district + "/district-" + district + "_houses.csv"

        self.district = district
        self.batteries: list[Battery] = self.read_batteries(file_batteries)
        self.houses: list[House] = self.read_houses(file_houses)

        # self.grid = self.init_grid()

        self.cost = 0

    def read_batteries(self, filename: str) -> list[Battery]:
        """
        Reads files where data for the batteries is stored
        Pre: filename is a string
        Post: returns list of objects of class Battery
        """
        
        batteries: list[Battery] = []

        with open(filename) as f:
            for line in f:

                # Ignore the first line in the file
                if line == "positie,capaciteit\n":
                    pass
                else:

                    # split the line into only its relevant data
                    data = self.split_line_in_file(line)
                        
                    batteries.append(Battery(data[0], data[1], data[2]))

        return batteries

    def read_houses(self, filename) -> list[House]:
        """
        Reads files where data for the houses is stored
        Pre: filename is a string
        Post: returns list of objects of class House
        """

        houses: list[House] = []

        with open(filename) as f:
            for line in f:

                # ignores first line in the file
                if line == "x,y,maxoutput\n":
                    pass
                else:

                    # split line into only its relevant data
                    data = self.split_line_in_file(line)
                        
                    houses.append(House(data[0], data[1], data[2]))

        return houses

    def split_line_in_file(self, line: str) -> tuple[int, int, float]:
        """
        Removes junk characters from line and
        split the line into components
        Pre: line is a string
        Post: returns tuple of int, int, float
        """

        # remove quote and newline characters
        line = line.replace("\"", "")
        line = line.replace("\n", "")
        values: list[str] = line.split(",")

        # give meaning to the values and return them
        x = int(values[0])
        y = int(values[1])
        capacity = float(values[2])
                        
        return (x, y, capacity)

    def init_grid(self) -> list[list[tuple[Union[Battery, House]]]]:
        """
        Creates 2d numpy array, which represents the
        grid in which all the batteries and houses lie
        Post: returns 2d array of 0's and objects
        """

        # find size grid needs to be
        size_grid: tuple(int, int) = self.size_grid()

        # create empty grid
        grid: list[list[tuple[str, int]]] = np.zeros((size_grid[0], size_grid[1]), dtype=tuple)

        # add batteries to correct coordinate in grid
        for battery in self.batteries:
            grid[battery.coord_y][battery.coord_x] = battery

        # add houses to correct coordinate in grid
        for house in self.houses:
            grid[house.coord_y][house.coord_x] = house

        return grid

    def size_grid(self):
        """
        Find largest x and y coordinates of objects
        to know how large the grid will be
        Pre: self has non-empty list of batteries and houses
        Post: return tuple of two ints
        """

        max_x: int = 0
        max_y: int = 0

        # combine lists to make looping easier
        all: list[object] = self.batteries + self.houses

        for obj in all:

            # check if x or y coordinate is larger than previous max
            if obj.coord_x > max_x:
                max_x = obj.coord_x
            if obj.coord_x > max_y:
                max_y = obj.coord_y

        # change max values to fit our own representation of the data
        max_x = max_x + 1
        max_y = max_y + 1

        return (max_x, max_y)

    def print_grid(self):
        """
        Print out the grid into the terminal.
        Post: prints array
        """

        # make sure entire array appears in terminal
        np.set_printoptions(threshold=sys.maxsize)
        print(self.grid)

    def add_cost(self, cost: int):
        """
        Give grid a cost based on calculation elsewhere
        Pre: cost is an int
        Post: self.cost has been given a value
        """

        self.cost = cost