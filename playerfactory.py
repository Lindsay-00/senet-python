from humanplayer import HumanPlayer
from aiplayer import AIPlayer

class PlayerFactory:
    
    def create_player(self, color, board, type):
        if type == "human":
            return HumanPlayer(color, board, type)
        else:
            return AIPlayer(color, board, type)
            