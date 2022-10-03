from typing import Tuple, Iterable, Callable, Protocol
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class Point:
    x: float
    y: float


class Lattice(Protocol):
    def points(self) -> Iterable[Point]:
        ...


class SquareLattice:
    def __init__(self,
                 lower_left: Point,
                 size: Tuple[float, float],
                 resolution: Tuple[int, int]) -> None:
        self._lower_left = lower_left
        self._size = size
        self._resolution = resolution

    def points(self) -> Iterable[Point]:
        dx = (
            self._size[0]/self._resolution[0],
            self._size[1]/self._resolution[1]
        )
        return (
            Point(
                self._lower_left.x + (float(i) + 0.5)*dx[0],
                self._lower_left.y + (float(j) + 0.5)*dx[1]
            )
            for j in range(self._resolution[1])
            for i in range(self._resolution[0])
        )


class FieldPlot:
    def __init__(self,
                 discretization: SquareLattice,
                 field: Callable[[Point], float]) -> None:
        x, y, z = [], [], []
        for p in discretization.points():
            x.append(p.x)
            y.append(p.y)
            z.append(field(p))
        self._figure = plt.figure("FieldPlot")
        ax = self._figure.add_subplot(projection='3d')
        img = ax.scatter(x, y, z)
        self._figure.colorbar(img)

    def show(self) -> None:
        plt.figure("FieldPlot")
        plt.show()


# The field function is nan at several places, so we wrap
# it in this concrete field plot class that only takes a
# resolution parameter, since the boundaries are given by
# the coordinates at which the field is not defined
class MyFieldPlot:
    def __init__(self, resolution: Tuple[int, int]) -> None:
        point_cloud = SquareLattice(
            lower_left=Point(1.0, 1.0),
            size=(4.0, 4.0),
            resolution=resolution
        )
        self._field_plot = FieldPlot(point_cloud, self._evaluate_field)

    def show(self) -> None:
        self._field_plot.show()

    def _evaluate_field(self, point: Point) -> float:
        x, y = point.x, point.y
        return 1.0/((1.0 - x)*(5.0 - x)) + 1.0/((1.0 - y)*(5.0 - y))


if __name__ == "__main__":
    plot = MyFieldPlot(
        resolution=(25, 25)
    )
    plot.show()

