import numpy as np
from copy import deepcopy


class Puzzle:
    def __init__(self, initial_board):
        self.board = initial_board
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def manhattan_distance(self, board=None):
        if board is None:
            board = self.board
        distance = 0
        for i in range(3):
            for j in range(3):
                value = board[i][j]
                if value != 0:  # Ignore the blank tile (0)
                    target_x, target_y = divmod(value - 1, 3)
                    distance += abs(target_x - i) + abs(target_y - j)
        return distance

    def get_neighbors(self, board=None):
        if board is None:
            board = self.board
        neighbors = []
        x, y = [(i, row.index(0)) for i, row in enumerate(board) if 0 in row][0]
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]  # Up, Down, Left, Right
        for dx, dy in moves:
            if 0 <= dx < 3 and 0 <= dy < 3:  # Check bounds
                new_board = deepcopy(board)
                new_board[x][y], new_board[dx][dy] = new_board[dx][dy], new_board[x][y]
                neighbors.append(new_board)
        return neighbors

    def hill_climbing(self):
        current = deepcopy(self.board)
        path = [current]
        while True:
            neighbors = self.get_neighbors(current)
            best_neighbor = min(neighbors, key=self.manhattan_distance)

            if self.manhattan_distance(best_neighbor) >= self.manhattan_distance(current):
                break

            current = best_neighbor
            path.append(current)

        return current, self.manhattan_distance(current), path

    def display_board(self, board):
        for row in board:
            print(" ".join(str(x) if x != 0 else " " for x in row))
        print("\n")


test_cases = [
    {
        "initial": [[1, 2, 3], [4, 0, 6], [7, 5, 8]],
        "description": "Almost solved, minor moves needed (easy success case)",
    },
    {
        "initial": [[1, 2, 3], [4, 5, 6], [0, 7, 8]],
        "description": "Stuck due to local maxima (classic failure case)",
    },
    {
        "initial": [[1, 2, 3], [4, 5, 6], [8, 7, 0]],
        "description": "Requires large steps to solve, highlighting plateau",
    },
]

for i, test in enumerate(test_cases, start=1):
    print(f"Test Case {i}: {test['description']}")
    puzzle = Puzzle(test["initial"])
    print("Initial Board:")
    puzzle.display_board(test["initial"])

    result, cost, path = puzzle.hill_climbing()
    print("Resultant Board:")
    puzzle.display_board(result)
    print(f"Heuristic Cost: {cost}")
    print(f"Steps Taken: {len(path)}")
    if cost == 0:
        print("Status: Solved successfully!")
    else:
        print("Status: Failed to solve due to limitations.\n")
    print("=" * 50)