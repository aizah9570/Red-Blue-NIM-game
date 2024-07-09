import argparse

class RedBlueNimGame:
    def __init__(self, num_red, num_blue, version='standard', first_player='computer', depth=3):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.current_player = first_player
        self.depth = depth

    def is_game_over(self):
        return self.num_red == 0 or self.num_blue == 0

    def get_score(self):
        return (self.num_red * 2) + (self.num_blue * 3)

    def make_move(self, move):
        if move == "1r":
            self.num_red = max(0, self.num_red - 1)
        elif move == "1b":
            self.num_blue = max(0, self.num_blue - 1)
        elif move == "2r":
            self.num_red = max(0, self.num_red - 2)
        elif move == "2b":
            self.num_blue = max(0, self.num_blue - 2)

    def available_moves(self):
        moves = []
        if self.num_red > 0:
            moves.append("1r")
        if self.num_blue > 0:
            moves.append("1b")
        if self.num_red > 1:
            moves.append("2r")
        if self.num_blue > 1:
            moves.append("2b")
        return moves

def minmax(game, depth, alpha, beta, maximizing_player):
    if depth == 0 or game.is_game_over():
        return game.get_score()

    if maximizing_player:
        max_eval = -float('inf')
        for move in game.available_moves():
            new_game = RedBlueNimGame(game.num_red, game.num_blue, game.version, game.current_player, game.depth)
            new_game.make_move(move)
            eval = minmax(new_game, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in game.available_moves():
            new_game = RedBlueNimGame(game.num_red, game.num_blue, game.version, game.current_player, game.depth)
            new_game.make_move(move)
            eval = minmax(new_game, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(game):
    best_eval = -float('inf')
    best_move = None
    for move in game.available_moves():
        new_game = RedBlueNimGame(game.num_red, game.num_blue, game.version, game.current_player, game.depth)
        new_game.make_move(move)
        eval = minmax(new_game, game.depth, -float('inf'), float('inf'), False)
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

def human_move(game):
    while True:
        move = input(f"Your move (available moves: {game.available_moves()}): ")
        if move in game.available_moves():
            return move
        else:
            print("Invalid move. Try again.")

def play_game(game):
    while not game.is_game_over():
        if game.current_player == 'human':
            move = human_move(game)
            game.make_move(move)
            game.current_player = 'computer'
        else:
            move = best_move(game)
            print(f"Computer moves: {move}")
            game.make_move(move)
            game.current_player = 'human'
        print(f"Red marbles: {game.num_red}, Blue marbles: {game.num_blue}")

    if game.version == 'standard':
        if game.is_game_over():
            print("Game over! You lose.")
    else:  # misere version
        if game.is_game_over():
            print("Game over! You win.")
    print(f"Final Score: {game.get_score()}")

def parse_args():
    parser = argparse.ArgumentParser(description="Red-Blue Nim Game")
    parser.add_argument('--num-red', type=int, default=5, help='Number of red marbles')
    parser.add_argument('--num-blue', type=int, default=7, help='Number of blue marbles')
    parser.add_argument('--version', choices=['standard', 'misere'], default='standard', help='Game version')
    parser.add_argument('--first-player', choices=['computer', 'human'], default='computer', help='First player')
    parser.add_argument('--depth', type=int, default=3, help='Search depth for AI')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    game = RedBlueNimGame(args.num_red, args.num_blue, args.version, args.first_player, args.depth)
    play_game(game)
