from __future__ import annotations


class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def up(length: int) -> Vector:
        return Vector(0, -length)

    @staticmethod
    def right(length: int) -> Vector:
        return Vector(length, 0)

    @staticmethod
    def down(length: int) -> Vector:
        return Vector(0, length)

    @staticmethod
    def left(length: int) -> Vector:
        return Vector(-length, 0)

    def opposite(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __add__(self, vector: Vector) -> Vector:
        return Vector(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector: Vector) -> Vector:
        return Vector(self.x - vector.x, self.y - vector.y)

    def __eq__(self, vector: Vector) -> bool:
        return self.x == vector.x and self.y == vector.y
