from typing import List
from services.GameService import GameService
from modals.Player import Player


class GameController(object):
    gameService: GameService

    def __init__(self, gameService):
        self.gameService = gameService

    def handleJoin(self, message, addr):
        try:
            player_words = self.gameService.generateWordsGrid()
            new_player = self.gameService.addPlayer(
                message["name"], addr, "", player_words)
            self.gameService.game.sendToClient({
                "id": new_player.getId(),
                "text": f"Welcome to game {message['name']}",
                "grid": player_words,
            })
            new_player.addHistory(message)
            print(f"{message['name']} joined the game")
        except:
            self.gameService.game.sendToClient(
                {"error": True, "message": "Server Error"})

    def handleConnectionBreak(self, addr):
        player = self.gameService.findPlayer(addr)
        if player is not None:
            player.addHistory({"action": "quit"})
        self.gameService.game.closeClientConnection()

    def handleCheck(self, message, addr):
        try:
            if self.gameService.playerHasWordList(addr):
                checked_word = self.gameService.checkGridWord(
                    addr, message["x"], message["y"])
                message["word"] = checked_word
                self.gameService.game.sendToClient({
                    "checked": True,
                    "word": checked_word,
                    "grid": self.gameService.getPlayerWordsList(addr)
                })
                self.gameService.findPlayer(addr).addHistory(message)
            else:
                self.gameService.game.sendToClient(
                    {"error": "You don't have a word list"})
        except:
            self.gameService.game.sendToClient(
                {"error": True, "message": "Server Error"})

    def handleIsWinner(self):
        winners: List[Player] = self.gameService.playersHasBingo()
        if len(winners) == 0:
            self.gameService.game.sendToClient(
                {"action": "ping"}
            )
        else:
            self.gameService.game.sendToAll({
                "action": "bingo",
                "winners": [{"name": winner.getName(), "addr": winner.getAddress(), "id": winner.getId()} for winner in winners]
            })
