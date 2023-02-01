import sys

from code.visualization.convert_from_JSON import convert_from_JSON
from code.visualization.visualization import visualize
from code.classes.grid import Grid


def visualize_json(filepath: str) -> None:
    """
    Visualizes the grid stored in a JSON file.

    pre : filepath is a string
    post: visualization of json shown as matplotlib plot
    """

    # load the grid from JSON
    grid: Grid = convert_from_JSON(filepath)

    # visualize the grid
    visualize(grid)


if __name__ == "__main__":
    # take first command-line argument as filepath
    filepath: str = sys.argv[1]

    # call 'main' function
    visualize_json(filepath)
