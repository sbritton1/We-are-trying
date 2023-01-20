from .house import House

class Battery:
    """
    Class that contains all information for batteries, such as
    its capacity, all the houses that are connected to the
    battery and its coordinates.
    """
    
    def __init__(self, x: int, y: int, capacity: float):
        self.coord_x = x
        self.coord_y = y
        self.total_capacity = capacity
        self.current_capacity = capacity

        self.connected_homes: list[House] = []

    def connect_home(self, house: House) -> None:
        """
        Connects house to battery and also substracts output from capacity.
        
        Pre: house from the house class
        Post: none
        """
        if self.current_capacity - house.maxoutput >= 0:
            self.current_capacity = self.current_capacity - house.maxoutput
            self.connected_homes.append(house)

    def disconnect_home(self, house: House) -> None:
        """
        Disconnects house from battery and also removes output of house.
        
        Pre: house from the house class
        Post: none
        """
        if house in self.connected_homes:
            self.current_capacity = self.current_capacity + house.maxoutput
            self.connected_homes.remove(house)

    def get_capacity(self) -> float:
        """
        Gets current capacity from battery.
        
        Pre: none
        Post: capacity as float
        """
        return self.current_capacity

    def is_connection_possible(self, house: House) -> bool:
        """
        Check if house does not overflow capacity of battery.
        
        Pre: house from house class
        Post: bool    
        """
        return self.current_capacity - house.maxoutput >= 0

    def lay_shared_cables(self):
        """
        Lays shared cables in grid.
        
        Pre: none
        Post: none
        """
        battery_cable = f"{self.coord_x},{self.coord_y}"
        self.cables: set[str] = {battery_cable}

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

                    # later iterate on trying different configurations when two houses
                    # have the same distance, this can lead to different results

                    if distance < min_dist:
                        min_dist = distance
                        min_house = house
                        min_cable = cable
                        loc_in_list = loc

            house_cable = f"{min_house.coord_x},{min_house.coord_y}"
            min_house.cables.append(house_cable)
            self.cables.add(house_cable)

            min_cable_x, min_cable_y = [int(coord) for coord in min_cable.split(",")]

            dir_y = 1
            if min_house.coord_y - min_cable_y > 0:
                dir_y = -1

            for new_y in range(min_house.coord_y, min_cable_y, dir_y):
                new_cable = f"{min_house.coord_x},{new_y + dir_y}"
                min_house.cables.append(new_cable)
                self.cables.add(new_cable)

            dir_x = 1
            if min_house.coord_x - min_cable_x > 0:
                dir_x = -1

            for new_x in range(min_house.coord_x, min_cable_x, dir_x):
                new_cable = f"{new_x + dir_x},{min_cable_y}"
                min_house.cables.append(new_cable)
                self.cables.add(new_cable)

            unconnected.remove(loc_in_list)

    def calc_distance(self, house: House, cable: str) -> int:
        """
        Calculates the distance between a house and a cable.
        
        Pre: house from the house class and a cable as a string
        Post: distance as integer
        """
        cable_x, cable_y = [int(coord) for coord in cable.split(",")]

        distance = abs(house.coord_x - cable_x) + abs(house.coord_y - cable_y)

        return distance

    def remove_cables(self) -> None:
        """
        Removes connected cables from grid.
        
        Pre: none
        Post: none
        """
        self.cables = None
        for house in self.connected_homes:
            house.remove_cables()
