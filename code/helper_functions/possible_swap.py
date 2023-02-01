from ..classes.house import House


def possible_swap(house1: House, house2: House) -> bool:
    """
    Checks if it is possible to swap two houses based on the
    remaining capacity of their batteries.

    Pre : house1 and house2 are of class House
    Post: returns True if houses can be swapped
          else returns False
    """

    # swapping housees with the same battery is pointless
    if house1.connection == house2.connection:
        return False

    avail_capacity1 = house2.maxoutput + house2.connection.current_capacity
    avail_capacity2 = house1.maxoutput + house1.connection.current_capacity

    # return false when a battery doesn't have the required available capacity
    if house1.maxoutput > avail_capacity1:
        return False
    elif house2.maxoutput > avail_capacity2:
        return False

    return True
