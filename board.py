from timeit import default_timer
from random import sample
from user_block import UserBlock

class Board:
    def __init__(self) -> None:
        # true means there is an obstacle at that position
        self.placements = [self.generate_row() for _ in range(6)]
        self.last_updated_time = default_timer()
        self.level = 0
        self.score_required_for_next_lv = 20

    @staticmethod
    def generate_row() -> list[bool]:
        # TODO
        indices = sample(list(range(0, 20)), 10)

        new_row = [False]*20
        for index in indices:
            new_row[index] = True

        return new_row

    def update_level_if_needed(self, current_score: int) -> bool:

        if current_score == self.score_required_for_next_lv and current_score != 0:
            self.level += 1
            self.score_required_for_next_lv += 30
            return True

        return False

    def do_update_if_needed(self) -> bool:
        current_time = default_timer()
        if current_time - self.last_updated_time > max(0.9 - 0.1*self.level, 0.2):
            self.last_updated_time = current_time
            self.update()
            return True
        return False

    def update(self) -> None:
        new_row = self.generate_row()

        if len(self.placements) < 10:
            self.placements.insert(0, new_row)
        else:
            self.placements.pop()
            self.placements.insert(0, new_row)

    def check_game_over(self, user_block: UserBlock) -> bool:
        if (user_block.y <= len(self.placements)-1 and self.placements[user_block.y][user_block.x]) or user_block.is_game_over:
            user_block.is_game_over = True
            return True
        else:
            return False