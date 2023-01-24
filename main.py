import pygame
from typing import Union
from board import Board
from user_block import UserBlock

# utility function
def represent_position_in_pixel(x: Union[int, float], y: Union[int, float]) -> tuple[Union[int, float], Union[int, float]]:
    return x*50, y*50


# window settings
pygame.init()
size = (1000, 500)
screen = pygame.display.set_mode(size)

# font settings
pygame.font.init()
default_font = pygame.font.SysFont('Comic Sans MS', 80)
thirty_inch_font = pygame.font.SysFont("Comic Sans MS", 30)

# main code
running = True
is_started = False
while running:
    if not is_started:
        board = Board()
        user_block = UserBlock()
        is_started = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # inside this function, the position of the user block will be updated if needed
            if not user_block.is_game_over:
                user_block.process_position_shift_event(event.key)
            else:
                board = Board()
                user_block = UserBlock()

    # game over logic
    is_game_over = board.check_game_over(user_block)

    if not is_game_over:
        screen.fill((255, 255, 255))

        # update the level if needed
        board.update_level_if_needed(user_block.score)

        # update board and user box by one row
        is_updated = board.do_update_if_needed()
        if is_updated:
            user_block.shift_position(4, for_shift_row=True)

        # render all the blocks from the board
        for r_idx in range(len(board.placements)):
            for c_idx in range(len(board.placements[r_idx])):
                if board.placements[r_idx][c_idx]:
                    x, y = represent_position_in_pixel(c_idx, r_idx)  # be careful: row -> y; column -> x

                    pygame.draw.rect(screen, (0, 0, 0), (x, y, 50, 50))

        # render the user block
        block_x, block_y = represent_position_in_pixel(user_block.x, user_block.y)
        pygame.draw.rect(screen, (255, 0, 0), (block_x, block_y, 50, 50))

        # render current user score
        text_surface = thirty_inch_font.render(f'Score: {user_block.score}', False, (0, 255, 0))
        x, y = represent_position_in_pixel(17, 0)
        screen.blit(text_surface, (x, y))

    else:
        # Game Over
        screen.fill((0, 255, 255))
        game_over_surface = default_font.render(f'You Suck Mate', False, (0, 0, 0))
        x, y = represent_position_in_pixel(4.5, 3)
        screen.blit(game_over_surface, (x, y))

        score_surface = thirty_inch_font.render(f'Score: {user_block.score}', False, (0, 0, 0))
        x, y = represent_position_in_pixel(9, 6)
        screen.blit(score_surface, (x, y))

        continue_surface = thirty_inch_font.render("Press Any Key to Play Again...", False, (0, 0, 0))
        x, y = represent_position_in_pixel(6, 8)
        screen.blit(continue_surface, (x, y))

    pygame.display.flip()

pygame.quit()
