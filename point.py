from __future__ import annotations


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, vector: Vector) -> Point:
        return Point(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector: Vector) -> Point:
        return Point(self.x - vector.x, self.y - vector.y)

    def coords(self) -> Tuple[int, int]:
        return (self.x, self.y)
