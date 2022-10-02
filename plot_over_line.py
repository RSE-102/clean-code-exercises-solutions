from typing import Tuple, List, Callable
from math import nan, sqrt, sin, cos, pi
from matplotlib.pyplot import plot, show, close

from raster_grid import RasterGrid, Point


class RasterFunction:
    def __init__(self,
                 raster: RasterGrid,
                 values: List[List[float]]) -> None:
        self._raster = raster
        self._values = values

    def __call__(self, point: Point) -> float:
        cell = self._raster.locate(point)
        return self._values[cell.col_index][cell.row_index] if cell else nan


def discretize(function: Callable[[Point], float],
               source: Point,
               target: Point,
               num_samples: int = 1000) -> Tuple[List[float], List[float]]:
    step = (
        (target.x - source.x)/(num_samples - 1),
        (target.y - source.y)/(num_samples - 1)
    )
    x_values, y_values = [], []
    for i in range(num_samples):
        dx, dy = step[0]*float(i), step[1]*float(i)
        position = Point(source.x + dx, source.y + dy)
        x_values.append(sqrt(dx*dx + dy*dy))
        y_values.append(function(position))
    return x_values, y_values


def plot_over_line(function: Callable[[Point], float],
                   source: Point,
                   target: Point,
                   number_of_samples: int = 1000) -> None:
    x, y = discretize(function, source, target, number_of_samples)
    plot(x, y)
    show()
    close()


def _get_discrete_values(grid: RasterGrid) -> List[List[float]]:
    def function(p: Point):
        return sin(2.0*pi*p.x)*cos(2.0*pi*p.y)
    discrete_values = [
        [0.0 for _ in range(grid.resolution[0])]
        for _ in range(grid.resolution[1])
    ]
    for cell in grid.cells:
        discrete_values[cell.col_index][cell.row_index] = function(grid.center(cell))
    return discrete_values


if __name__ == "__main__":
    grid = RasterGrid(
        Point(0.0, 0.0),
        size=(1.0, 1.0),
        resolution=(100, 100)
    )
    values = _get_discrete_values(grid)
    raster_function = RasterFunction(grid, values)
    plot_over_line(
        function=raster_function,
        source=Point(0.0, 0.0),
        target=Point(1.0, 1.0),
        number_of_samples=2000
    )
