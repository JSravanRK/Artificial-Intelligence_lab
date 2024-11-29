import random
from collections import defaultdict
class MENACE:
    def _init_(self):
        self.matchboxes = defaultdict(lambda: defaultdict(int))  # Maps board states to bead counts
        self.history = []  # Tracks moves for learning

    def initialize_matchbox(self, board_state):
        if board_state not in self.matchboxes:
            for i in range(9):  # Add all possible moves with 1 bead
                if board_state[i] == " ":
                    self.matchboxes[board_state][i] = 1
    def choose_move(self, board_state):
        self.initialize_matchbox(board_state)
        moves = self.matchboxes[board_state]
        total_beads = sum(moves.values())
        if total_beads == 0:
            return random.choice([i for i, cell in enumerate(board_state) if cell == " "])
        probabilities = [moves[i] / total_beads for i in range(9)]
        chosen_move = random.choices(range(9), weights=probabilities, k=1)[0]
        self.history.append((board_state, chosen_move))
        return chosen_move
    def update_matchboxes(self, result):
        for board_state, move in self.history:
            if result == 1:  # MENACE won
                self.matchboxes[board_state][move] += 3
            elif result == -1:  # MENACE lost
                self.matchboxes[board_state][move] = max(1, self.matchboxes[board_state][move] - 1)
            # No changes for a draw
        self.history = []

def display_board(board):
    for i in range(0, 9, 3):
        print(" | ".join(board[i:i+3]))
        if i < 6:
            print("-" * 5)

def check_winner(board, player):
    win_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                     (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                     (0, 4, 8), (2, 4, 6)]  # Diagonals
    return any(all(board[i] == player for i in line) for line in win_positions)

def play_game():
    menace = MENACE()
    for game in range(10):  # Play multiple games to train MENACE
        board = [" "] * 9
        current_player = "X"
        result = 0
        while " " in board:
            if current_player == "X":
                print("MENACE's turn:")
                move = menace.choose_move(tuple(board))
            else:
                print("Your turn:")
                display_board(board)
                move = int(input("Enter your move (0-8): "))
                while board[move] != " ":
                    move = int(input("Invalid move. Try again: "))
            board[move] = current_player
            display_board(board)
            if check_winner(board, current_player):
                result = 1 if current_player == "X" else -1
                print(f"{current_player} wins!")
                break
            current_player = "O" if current_player == "X" else "X"
        if result == 0:
            print("It's a draw!")
        menace.update_matchboxes(result)
if _name_ == "_main_":
    play_game()
