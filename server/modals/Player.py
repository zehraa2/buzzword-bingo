import uuid
import datetime


class Player(object):
    id: str
    name: str
    address: set
    startedAt: str
    words: list
    history: list = []
    resolution: int
    logFileName: str
    winner = False
    # history dict type
    # {
    # 	action: str,
    # 	x: int,
    # 	y: int,
    # }

    def __init__(self, name, address, startedAt, words, resolution):
        self.id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.startedAt = startedAt
        self.words = words
        self.connected = False
        self.resolution = resolution
        self.logFileName = self.getTimestamp() + "-" + name + ".txt"

    # Methods
    def addWord(self, word):
        self.words.append(word)

    def addHistory(self, history):
        log = self.getTimestamp()
        action = history.get("action")
        print("[LOGGER] action: " + action)
        if action == "join":
            log += " - " + self.name + " joined the game" + "\n"
            log += self.getTimestamp() + " grid size: " + str(self.resolution) + "\n"
        if action == "check":
            log += " Checked word: " + history.get("word") + " at position: " + str(
                history.get("x")) + "," + str(history.get("y")) + "\n"
        if action == "bingo":
            log += " Bingo! " + self.name + " won the game" + "\n"
        if action == "quit":
            log += " " + self.name + " left the game" + "\n"
        self.history.append(log)
        with open("logs/" + self.logFileName, 'a+') as f:
            f.writelines(log)

    @staticmethod
    def getTimestamp():
        return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def hasWords(self):
        return len(self.words) > 0

    def concat(self):
        arr = self.getWords()
        result = []
        for i in range(len(arr)):
            for l in range(len(arr[i])):
                result.append(arr[i][l])
        return result

    def hasBingoHorizontal(self):
        arr = self.concat()
        for i in range(self.resolution):
            checkedAmount = 0
            for word in arr:
                if word.get("y") == i and word.get("checked"):
                    checkedAmount += 1
                elif word.get("y") == i and not word.get("checked"):
                    checkedAmount = 0
                    break
            if checkedAmount == self.resolution:
                return True

    def hasBingoVertical(self):
        arr = self.concat()
        for i in range(self.resolution):
            checkedAmount = 0
            for word in arr:
                if word.get("x") == i and word.get("checked"):
                    checkedAmount += 1
                elif word.get("x") == i and not word.get("checked"):
                    checkedAmount = 0
                    break
            if checkedAmount == self.resolution:
                return True
        return False

    def hasBingoDiagonalIndexUp(self):
        arr = self.getWords()
        checkedAmount = 0
        for i in range(self.resolution):
            if arr[i][i].get("checked"):
                checkedAmount += 1
            else:
                checkedAmount = 0
                break
        if (checkedAmount == self.resolution):
            return True
        else:
            return False

    def hasBingoDiagonalIndexDown(self):
        arr = self.concat()
        checkedAmount = 0
        for i in range(self.resolution):
            y = i + 1
            x = self.resolution - i
            for word in arr:
                if word.get("x") == x and word.get("y") == y and word.get("checked"):
                    checkedAmount += 1
                else:
                    continue
        if (checkedAmount == self.resolution):
            return True
        else:
            return False

    def hasBingo(self):
        # TODO History len > resolution
        vertical = self.hasBingoVertical()
        horizontal = self.hasBingoHorizontal()
        diagonalUp = self.hasBingoDiagonalIndexUp()
        diagonalDown = self.hasBingoDiagonalIndexDown()
        return vertical or horizontal or diagonalUp or diagonalDown

    # Getters and Setters

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getAddress(self):
        return self.address

    def setAddress(self, address):
        self.address = address

    def getStartedAt(self):
        return self.startedAt

    def setStartedAt(self, startedAt):
        self.startedAt = startedAt

    def getWords(self):
        return self.words

    def setWords(self, words):
        self.words = words

    def getHistory(self):
        return self.history

    def setHistory(self, history):
        self.history = history

    def setWinner(self, bool):
        self.winner = bool
