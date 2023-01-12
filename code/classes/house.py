class House:
    def __init__(self, x: int, y: int, maxoutput: float):
        self.coord_x = x
        self.coord_y = y
        self.maxoutput = maxoutput

        self.has_connection: bool = False
        self.connection: object = None
        self.cables: list[str] = []

    def has_connection(self) -> bool:
        """
        Checkt of een huis een connectie heeft met een batterij.
        Returnt true of false.
        """
        return self.has_connection

    def make_connection(self, battery: object) -> None:
        """
        Deze methode zorgt er voor dat een huis een connectie
        heeft met een bepaalde batterij, wanneer een huis nog geen
        connectie heeft. Deze methode zorgt er ook voor dat alle
        kabels worden gelegd naar de batterij.
        """
        if self.has_connection is False:
            self.has_connection = True
            self.connection = battery
            self.lay_cables()

    def delete_connection(self) -> None:
        """
        Verwijdert een connectie met een batterij, waardoor er geen
        connectie meer is.
        """
        if self.has_connection is True:
            self.has_connection = False
            self.connection = None

    def distance_to_battery(self) -> int:
        """
        Berekent wanneer een huis is aangesloten aan een batterij
        wat de afstand tussen de batterij en het huis is.
        """
        if self.has_connection:
            dist_x = abs(self.coord_x - self.connection.coord_x)
            dist_y = abs(self.coord_y - self.connection.coord_y)
            distance = dist_x + dist_y
            return distance

    def lay_cables(self) -> None:
        """
        Zet alle kabels in een lijst, op basis van de kortste afstand.
        """
        dist_x = abs(self.coord_x - self.connection.coord_x)
        dist_y = abs(self.coord_y - self.connection.coord_y)

        non_abs_dist_y = self.coord_y - self.connection.coord_y

        # voegt alle kabels toe langs de y-as
        for new_y in range(dist_y + 1):
            if self.coord_y - self.connection.coord_y > 0:
                new_cable = f"{self.coord_x},{self.coord_y - new_y}"
                self.cables.append(new_cable)
            else:
                new_cable = f"{self.coord_x},{self.coord_y + new_y}"
                self.cables.append(new_cable)

        # dit is de y-waarde waar de kabels langs de x-as gelegd moeten worden
        last_y_value = self.coord_y - non_abs_dist_y

        # voegt alle kabels toe langs de x-as
        for new_x in range(dist_x + 1):
            if self.coord_x - self.connection.coord_x > 0:
                new_cable = f"{self.coord_x - new_x},{last_y_value}"
                self.cables.append(new_cable)
            else:
                new_cable = f"{self.coord_x + new_x},{last_y_value}"
