class Battery:
    def __init__(self, x: int, y: int, capacity: float):
        self.coord_x = x
        self.coord_y = y
        self.total_capacity = capacity
        self.current_capacity = capacity

        self.connected_homes: list[object] = [] 

    def connect_home(self, house: object) -> None:
        """
        Haalt van de totale capaciteit, de output af van een specifieke huis
        als er nog capaciteit is. Ook zet deze methode een aangesloten huis
        in de lijst van de battery
        """
        if self.current_capacity - house.maxoutput >= 0:
            self.current_capacity = self.current_capacity - house.maxoutput
            self.connected_homes.append(house)


    def disconnect_home(self, house: object) -> None:
        """
        Deze methode haalt de connectie van een huis weg, en past de capaciteit aan, 
        wanneer een huis is aangesloten
        """

        if house in self.connected_homes:
            self.current_capacity = self.current_capacity + house.maxoutput
            self.connected_homes.remove(house)

    def get_capacity(self) -> float:
        """
        Verkrijgt de capaciteit van de batterij
        """
        return self.current_capacity

    def is_connection_possible(self, house: object) -> bool:
        if self.current_capacity - house.maxoutput >= 0:
            return True
        else:
            return False
