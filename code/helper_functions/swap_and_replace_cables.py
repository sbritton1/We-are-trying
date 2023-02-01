from ..classes.house import House
from .swap_houses import swap_houses


def swap_and_replace_cables(target1: House, target2: House) -> None:
    """
    Swaps two houses and re-lays the cables for those batteries.

    Pre : target1 and target2 are of class House
    Post: houses swapped batteries and the new cables are placed
    """

    # disconnect cables as they are now
    target1.connection.remove_cables()
    target2.connection.remove_cables()

    swap_houses(target1, target2)

    # reconnect cables with houses swapped
    target1.connection.lay_shared_cables()
    target2.connection.lay_shared_cables()
