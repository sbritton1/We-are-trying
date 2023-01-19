import sys

from code.visualization.convert_from_JSON import convert_from_JSON
from code.visualization.visualization import visualize


def visualize_json(filepath: str) -> None:
    """
    Visualizes the grid stored in a JSON file
    """

    # load the grid from JSON
    grid = convert_from_JSON(filepath)

    # visualize the grid
    visualize(grid)


if __name__ == "__main__":
    # take first command-line argument as filepath
    filepath = sys.argv[1]

    # call 'main' function
    visualize_json(filepath)
