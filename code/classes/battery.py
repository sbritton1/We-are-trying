from .house import House


class Battery:
    """
    Class that contains all information for batteries, such as
    its capacity, all the houses that are connected to the
    battery and its coordinates.
    """

    def __init__(self, x: int, y: int, capacity: float):
        self.coord_x: int = x
        self.coord_y: int = y
        self.total_capacity: int = capacity
        self.current_capacity: int = capacity

        self.connected_homes: list[House] = []

    def connect_home(self, house: House) -> None:
        """
        Connects house to battery and also substracts output from capacity.

        Pre : house from the house class
        Post: none
        """
        if self.current_capacity - house.maxoutput >= 0:
            self.current_capacity = self.current_capacity - house.maxoutput
            self.connected_homes.append(house)

    def disconnect_home(self, house: House) -> None:
        """
        Disconnects house from battery and also removes output of house.

        Pre : house from the house class
        Post: none
        """

        if house in self.connected_homes:
            # updates capacity for when house is disconnected
            self.current_capacity = self.current_capacity + house.maxoutput

            # disconnects house
            self.connected_homes.remove(house)

    def get_capacity(self) -> float:
        """
        Gets current capacity from battery.

        Pre : none
        Post: capacity as float
        """

        return self.current_capacity

    def is_connection_possible(self, house: House) -> bool:
        """
        Check if house does not overflow capacity of battery.

        Pre : house from house class
        Post: bool
        """

        return self.current_capacity - house.maxoutput >= 0

    def lay_shared_cables(self):
        """
        Lays shared cables in grid.

        Pre : none
        Post: none
        """

        # saves coordinates from a cable
        battery_cable: str = f"{self.coord_x},{self.coord_y}"

        # puts cables in a set, so there will be no duplicates
        self.cables: set[str] = {battery_cable}

        # gets all houses
        unconnected: list[int] = list(range(len(self.connected_homes)))

        for _ in range(len(self.connected_homes)):

            # random high placeholder
            min_dist: int = 100
            min_house: House = None
            min_cable: str = None
            loc_in_list: int = None

            for loc in unconnected:
                house = self.connected_homes[loc]
                for cable in self.cables:
                    distance = self.calc_distance(house, cable)

                    # updates cable if the distance is smaller
                    if distance < min_dist:
                        min_dist = distance
                        min_house = house
                        min_cable = cable
                        loc_in_list = loc

            # adds cable that connects house to cables list
            house_cable = f"{min_house.coord_x},{min_house.coord_y}"
            min_house.cables.append(house_cable)
            self.cables.add(house_cable)

            # gets coordinates from cable with whe smallest distance
            min_cable_x, min_cable_y = [int(coord) for coord in min_cable.split(",")]

            self.add_cables_y_axis(min_house, min_cable_y)

            self.add_cables_x_axis(min_house, min_cable_x, min_cable_y)

            unconnected.remove(loc_in_list)
            
    def get_axis_direction(self, start, end) -> int:
        """
        Returns 1 if the connection is in the negative axis direction and 1 if
        in the positive direction.
        
        Pre : a start and end coordinate as integer
        Post: returns direction as integer
        """

        if end - start < 0:
            return -1
        return 1

    def add_cables_x_axis(self, min_house: House, min_cable_x: int, min_cable_y: int) -> None:
        """
        Lays cables along the x_axis.
        
        Pre : house from class House, and three integers
        Post: none
        """
        
        direction = self.get_axis_direction(min_house.coord_x, min_cable_x)
        
        for new_x in range(min_house.coord_x, min_cable_x, direction):
            new_cable = f"{new_x + direction},{min_cable_y}"
            min_house.cables.append(new_cable)
            self.cables.add(new_cable)


    def add_cables_y_axis(self, min_house: House, end_coord: int) -> None:
        """
        Lays cables along the y_axis.
        
        Pre : house from class House, and two integers
        Post: none
        """
        
        direction = self.get_axis_direction(min_house.coord_y, end_coord)
        
        for new_y in range(min_house.coord_y, end_coord, direction):
            new_cable = f"{min_house.coord_x},{new_y + direction}"
            min_house.cables.append(new_cable)
            self.cables.add(new_cable)

    def calc_distance(self, house: House, cable: str) -> int:
        """
        Calculates the distance between a house and a cable.

        Pre : house from the house class and a cable as a string
        Post: distance as integer
        """

        # gets cable coordinates
        cable_coords: tuple(int, int) = [int(coord) for coord in cable.split(",")]

        # calculates distance between a cable and a house
        distance: int = abs(house.coord_x - cable_coords[0]) + abs(house.coord_y - cable_coords[1])

        return distance

    def remove_cables(self) -> None:
        """
        Removes connected cables from grid.

        Pre : none
        Post: none
        """

        self.cables = None
        for house in self.connected_homes:
            house.remove_cables()

    def move_to(self, x: int, y: int) -> None:
        """
        Moves the battery to position x,y
        
        Pre : x and y are integers
        Post: x and y are stored in attributes coord_x and coord_y respectively
        """

        self.coord_x = x
        self.coord_y = y

    def get_coords(self) -> tuple[int, int]:
        """
        Gets coordinates of battery:
        
        Pre : none
        Post: tuple with two integers
        """
        
        return (self.coord_x, self.coord_y)

    def connect_home_without_load(self, house: House) -> None:
        """
        Connects a house to the battery.
        
        Pre : house of class House
        Post: none
        """
        
        self.connected_homes.append(house)
        house.make_connection(self)

    def disconnect_all_houses(self) -> None:
        """
        Disconnects all houses from battery.
        
        Pre : none
        Post: none
        """
        
        for house in self.connected_homes:
            house.delete_connection()
        self.connected_homes = []
        self.current_capacity = self.total_capacity
