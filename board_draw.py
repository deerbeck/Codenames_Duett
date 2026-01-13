import random

ROWS = 5
COLUMNS = 5
BOARD_SIZE = ROWS * COLUMNS
WINNING_GREEN_COUNT = 9
OVERLAP = 3
NUM_BLACK_PER_PLAYER = 3

green_1 = set(random.sample(range(BOARD_SIZE), WINNING_GREEN_COUNT))

# pick exactly 3 elements from green_1 to overlap
overlap = set(random.sample(list(green_1), OVERLAP))
# pick the remaining 6 from indices not in green_1
remaining_pool = set(range(BOARD_SIZE)) - green_1
green_2 = overlap | set(random.sample(list(remaining_pool), (WINNING_GREEN_COUNT - OVERLAP)))

# build black sets with the constraints:
# - one number shared between black_1 and black_2 that is in neither green_1 nor green_2
# - black_1 contains one number from green_2
# - black_2 contains one number from green_1
# - each black set has one additional number that is not in any green set and not in the other black set (unique)
all_indices = set(range(BOARD_SIZE))
non_green_pool = list(all_indices - green_1 - green_2)

# ensure we have enough non-green indices (should be 25 - |green_1 ∪ green_2|)
if len(non_green_pool) < NUM_BLACK_PER_PLAYER - 1:
    raise RuntimeError("Not enough non-green indices to satisfy black set constraints")

# pick one shared black number (not in any green)
shared_black = random.choice(non_green_pool)
non_green_pool.remove(shared_black)

# pick one unique non-green number for each black set
unique_black_1 = random.choice(non_green_pool)
non_green_pool.remove(unique_black_1)
unique_black_2 = random.choice(non_green_pool)
non_green_pool.remove(unique_black_2)

# pick one from the opposite green set for each black set
black1_from_green2 = random.choice(list(green_2 - overlap))
black2_from_green1 = random.choice(list(green_1 - overlap))

black_1 = {shared_black, black1_from_green2, unique_black_1}
black_2 = {shared_black, black2_from_green1, unique_black_2}


def board_matrix_from_sets(green_set, black_set):
    """Return a 5x5 matrix (list of lists) with 'G' for any green/black positions and 'O' for empty."""
    board = [['X' for _ in range(COLUMNS)] for _ in range(ROWS)]
    for pos in green_set:
        row = pos // COLUMNS
        col = pos % COLUMNS
        board[row][col] = "\033[32mG\033[0m"
    for pos in black_set:
        row = pos // COLUMNS
        col = pos % COLUMNS
        board[row][col] = "\033[31mS\033[0m"
    return board

def print_board(board):
    for row in board:
        print(' '.join(row))


if __name__ == "__main__":
    print("\nCodenames Duet Board-Generator:")
    print("Player 1 (Green 1 & Black 1):")
    print("Green 1 position:", green_1)
    print("Black 1 position:", black_1)
    print("\nPlayer 1 board:")
    print_board(board_matrix_from_sets(green_1, black_1))
    input("\nPress Enter to acknowledge Player 1's positions...")
    print('\033c', end='')  # Clear screen
    input("\nPress Enter to reveal Player 2's positions...")
    print("\nPlayer 2 (Green 2 & Black 2):")
    print("Green 2 position:", green_2)
    print("Black 2 position:", black_2)
    print("\nPlayer 2 board:")
    print_board(board_matrix_from_sets(green_2, black_2))
    input("\nPress Enter to clear...")
    print('\033c', end='')  # Clear screen