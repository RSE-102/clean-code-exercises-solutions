# In this "solution", we have changed the names of the function
# of `RasterGrid` to be more expressive. Moreover, we have computed
# the discretization length of a single cell in the constructor in
# order to not have to recompute that everytime in `cell_center`
# (in the original exercise just called `c`).

# We have also collected the arguments of the constructor into
# data structures such that the total number of arguments is reduced
# and can be type-checked, as each argument is of a different type.
# That is, a point, a tuple of floats and a tuple of ints for the
# origin, the size and the resolution. In the tests, we have created
# helper functions in order to improve the readability.
#
# Another thing we did here was to not save the cells as one long list
# in `RasterGrid`. Since the grid is fully structured, we can easily
# construct the cells when they are requested, which saves us from
# unneccesary memory overhead for very large rasters. Therefore, we
# made `cells` a property that returns a generator expression -> something
# that is iterable and each iterate is a cell. This does lazy evaluation,
# which means that when the user calls `cells` on a raster, a lightweight
# object is returned, which constructs a new cell upon iteration. This way
# we don't have to store a large list of cells but construct them on-the-fly
# when users iterate through them.

from typing import Tuple, Iterable
from math import isclose
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


class RasterGrid:
    @dataclass
    class Cell:
        _ix: int
        _iy: int

    def __init__(self,
                 origin: Point,
                 size: Tuple[float, float],
                 resolution: Tuple[int, int]) -> None:
        self._origin = origin
        self._resolution = resolution
        self._dx = size[0]/float(resolution[0])
        self._dy = size[1]/float(resolution[1])

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

    def cell_center(self, cell: Cell) -> Point:
        return Point(
            self._origin.x + (float(cell._ix) + 0.5)*self._dx,
            self._origin.y + (float(cell._iy) + 0.5)*self._dy
        )


def test_number_of_cells():
    def _make_grid(resolution: Tuple[int, int]) -> RasterGrid:
        return RasterGrid(Point(0., 0.), (1., 1.), resolution)

    assert _make_grid((10, 10)).number_of_cells == 100
    assert _make_grid((10, 20)).number_of_cells == 200
    assert _make_grid((20, 10)).number_of_cells == 200
    assert _make_grid((20, 20)).number_of_cells == 400


def test_cell_center():
    grid = RasterGrid(Point(0.0, 0.0), (2.0, 2.0), (2, 2))
    expected_centers = [
        Point(0.5, 0.5),
        Point(1.5, 0.5),
        Point(0.5, 1.5),
        Point(1.5, 1.5)
    ]

    def _is_equal(p0: Point, p1: Point) -> bool:
        return isclose(p0.x, p1.x) and isclose(p0.y, p1.y)

    for cell in grid.cells:
        for center in expected_centers:
            if _is_equal(center, grid.cell_center(cell)):
                expected_centers.remove(center)

    assert len(expected_centers) == 0


if __name__ == "__main__":
    test_number_of_cells()
    test_cell_center()
    print("All tests passed")
