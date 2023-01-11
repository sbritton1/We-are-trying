class House:
    def __init__(self, x: int, y: int, maxoutput: float):
        self.coord_x = x
        self.coord_y = y
        self.maxoutput = maxoutput

        self.has_connection: bool = False

        self.connection: object = None

    def has_connection(self) -> bool:
        """
        checkt of een huis een connectie heeft met een batterij
        """
        return self.has_connection

    def make_connection(self, battery: object) -> None:
        """
        Deze methode zorgt er voor dat een huis een connectie 
        heeft met een bepaalde batterij
        """
        if self.has_connection is False:
            self.has_connection = True
            self.connection = battery  

    def delete_connection(self) -> None:
        """
        verwijdert een connectie met een batterij, waardoor er geen
        connectie meer is.
        """
        if self.has_connection is True:
            self.has_connection = False
            self.connection = None 

    def distance_to_battery(self) -> float:
        """
        berekent wanneer aangesloten wat de afstand tussen de batterij en het huis is
        """
        if self.has_connection:
            distance = abs(self.coord_x - self.connection.coord_x) + abs(self.coord_y - self.connection.coord_y)
            return distance
