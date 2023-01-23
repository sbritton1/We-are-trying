from .house import House
from .battery import Battery
import numpy as np
import sys
from typing import Union

class Grid:
    """
    Class representing a grid in which houses and batteries lay.
    Also has methods to change the properties of objects within self.
    """

    def __init__(self, district: str, load_csv: bool = True) -> None:
        """
        Class initializer.

        Pre : district is a string of a number
        Post: self variables created
        """

        # create file paths to where the data is stored
        file_batteries: str = "data/district_" + district + "/district-" + district + "_batteries.csv"
        file_houses: str= "data/district_" + district + "/district-" + district + "_houses.csv"

        self.district = district

        self.batteries: list[Battery] = []
        self.houses: list[House] = []

        # read csv files storing the data
        if load_csv:
            self.batteries = self.read_batteries(file_batteries)
            self.houses = self.read_houses(file_houses)

    def read_batteries(self, filename: str) -> list[Battery]:
        """
        Reads files where data for the batteries is stored.

        Pre : filename is a string
        Post: returns list of objects of class Battery
        """
        
        batteries: list[Battery] = []

        with open(filename) as f:
            # skip header line
            next(f)

            for line in f:
                    # split the line into only its relevant data
                    x, y, capacity = self.split_line_in_file(line)
                        
                    batteries.append(Battery(x, y, capacity))

        return batteries

    def read_houses(self, filename) -> list[House]:
        """
        Reads files where data for the houses is stored.

        Pre : filename is a string
        Post: returns list of objects of class House
        """

        houses: list[House] = []

        with open(filename) as f:
            # skip header line
            next(f)

            for line in f:
                # split line into only its relevant data
                x, y, maxoutput = self.split_line_in_file(line)

                # make House object and add it to the houses list    
                houses.append(House(x, y, maxoutput))

        return houses

    def split_line_in_file(self, line: str) -> tuple[int, int, float]:
        """
        Removes junk characters from line and split the line into components.

        Pre : line is a string
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

    def size_grid(self) -> tuple[int, int]:
        """
        Find largest x and y coordinates of objects to know how large the grid
        will be.

        Pre : self has non-empty list of batteries and houses
        Post: return tuple of two ints
        """

        max_x: int = 0
        max_y: int = 0

        # combine lists to make looping easier
        all_objects: list[object] = self.batteries + self.houses

        for obj in all_objects:

            # check if x or y coordinate is larger than previous max
            if obj.coord_x > max_x:
                max_x = obj.coord_x
            if obj.coord_x > max_y:
                max_y = obj.coord_y

        # change max values to fit our own representation of the data
        max_x = max_x + 1
        max_y = max_y + 1

        return (max_x, max_y)

    def calc_cost_normal(self) -> int:
        """
        Calculates the price of a grid.

        Pre : tmp_grid is of class Grid
        Post: returns an int cost
        """

        # each battery in the grid costs 5000
        self.cost: int = len(self.batteries) * 5000

        for house in self.houses:
            if house.has_connection is True:

                # each grid piece length of cable costs 9
                self.cost += house.distance_to_battery() * 9

        return self.cost

    def calc_cost_shared(self) -> int:
        """
        Calculates the price of a grid when cables can be shared.

        Pre : tmp_grid is of class Grid
        Post: returns an int cost
        """

        # each battery in the grid costs 5000
        self.cost: int = len(self.batteries) * 5000

        for house in self.houses:
            self.cost += (len(house.cables) - 1) * 9

        return self.cost

    def lay_unique_cables(self) -> None:
        """
        Lays non-shared cables for houses in self.

        Pre : self has houses
        Post: houses have cables
        """

        for house in self.houses:
            house.lay_cables()

    def lay_shared_cables(self) -> None:
        """
        Lays shared cables for batteries in self.

        Pre : self has batteries
        Post: houses in batteries have cables
        """

        for battery in self.batteries:
            battery.lay_shared_cables()

    def remove_cables(self) -> None:
        """
        Removes all cables in the grid.

        Pre : self has batteries
        Post: all cables are removed
        """

        for battery in self.batteries:
            battery.remove_cables()

    def set_cost(self, cost: int) -> None:
        """
        Sets the cost attribute to the given cost.

        Pre : cost is an integer
        Post: the cost attribute is set to the given cost
        """

        self.cost = cost

    def add_battery(self, battery: Battery) -> None:
        """
        Adds a battery to the grid.

        Pre : the batteries list attribute is initialized
        Post: the given battery is appended to the batteries list attribute
        """

        self.batteries.append(battery)

    def add_house(self, house: House) -> None:
        """
        Adds a house to the grid.

        Pre : the houses list attribute is initialized
        Post: the given house is appended to the houses list attribute
        """

        self.houses.append(house)
