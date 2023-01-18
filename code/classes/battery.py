from .house import House

class Battery:
    def __init__(self, x: int, y: int, capacity: float):
        self.coord_x = x
        self.coord_y = y
        self.total_capacity = capacity
        self.current_capacity = capacity

        self.connected_homes: list[House] = []

    def connect_home(self, house: House) -> None:
        """
        Haalt van de totale capaciteit, de output af van een specifieke huis
        als er nog capaciteit is. Ook zet deze methode een aangesloten huis
        in de lijst van de battery.
        """
        if self.current_capacity - house.maxoutput >= 0:
            self.current_capacity = self.current_capacity - house.maxoutput
            self.connected_homes.append(house)

    def disconnect_home(self, house: House) -> None:
        """
        Deze methode haalt de connectie van een huis weg en past de huidige
        capaciteit van een huis aan wanneer een huis is aangesloten.
        """
        if house in self.connected_homes:
            self.current_capacity = self.current_capacity + house.maxoutput
            self.connected_homes.remove(house)

    def get_capacity(self) -> float:
        """
        Verkrijgt de huidige capaciteit van de batterij.
        """
        return self.current_capacity

    def is_connection_possible(self, house: House) -> bool:
        """
        Deze methode checkt of er nog genoeg capaciteit
        is om een huis aan te sluiten.
        """
        return self.current_capacity - house.maxoutput >= 0

    def lay_shared_cables(self):
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
        cable_x, cable_y = [int(coord) for coord in cable.split(",")]

        distance = abs(house.coord_x - cable_x) + abs(house.coord_y - cable_y)

        return distance

