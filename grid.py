from __future__ import annotations
from point import Point


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def count(self) -> int:
        return self.width * self.height

    def wrap_point(self, point: Point) -> Point:
        return Point(point.x % self.width, point.y % self.height)

    def point_by_index(self, index: int) -> Point:
        x = index % self.width
        y = index // self.width
        return Point(x, y)

    def index_by_point(self, point: Point) -> int:
        x, y = self.wrap_point(point).coords()
        return x + self.width * y

    def move_point(self, point: Point, vector: Vector) -> Point:
        return self.wrap_point(point + vector)
