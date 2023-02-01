from ..classes.house import House
from ..classes.battery import Battery
from .possible_swap import possible_swap


def swap_houses(house1: House, house2: House) -> bool:
    """
    Swaps the battery of two houses.

    Pre : house1 and house2 are of class House
    Post: battery connection of two houses are swapped and returns True,
          returns False if a swap isn't possible
    """

    if possible_swap(house1, house2) is False:
        return False

    house1_bat: Battery = house1.connection
    house2_bat: Battery = house2.connection

    # disconnect established connections
    house1_bat.disconnect_home(house1)
    house1.delete_connection()
    house2_bat.disconnect_home(house2)
    house2.delete_connection()

    # make new connections
    house1_bat.connect_home(house2)
    house2.make_connection(house1_bat)
    house2_bat.connect_home(house1)
    house1.make_connection(house2_bat)

    return True
