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


class Line:
    def __init__(self, source: Point, target: Point) -> None:
        self._points = (source, target)

    @property
    def source(self) -> Point:
        return self._points[0]

    @property
    def target(self) -> Point:
        return self._points[1]


def discretize(line: Line, number_of_samples: int) -> List[Point]:
    step = (
        (line.target.x - line.source.x)/(number_of_samples - 1),
        (line.target.y - line.source.y)/(number_of_samples - 1)
    )
    return [
        Point(
            line.source.x + step[0]*float(i),
            line.source.y + step[1]*float(i)
        ) for i in range(number_of_samples)
    ]


def distance(p0: Point, p1: Point) -> float:
    dx = p1.x - p0.x
    dy = p1.y - p0.y
    return sqrt(dx*dx + dy*dy)


def plot_over_line(function: Callable[[Point], float],
                   line: Line,
                   number_of_samples: int = 1000) -> None:
    points = discretize(line, number_of_samples)
    x = [distance(points[0], p) for p in points]
    y = [function(p) for p in points]
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
        line=Line(
            Point(0.0, 0.0),
            Point(1.0, 1.0)
        ),
        number_of_samples=2000
    )
