from math import inf
from timeit import default_timer
import pygame

class UserBlock:
    def __init__(self):
        self.x = 9
        self.y = 7
        self.comma_pressed_time = -inf
        self.period_pressed_time = -inf
        self.is_game_over = False
        self.score = 0

    def process_position_shift_event(self, event_key: pygame.KEYDOWN) -> None:
        if event_key == pygame.K_COMMA:
            self.comma_pressed_time = default_timer()
        elif event_key == pygame.K_PERIOD:
            self.period_pressed_time = default_timer()

        elif event_key == pygame.K_UP:
            delta_from_period = default_timer() - self.period_pressed_time
            delta_from_comma = default_timer() - self.comma_pressed_time

            if delta_from_comma < 0.2:
                self.shift_position(7)
            elif delta_from_period < 0.2:
                self.shift_position(1)
            else:
                self.shift_position(0)

        elif event_key == pygame.K_RIGHT:
            self.shift_position(2)

        elif event_key == pygame.K_DOWN:
            delta_from_comma = default_timer() - self.comma_pressed_time
            delta_from_period = default_timer() - self.period_pressed_time

            if delta_from_comma < 0.2:
                self.shift_position(5)
            elif delta_from_period < 0.2:
                self.shift_position(3)
            else:
                self.shift_position(4)

        elif event_key == pygame.K_LEFT:
            self.shift_position(6)

    def shift_position(self, direction: int, for_shift_row=False) -> None:
        """
        :param for_shift_row: if this function is used to shift the rows, then the score will not be updated inside
        :param direction: 0=north, 1=north-east, 2=east, 3=south-east, 4=south, 5=south-west, 6=west, 7=north-west
        :return:
        """
        if direction == 0:
            if self.y != 0:
                self.y -= 1
                self.score += 1

        elif direction == 1:
            if self.x != 19 and self.y != 0:
                self.x += 1
                self.y -= 1
                self.score += 1

        elif direction == 2:
            if self.x != 19:
                self.x += 1

        elif direction == 3:
            if self.y == 9:
                self.is_game_over = True
            if self.x != 19:
                self.x += 1
                self.y += 1
                self.score -= 1

        elif direction == 4:
            if self.y == 9:
                self.is_game_over = True

            self.y += 1

            if not for_shift_row:
                self.score -= 1

        elif direction == 5:
            if self.y == 9:
                self.is_game_over = True
            if self.x != 0:
                self.x -= 1
                self.y += 1
                self.score -= 1

        elif direction == 6:
            if self.x != 0:
                self.x -= 1

        elif direction == 7:
            if self.x != 0 and self.y != 0:
                self.x -= 1
                self.y -= 1
                self.score += 1

        else:
            raise ValueError("direction must be 0/1/2/3")

    def represent_position_in_pixel(self) -> tuple[int, int]:
        return self.x*50, self.y*50