import random

from .house import House
from .battery import Battery


class Grid:
    """
    Class representing a grid on which houses and batteries lay. Can load these
    houses and batteries from csv files.
    """

    def __init__(self, district: str, load_csv: bool = True) -> None:
        """
        Class initializer. Reads the grid data from csv files if load_csv is
        set to True.

        Pre : district is a string of a number in range 1 to 3
        Post: attributes are initialized and filled from the csv files
              if load_csv is True
        """

        # create file paths to where the data is stored
        file_batteries: str = "data/district_" + district + "/district-" + \
                              district + "_batteries.csv"
        file_houses: str = "data/district_" + district + "/district-" + \
                           district + "_houses.csv"

        self.district = district

        self.batteries: list[Battery] = []
        self.houses: list[House] = []

        self.used_coordinates: list[tuple[int, int]] = []

        self.total_maxoutput = 0

        # read csv files storing the data
        if load_csv:
            # self.batteries = self.read_batteries(file_batteries)
            self.houses = self.read_houses(file_houses)

            self.max_x, self.max_y = self.size_grid()

            self.batteries = self.read_batteries(file_batteries)

    def read_batteries(self, filename: str) -> list[Battery]:
        """
        Reads the file with given filename and creates the Battery objects from
        this data.

        Pre : filename is a string and is an existing filepath for the battery
              data
        Post: returns list of objects of class Battery read from the data
        """

        batteries: list[Battery] = []

        with open(filename) as f:
            # skip header line
            next(f)

            for line in f:
                # split the line into only its relevant data
                x, y, capacity = self.split_line_in_file(line)

                self.add_used_coordinates(x, y)

                batteries.append(Battery(x, y, capacity))

        return batteries

    def read_houses(self, filename) -> list[House]:
        """
        Reads the file with given filename and creates the House objects from
        this data.

        Pre : filename is a string and is an existing filepath for the house
              data
        Post: returns list of objects of class House read from the data
        """

        houses: list[House] = []

        with open(filename) as f:
            # skip header line
            next(f)

            for line in f:
                # split line into only its relevant data
                x, y, maxoutput = self.split_line_in_file(line)

                self.add_used_coordinates(x, y)

                self.total_maxoutput += maxoutput

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

        # cast values to the right types
        x = int(values[0])
        y = int(values[1])
        capacity = float(values[2])

        return (x, y, capacity)

    def size_grid(self) -> tuple[int, int]:
        """
        Find the size the grid should be, depending on the location of the
        houses and batteries.

        Pre : self has non-empty lists for the batteries and houses
        Post: return tuple of two ints where the first int is the maximum
              x-value of all the batteries and houses and the second int is the
              maximum y-value of all the batteries and houses
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
        Calculates the price of the grid for the 'normal' case.

        Post: returns an int representing the cost and stores it in the
              attribute self.cost
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
        Calculates the price of the grid when cables can be shared.

        Post: returns an int cost
        """

        # each battery in the grid costs 5000
        self.cost: int = len(self.batteries) * 5000

        for house in self.houses:
            self.cost += (len(house.cables) - 1) * 9

        return self.cost

    def lay_unique_cables(self) -> None:
        """
        Lays non-shared cables on the grid to satisfy all the connections.

        Pre : all houses in the houses attribute are connected properly
        Post: the correct cables are stored in the house objects in the houses
              attribute
        """

        for house in self.houses:
            house.lay_cables()

    def lay_shared_cables(self) -> None:
        """
        Lays shared cables on the grid to satisfy all the connections.

        Pre : all houses in the houses attribute are connected properly
        Post: the correct cables are stored in the house objects in the houses
              attribute
        """

        for battery in self.batteries:
            battery.lay_shared_cables()

    def remove_cables(self) -> None:
        """
        Removes all cables in the grid.

        Post: all cables are removed from the battery objects in the batteries
              attribute and from all connected house objects in each of these
              battery
        """

        for battery in self.batteries:
            battery.remove_cables()

    def set_cost(self, cost: int) -> None:
        """
        Sets the cost of the grid to the given cost.

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

    def move_battery(self, battery: Battery, new_x: int, new_y: int) -> bool:
        """
        Moves battery if it can move to place if the coordinates do not
        contain a house.

        Pre : type hints are met and battery is a battery in the batteries
              attribute
        Post: if the new coordinates are free, the battery is moved to these
              coordinates, its cables are removed, used_coordinates attribute
              is updated and True is returned, if new coordinates are not free
              False is returned
        """

        if self.is_coordinates_free(new_x, new_y) is True:
            # free up the old coordinates
            old_x, old_y = battery.get_coords()
            self.remove_used_coordinates(old_x, old_y)

            # remove all the cables from the grid
            self.remove_cables()

            # move battery
            battery.move_to(new_x, new_y)
            self.add_used_coordinates(new_x, new_y)

            # return true to notify the battery was moved
            return True
        return False

    def is_coordinates_free(self, x: int, y: int) -> bool:
        """
        Checks if coordinates are not occupied by a house or battery.

        Pre : x and y are positive integers
        Post: returns True if (x, y) is not in the used coordinates, returns
              False if not
        """

        if x < self.max_x and y < self.max_y:
            return (x, y) not in self.used_coordinates
        return False

    def add_used_coordinates(self, x: int, y: int) -> None:
        """
        Sets coordinates as occupied.

        Pre : x and y are positive integers that are smaller than the max_x and
              max_y attributes respectively
        Post: (x, y) is appended to the used_coordinates attribute
        """

        self.used_coordinates.append((x, y))

    def remove_used_coordinates(self, x: int, y: int) -> None:
        """
        Sets coordinates as no longer occupied.

        Pre : x and y are integers
        Post: (x, y) is removed from the used_coordinates attribute if it was
              there in the first place
        """

        self.used_coordinates.remove((x, y))

    def remove_all_connections(self) -> None:
        """
        Removes all connections from batteries to houses.

        Pre : none
        Post: all connections of the battery objects in the batteries attribute
              are removed
        """

        for battery in self.batteries:
            battery.disconnect_all_houses()

    def make_powerstar(self, x: int, y: int) -> None:
        """
        Makes a Powerstar battery and places it on the grid.

        Pre : x and y are positive integers that are smaller than the max_x and
              max_y attributes respectively
        Post: a battery object with the specs of Powerstar is created and
              appended to the batteries attribute
        """

        self.batteries.append(Battery(x, y, 450.0))

    def make_immerse_2(self, x: int, y: int) -> Battery:
        """
        Makes a Immerse-II battery and places it on the grid.

        Pre : x and y are positive integers that are smaller than the max_x and
              max_y attributes respectively
        Post: a battery object with the specs of Immerse-II is created and
              appended to the batteries attribute
        """

        self.batteries.append(Battery(x, y, 900.0))

    def make_immerse_3(self, x: int, y: int) -> Battery:
        """
        Makes a Immerse-III battery and places it on the grid.

        Pre : x and y are positive integers that are smaller than the max_x and
              max_y attributes respectively
        Post: a battery object with the specs of Immerse-III is created and
              appended to the batteries attribute
        """

        self.batteries.append(Battery(x, y, 1800.0))

    def calc_cost_advanced(self):
        """
        Calculates the price of a grid for the Advanced case.

        Pre : the Battery objects in the batteries attribute are only of the
              types Powerstar, Immerse-II or Immerse-III
        Post: returns an integer representing the cost
        """

        # cost calculation for 3 types of batteries
        for battery in self.batteries:
            if battery.total_capacity == 450.0:
                self.cost += 900
            elif battery.total_capacity == 900.0:
                self.cost += 1350
            else:
                self.cost += 1800

        for house in self.houses:
            self.cost += (len(house.cables) - 1) * 9

        return self.cost

    def initialize_advanced_batteries(self) -> list[Battery]:
        """
        NOT FINISHED AND USED!

        Generates advanced batteries such that there is enough
        capacity.

        Pre : none
        Post: none
        """

        batteries: list[Battery] = []

        needed_capacity: float = self.total_maxoutput

        while needed_capacity > 0:
            # get x and y coordinate that is not occupied by house
            while True:
                new_x = random.randrange(0, 50)
                new_y = random.randrange(0, 50)

                if self.is_coordinates_free(new_x, new_y):
                    self.add_used_coordinates(new_x, new_y)
                    break

            # chooses randomly which battery to add
            new_battery: str = random.choice(["p", "i_2", "i_3"])
            if new_battery == "p":
                another_battery = self.make_powerstar(new_x, new_y)
                needed_capacity -= 450.0
            elif new_battery == "i_2":
                another_battery = self.make_immerse_2(new_x, new_y)
                needed_capacity -= 900.0
            else:
                another_battery = self.make_immerse_3(new_x, new_y)
                needed_capacity -= 1800.0
            batteries.append(another_battery)
        return batteries
