from typing import Tuple, Iterable, Optional
from dataclasses import dataclass
from math import isclose

@dataclass
class Point:
    x: float
    y: float

Resolution = Tuple[int, int]

class RasterGrid:
    @dataclass
    class Cell:
        col_index: int
        row_index: int

    def __init__(self,
                 lower_left: Point,
                 size: Tuple[float, float],
                 resolution: Resolution) -> None:
        self._lower_left = lower_left
        self._size = size
        self._resolution = resolution
        self._dx = (
            size[0]/float(resolution[0]),
            size[1]/float(resolution[1])
        )

    @property
    def resolution(self) -> Resolution:
        return self._resolution

    @property
    def number_of_cells(self) -> int:
        return self._resolution[0]*self._resolution[1]

    @property
    def cells(self) -> Iterable[Cell]:
        return (
            self.Cell(i, j)
            for i in range(self._resolution[0])
            for j in range(self._resolution[1])
        )

    def center(self, cell: Cell) -> Point:
        return Point(
            self._lower_left.x + (float(cell.col_index) + 0.5)*self._dx[0],
            self._lower_left.y + (float(cell.row_index) + 0.5)*self._dx[1]
        )

    def locate(self, point: Point) -> Optional[Cell]:
        tolerance = 1e-6*max(self._dx[0], self._dx[1])
        ix = self._get_x_index(point, tolerance)
        iy = self._get_y_index(point, tolerance)
        if ix < 0 or ix >= self._resolution[0]:
            return None
        if iy < 0 and iy >= self._resolution[1]:
            return None
        return self.Cell(ix, iy)

    def _get_x_index(self, point: Point, tolerance: float) -> int:
        x_min = self._lower_left.x
        x_max = self._lower_left.x + self._size[0]
        if abs(point.x - x_min) < tolerance:
            return 0
        elif abs(point.x - x_max) < tolerance:
            return self._resolution[0] - 1
        return int((point.x - x_min)/self._dx[0])

    def _get_y_index(self, point: Point, tolerance: float) -> int:
        y_min = self._lower_left.y
        y_max = self._lower_left.y + self._size[1]
        if abs(point.y - y_min) < tolerance:
            return 0
        elif abs(point.y - y_max) < tolerance:
            return self._resolution[1] - 1
        return int((point.y - y_min)/self._dx[1])


def test_number_of_cells() -> None:
    p0 = Point(0.0, 0.0)
    dx = 1.0
    dy = 1.0
    assert RasterGrid(p0, (dx, dy), (10, 10)).number_of_cells == 100
    assert RasterGrid(p0, (dx, dy), (10, 20)).number_of_cells == 200
    assert RasterGrid(p0, (dx, dy), (20, 10)).number_of_cells == 200
    assert RasterGrid(p0, (dx, dy), (20, 20)).number_of_cells == 400


def test_locate_cell() -> None:
    grid = RasterGrid(
        lower_left=Point(0.0, 0.0),
        size=(2.0, 2.0),
        resolution=(2, 2)
    )
    cell = grid.locate(Point(0, 0))
    assert cell and cell.col_index == 0 and cell.row_index == 0
    cell = grid.locate(Point(1, 1))
    assert cell and cell.col_index == 1 and cell.row_index == 1
    cell = grid.locate(Point(0.5, 0.5))
    assert cell and cell.col_index == 0 and cell.row_index == 0
    cell = grid.locate(Point(1.5, 0.5))
    assert cell and cell.col_index == 1 and cell.row_index == 0
    cell = grid.locate(Point(0.5, 1.5))
    assert cell and cell.col_index == 0 and cell.row_index == 1
    cell = grid.locate(Point(1.5, 1.5))
    assert cell and cell.col_index == 1 and cell.row_index == 1


def test_cell_iterator() -> None:
    grid = RasterGrid(
        lower_left=Point(0.0, 0.0),
        size=(2.0, 2.0),
        resolution=(2, 2)
    )
    count = sum(1 for _ in grid.cells)
    assert count == grid.number_of_cells

    cell_indices_without_duplicates = set(list(
        (cell.col_index, cell.row_index) for cell in grid.cells
    ))
    assert len(cell_indices_without_duplicates) == count


def test_cell_center():
    grid = RasterGrid(
        lower_left=Point(0.0, 0.0),
        size=(2.0, 2.0),
        resolution=(2, 2)
    )
    cell = grid.locate(Point(0.5, 0.5))
    assert cell and _is_equal(grid.center(cell), Point(0.5, 0.5))
    cell = grid.locate(Point(1.5, 0.5))
    assert cell and _is_equal(grid.center(cell), Point(1.5, 0.5))
    cell = grid.locate(Point(0.5, 1.5))
    assert cell and _is_equal(grid.center(cell), Point(0.5, 1.5))
    cell = grid.locate(Point(1.5, 1.5))
    assert cell and _is_equal(grid.center(cell), Point(1.5, 1.5))


def _is_equal(p0: Point, p1: Point) -> bool:
    return isclose(p0.x, p1.x) and isclose(p0.y, p1.y)
