from typing import Optional

class House:
    """
    Class that contains all information for a house, such as
    maxoutput, connection to a battery and the coordinates.
    """
    
    def __init__(self, x: int, y: int, maxoutput: float) -> None:
        self.coord_x: int = x
        self.coord_y: int = y
        self.maxoutput: float = maxoutput

        # ! attribute same name as method
        self.has_connection: bool = False
        self.connection: Optional[object] = None
        self.cables: list[str] = []

    def make_connection(self, battery: object) -> None:
        """
        This method connects a house to a battery if it is not already
        connected. 
        
        Pre : battery of class Battery
        Post: none
        """
        # ! Moet er niet een error worden geraised als er al een connectie is?
        if self.has_connection is False:
            self.has_connection = True
            self.connection = battery

    def delete_connection(self) -> None:
        """
        Deletes connection with a battery.
        
        Pre : none
        Post: none
        """
        self.has_connection = False
        self.connection = None

    def distance_to_battery(self) -> int:
        """
        Calculates the distance to the connected battery.
        
        Pre : none
        Post: returns distance as integer
        """
        if self.has_connection:
            # calculates distance vertically and horizontally
            dist_x: int = abs(self.coord_x - self.connection.coord_x)
            dist_y: int = abs(self.coord_y - self.connection.coord_y)
            
            return dist_x + dist_y

    def distance_to_any_battery(self, battery: object) -> int:
        """
        Calculates distance between house and any battery object.
        
        Pre : battery of class Battery
        Post: returns an int
        """
        # calculates distance vertically and horizontally
        dist_x: int = abs(self.coord_x - battery.coord_x)
        dist_y: int = abs(self.coord_y - battery.coord_y)
        distance: int = dist_x + dist_y

        return distance
    
    def lay_cables(self) -> None:
        """
        Puts all cables in list for the smallest distance.
        
        Pre : none
        Post: none
        """
        # makes sure no cables will be layed if house has no connection
        if self.has_connection is False:
            return

        # gets coordinates
        start_coords: tuple(int, int) = self.coord_x, self.coord_y
        end_x, end_y = self.connection.coord_x, self.connection.coord_y

        # calculates distance vertically and horizontally
        dist_x: int = abs(start_coords[0] - end_x)
        dist_y: int = abs(start_coords[1] - end_y)

        y_direction: int = self.get_axis_direction(start_coords[1], end_y)

        # adds all cables along the y-axis
        for new_y in range(dist_y + 1):
            new_cable: str = f"{start_coords[0]},{start_coords[1] + new_y * y_direction}"
            self.cables.append(new_cable)

        x_direction: int = self.get_axis_direction(start_coords[0], end_x)

        # adds all cables along the x-axis
        for new_x in range(1, dist_x + 1):
            new_cable: str = f"{start_coords[0] + new_x * x_direction},{end_y}"
            self.cables.append(new_cable)

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

    def remove_cables(self) -> None:
        """
        Removes all cables.
        
        Pre : none
        Post: none
        """

        # makes list of cables empty
        self.cables = []

    def set_cables(self, cables: list[str]) -> None:
        """
        Sets the cables of the house to the given cables.
        
        Pre: cables argument is a list of strings, where the strings are in the
             shape of 'x,y'
        Post: the cables attribute is set to the cables argument
        """

        self.cables = cables
