from ..classes.house import House


def possible_swap(house1: House, house2: House) -> bool:
    """
    Checks if it is possible to swap two houses based on the
    remaining capacity of their batteries.

    Pre : house1 and house2 are of class House
    Post: returns True if houses can be swapped
          else returns False
    """

    if house1.connection == house2.connection:
        return False

    if house1.maxoutput > house2.maxoutput + house2.connection.current_capacity:
        return False

    elif house2.maxoutput > house1.maxoutput + house1.connection.current_capacity:
        return False

    return True
