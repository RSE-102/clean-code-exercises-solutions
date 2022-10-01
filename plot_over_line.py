from typing import Tuple, List, Callable
from math import nan, sqrt, sin, cos, pi
from matplotlib.pyplot import plot, show, close

from raster_grid import RasterGrid, Point


DataArray = List[List[float]]
PlotOverLineData = Tuple[List[float], List[float]]


class RasterFunction:
    def __init__(self,
                 raster: RasterGrid,
                 values: DataArray) -> None:
        self._raster = raster
        self._values = values

    def __call__(self, point: Point) -> float:
        cell = self._raster.locate(point)
        return self._values[cell.col_index][cell.row_index] if cell else nan


class PlotOverLine:
    def __init__(self,
                 source: Point,
                 target: Point,
                 num_samples: int = 1000) -> None:
        self._source = source
        self._num_samples = num_samples
        self._step = (
            (target.x - source.x)/(num_samples - 1),
            (target.y - source.y)/(num_samples - 1)
        )

    def make_plot_data(self, function: Callable[[Point], float]) -> PlotOverLineData:
        x_values, y_values = [], []
        for i in range(self._num_samples):
            position = Point(
                self._source.x + self._step[0]*i,
                self._source.y + self._step[1]*i
            )
            x_values.append(self._distance(position))
            y_values.append(function(position))
        return x_values, y_values

    def _distance(self, position: Point) -> float:
        dx = position.x - self._source.x
        dy = position.y - self._source.y
        return sqrt(dx*dx + dy*dy)


def plot_over_line(function: Callable[[Point], float],
                   source: Point,
                   target: Point,
                   number_of_samples: int = 1000) -> None:
    pol = PlotOverLine(source, target, number_of_samples)
    x, y = pol.make_plot_data(function)
    plot(x, y)
    show()
    close()


def _get_discrete_values(grid: RasterGrid) -> DataArray:
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
