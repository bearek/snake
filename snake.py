import sys
import pygame
from random import choice

from grid import Grid
from point import Point
from vector import Vector
from settings import Settings


class Snake:
    def __init__(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Snake")

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

        self.overlay = pygame.Surface(
            (self.screen_rect.width, self.screen_rect.height)
        )

        self.overlay.fill(self.settings.color.overlay)

        self.grid = Grid(20, 20)

        grid_rect_size = min(self.screen_rect.width, self.screen_rect.height)
        grid_rect_width = grid_rect_size
        grid_rect_height = grid_rect_size

        self.grid_surface = pygame.Surface((grid_rect_width, grid_rect_height))

        self.grid_rect = self.grid_surface.get_rect()
        self.grid_rect.center = self.screen_rect.center

        border_ratio = 0.15

        self.cells = []

        cell_width = grid_rect_width / ((self.grid.width + 1) *
                                        border_ratio + self.grid.width)
        cell_height = grid_rect_height / ((self.grid.height + 1) *
                                          border_ratio + self.grid.height)

        border_width = cell_width * border_ratio
        border_height = cell_height * border_ratio

        for y in range(0, self.grid.height):
            for x in range(0, self.grid.width):
                rect = pygame.Rect(
                    x * (border_width + cell_width) + border_width,
                    y * (border_height + cell_height) + border_height,
                    cell_width,
                    cell_height
                )

                self.cells.append(rect)

        game_over_font = pygame.font.SysFont(
            "Verdana",
            self.settings.font.size
        )

        self.game_over_text = game_over_font.render(
            "Game Over - press SPACEBAR to restart",
            True,
            self.settings.font.color
        )

        self.game_over_text_rect = self.game_over_text.get_rect()
        self.game_over_text_rect.center = self.screen_rect.center

        self.init_game()

    def init_game(self) -> None:
        self.snake_normal_speed = self.settings.snake.speed
        self.snake_effective_speed = self.snake_normal_speed
        self.snake_progress = 0

        self.game_active = True
        self.speed_up = False

        directions = [Vector.up, Vector.right, Vector.down, Vector.left]
        initial_direction = choice(directions)

        snake_head = self.grid.point_by_index(
            (self.grid.count() - self.grid.width) // 2
        )

        self.snake = [
            self.grid.index_by_point(snake_head - initial_direction(offset))
            for offset
            in range(self.settings.snake.length)
        ]

        self.snake_move_vector = initial_direction(1)
        self.snake_last_move_vector = None

        self.food = set()
        self._add_food()

    def run_game(self) -> None:
        while True:
            self._check_events()

            if self.game_active:
                if self.speed_up:
                    self.snake_effective_speed = max(
                        self.settings.snake.boost_speed,
                        self.snake_normal_speed
                    )
                else:
                    self.snake_effective_speed = self.snake_normal_speed

                self.snake_progress += self.snake_effective_speed

                if self.snake_progress >= 1:
                    self.snake_progress = 0
                    self.snake_last_move_vector = self.snake_move_vector

                    snake_head = self.grid.point_by_index(self.snake[0])
                    new_snake_head = self.grid.move_point(
                        snake_head, self.snake_last_move_vector
                    )
                    new_snake_head_index = self.grid.index_by_point(
                        new_snake_head
                    )

                    tail = self.snake.pop()

                    if new_snake_head_index in self.snake:
                        self.game_active = False

                    self.snake.insert(0, new_snake_head_index)

                    if new_snake_head_index in self.food:
                        self.food.remove(new_snake_head_index)
                        self.snake.append(tail)
                        self._add_food()
                        self.snake_normal_speed += self.settings.snake.acceleration

            self.screen.fill(self.settings.color.background)
            self._draw_grid()

            if not self.game_active:
                self.screen.blit(self.overlay, self.screen_rect)
                self.screen.blit(self.game_over_text, self.game_over_text_rect)

            pygame.display.flip()

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    if self.game_active:
                        self.speed_up = True
                    else:
                        self.init_game()
                else:
                    directions = {
                        pygame.K_UP: Vector.up,
                        pygame.K_RIGHT: Vector.right,
                        pygame.K_DOWN: Vector.down,
                        pygame.K_LEFT: Vector.left,
                    }

                    new_direction = directions.get(event.key)

                    if new_direction is not None:
                        self._change_direction(new_direction(1))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.speed_up = False

    def _change_direction(self, vector: Vector) -> None:
        if self.snake_last_move_vector.opposite() != vector:
            self.snake_move_vector = vector

    def _draw_grid(self) -> None:
        self.grid_surface.fill(self.settings.color.border)

        for cell_index, cell in enumerate(self.cells):
            if cell_index in self.snake:
                cell_color = self.settings.color.snake
            elif cell_index in self.food:
                cell_color = self.settings.color.food
            else:
                cell_color = self.settings.color.cell

            pygame.draw.rect(self.grid_surface, cell_color, cell)

        self.screen.blit(self.grid_surface, self.grid_rect)

    def _add_food(self) -> None:
        available_cells = [
            index
            for index
            in range(self.grid.count())
            if index not in self.snake
        ]

        cell_index = choice(available_cells)
        self.food.add(cell_index)


if __name__ == "__main__":
    snake = Snake()
    snake.run_game()
