class Battery:
    def __init__(self, x: int, y: int, capacity: float):
        self.coord_x = x
        self.coord_y = y
        self.total_capacity = capacity
        self.current_capacity = capacity

        self.connected_homes: list[tuple(int, int, float)] = [] 

    def connect_homes(self, x_house: int, y_house: int, output_house: float) -> None:
        """
        Haalt van de totale capaciteit, de output af van een specifieke huis
        als er nog capaciteit is. Ook zet deze methode een aangesloten huis
        in de lijst van de battery
        """
        if self.current_capacity - output_house >= 0:
            self.current_capacity = self.current_capacity - output_house
            new_house = (x_house, y_house, output_house)
            self.connected_homes.append(new_house)


    def disconnect_homes(self, x_house: int, y_house: int, output_house: float) -> None:
        """
        Deze methode haalt de connectie van een huis weg, en past de capaciteit aan, 
        wanneer een huis is aangesloten
        """
        house = (x_house, y_house, output_house)
        if house in self.connected_homes:
            self.current_capacity = self.current_capacity + output_house
            for i in self.connected_homes:
                if self.connected_homes[i] == house:
                    self.connected_homes[i] = 0
                    break

    def get_capacity(self) -> float:
        """
        Verkrijgt de capaciteit van de batterij
        """
        return self.current_capacity