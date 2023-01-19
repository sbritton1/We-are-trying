from typing import Optional

class House:
    def __init__(self, x: int, y: int, maxoutput: float) -> None:
        self.coord_x = x
        self.coord_y = y
        self.maxoutput = maxoutput

        # ! attribute same name as method
        self.has_connection: bool = False
        self.connection: Optional[object] = None
        self.cables: list[str] = []

    def has_connection(self) -> bool:
        """
        Checkt of een huis een connectie heeft met een batterij.
        Returnt true of false.
        """
        return self.has_connection

    def make_connection(self, battery: object) -> None:
        """
        This method connects a house to a battery if it is not already
        connected. 
        
        Pre: battery of class Battery
        Post: none
        """
        # ! Moet er niet een error worden geraised als er al een connectie is?
        if self.has_connection is False:
            self.has_connection = True
            self.connection: object = battery

    def delete_connection(self) -> None:
        """
        Deletes connection with a battery.
        
        Pre: none
        Post: none
        """
        # ! Deze check is niet echt nodig
        if self.has_connection is True:
            self.has_connection = False
            self.connection = None

    def distance_to_battery(self) -> int:
        """
        Calculates the distance to the connected battery.
        
        Pre: none
        Post: returns distance as integer
        """
        if self.has_connection:
            dist_x = abs(self.coord_x - self.connection.coord_x)
            dist_y = abs(self.coord_y - self.connection.coord_y)
            
            return dist_x + dist_y

    def distance_to_any_battery(self, battery: object) -> int:
        """
        Calculates distance between house and any battery object
        
        Pre: battery of class Battery
        Post: returns an int
        """
        # ! Sommige type hints zijn al implied
        dist_x: int = abs(self.coord_x - battery.coord_x)
        dist_y: int = abs(self.coord_y - battery.coord_y)
        distance: int = dist_x + dist_y

        return distance
    
    def lay_cables(self) -> None:
        """
        Puts all cables in list for the smallest distance
        
        Pre: none
        Post: none
        """

        if self.has_connection is False:
            return

        start_x, start_y = self.coord_x, self.coord_y
        end_x, end_y = self.connection.coord_x, self.connection.coord_y

        dist_x = abs(start_x - end_x)
        dist_y = abs(start_y - end_y)

        y_direction = self.get_axis_direction(start_y, end_y)

        # voegt alle kabels toe langs de y-as
        for new_y in range(dist_y + 1):
            new_cable = f"{start_x},{start_y + new_y * y_direction}"
            self.cables.append(new_cable)

        x_direction = self.get_axis_direction(start_x, end_x)

        # voegt alle kabels toe langs de x-as
        for new_x in range(1, dist_x + 1):
            new_cable = f"{start_x + new_x * x_direction},{end_y}"
            self.cables.append(new_cable)

    def get_axis_direction(self, start, end) -> int:
        """
        Returns 1 if the connection is in the negative axis direction and 1 if
        in the positive direction.
        
        Pre: a start and end coordinate as integer
        Post: returns direction as integer
        """

        if end - start < 0:
            return -1
        return 1

    def remove_cables(self):
        self.cables = []

    def set_cables(self, cables: list[str]) -> None:
        """
        Sets the cables of the house to the given cables.
        
        Pre: cables argument is a list of strings, where the strings are in the
            shape of 'x,y'
        Post: the cables attribute is set to the cables argument"""

        self.cables = cables
