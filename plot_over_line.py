# In this "solution", we reduced the number of arguments to
# `plot_over_line` by combining the point cloud and the associated
# discrete values into a `DiscreteFunction`, which allows for evaluation
# at a given point via the __call__ operator. This has the benefit that
# now the decision on how to evaluate the discrete function is now in here
# and `plot_over_line` does not have to know about this.
#
# We also combined the start/end points of the line into a separate class `Line`,
# which furthermore allows to get the points along a line for a given local coordinate
# along the line between 0 and 1.
#
# Finally, we split the plot data generation from the actual plotting to make
# it reusable in different contexts.

from __future__ import annotations
from typing import List, Tuple
from dataclasses import dataclass
from math import pi, sqrt, sin, cos
from matplotlib.pyplot import plot, show, close


@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return sqrt(dx*dx + dy*dy)


class PointCloud:
    def __init__(self, points: List[Point]) -> None:
        self._points = points

    @property
    def size(self) -> int:
        return len(self._points)

    # This is to make a `PointCloud` iterable, that is, to
    # allow looping over its points like this:
    #
    # for p in point_cloud:
    #     ...
    def __iter__(self):
        return iter(self._points)

    def __getitem__(self, index: int) -> Point:
        return self._points[index]

    def get_nearest(self, p: Point) -> Point:
        return min(self._points, key=lambda point: point.distance_to(p))

    def get_nearest_point_index(self, p: Point) -> int:
        return self._points.index(self.get_nearest(p))


class DiscreteFunction:
    def __init__(self, point_cloud: PointCloud, point_values: List[float]) -> None:
        self._point_cloud = point_cloud
        self._point_values = point_values

    def __call__(self, point: Point) -> float:
        return self._point_values[
            self._point_cloud.get_nearest_point_index(point)
        ]


class Line:
    def __init__(self, source: Point, target: Point) -> None:
        self._source = source
        self._target = target
        self._vector = (
            target.x - source.x,
            target.y - source.y
        )

    @property
    def source(self) -> Point:
        return self._source

    @property
    def target(self) -> Point:
        return self._target

    def at(self, fraction: float) -> Point:
        assert fraction >= 0.0 and fraction <= 1.0
        return Point(
            self._source.x + fraction*self._vector[0],
            self._source.y + fraction*self._vector[1]
        )


def make_plot_data(function: DiscreteFunction,
                   line: Line,
                   number_of_samples: int = 1000) -> Tuple[List[float], List[float]]:
    x = []
    y = []
    step_fraction = 1.0/(number_of_samples - 1)
    for i in range(number_of_samples):
        current = line.at(float(i)*step_fraction)
        x.append(line.source.distance_to(current))
        y.append(function(current))
    return x, y


def plot_over_line(function: DiscreteFunction,
                   line: Line,
                   number_of_samples: int = 1000) -> None:
    x, y = make_plot_data(function, line, number_of_samples)
    plot(x, y)
    show()
    close()


def _test_function(position: Point) -> float:
    return sin(2.0*pi*position.x)*cos(2.0*pi*position.y)


if __name__ == "__main__":
    print("Plotting along a line though a point cloud...")
    print(
        "Note that this may take some time since we are "
        "doing a brute force nearest neighbor evaluation"
    )

    domain_size = (1.0, 1.0)
    number_of_points = (50, 50)
    dx = (
        domain_size[0]/float(number_of_points[0]),
        domain_size[1]/float(number_of_points[1])
    )

    point_cloud = PointCloud([
        Point(float(i)*dx[0], float(j)*dx[1])
        for i in range(number_of_points[0])
        for j in range(number_of_points[1])
    ])

    point_values = [_test_function(p) for p in point_cloud]

    plot_over_line(
        DiscreteFunction(point_cloud, point_values),
        Line(Point(0.0, 0.0), Point(1.0, 1.0)),
        number_of_samples=2000
    )
