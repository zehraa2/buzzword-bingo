import random
import math
from modals.GameModal import GameModal
from modals.Player import Player


# GameService is for all bushiness logic of the game
# Has methods for generating the game grid, checking the grid, add new player

class GameService(object):
    game: GameModal

    def __init__(self, IP, PORT, connection, addr, wordsFile, maxPlayers, resolution):
        self.game = GameModal(
            IP, PORT, connection, addr, wordsFile, maxPlayers, resolution)

    def generateWordsGrid(self):
        #words_list = list("abcdefghijklmnopqrstuvwxyz")
        #words_list = "random word".split(" ")
        words_list = self.game.getWordsList()
        resolution = math.sqrt(self.game.resolution)
        range_num = int(resolution)
        middle_row = int((range_num / 2) + 1)
        result = []
        for i in range(range_num):
            arr = []
            for l in range(range_num):
                x = l + 1
                y = i + 1
                isJoker = self.isInJokerPosition(x, y, middle_row, range_num)
                arr.append({
                    "word": " " if isJoker else random.choice(words_list) + " -(" + str(x) + "," + str(y) + ")",
                    "x": x,
                    "y": y,
                    "checked": True if isJoker else False
                })
            result.append(arr)
        return result

    def playersHasBingo(self):
        players = self.game.getPlayers()
        winners = []
        for player in players:
            if player.hasBingo():
                if player.winner == False:
                    player.addHistory({"action": "bingo"})
                    player.setWinner(True)
                winners.append(player)
        return winners

    def addPlayer(self, name: str, address: any, startedAt: str, words: list):
        playerResolution = int(math.sqrt(self.game.resolution))
        player = Player(name, address, startedAt, words, playerResolution)
        self.game.addPlayer(player)
        return player

    def getPlayerWordsList(self, address):
        for player in self.game.getPlayers():
            if player.getAddress() == address:
                return player.getWords()

    def findPlayer(self, address):
        for player in self.game.getPlayers():
            if player.getAddress()[1] == address[1]:
                return player

    def setPlayerWords(self, address, words):
        player = self.findPlayer(address)
        player.setWords(words)

    def checkGridWord(self, address, x, y):
        player = self.findPlayer(address)
        new_words = player.getWords()
        checked_word = "Italy"
        for word_list in new_words:
            for word in word_list:
                if word["x"] == int(x) and word["y"] == int(y):
                    checked_word = word["word"].split(" ")[0]
                    word["checked"] = True
                    word["word"] = "❌"
        self.setPlayerWords(address, new_words)
        return checked_word

    def playerHasWordList(self, address):
        for player in self.game.getPlayers():
            if player.getAddress() == address:
                if player.hasWords():
                    return True
        return False

    @staticmethod
    def isInJokerPosition(x, y, middleRow, rangeNum):
        return y == middleRow and x == middleRow and (
            rangeNum == 5 or rangeNum == 7)
