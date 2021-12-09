import random, os
from stockfish import Stockfish

class AtomChess:
    def __init__(self, rating, user):
        self.user = user
        self.move_list = []
        self.stockfish = Stockfish(os.getenv('PATH_TO_STOCKFISH')) 
        if random.randint(0, 1) == 1:
            self.color = 'white'
            self.player_color = 'black'
        else:
            self.color = 'black'
            self.player_color = 'white'

    def ai_move(self):
        move = self.stockfish.get_best_move()
        # Have the chess engine look for a valid move if it has selected an invalid one
        while self.stockfish.is_move_correct(move) == 'failed':
            move = self.stockfish.get_best_move()
        
        self.move_list.append(move) 
        self.stockfish.set_position(self.move_list)
        return move

    def move(self, move):
        # Check if the move is valid
        if self.stockfish.is_move_correct(move):
            # Append the move to a list of moves for the current game and then update the position
            self.move_list.append(move) 
            self.stockfish.set_position(self.move_list)
            
            # Return the move made for discord message
            return move
        else:
            # Return a specific flag for if the move was invalid
            return 'failed'