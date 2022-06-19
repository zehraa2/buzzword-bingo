import json
from socket import socket

from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.table import Column
from rich import box
from rich.panel import Panel


# Client Object has all information about the client connected to the game
# The Rich Theme is also defined here
# Client includes methods to send and receive messages from the server
# also includes methods to print messages to the console

class Client(object):
    id: str = None
    IP: str
    PORT: int
    ADDR: set()
    FORMAT = "utf-8"
    SIZE = 8192
    connection: socket

    isWinner: bool = False

    # rich theme

    theme = Theme({"success": "green", "error": "bold red",
                  "warning": "yellow1", "turquoise": "pale_turquoise1"})
    console = Console(theme=theme)

    def __init__(self, IP, PORT, connection):
        self.IP = IP
        self.PORT = PORT
        self.ADDR = (IP, PORT)
        self.connection = connection
        self.connection.connect(self.ADDR)

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setIsWinner(self, val):
        self.isWinner = val

    def getIsWinner(self):
        return self.isWinner

    @staticmethod
    def dictionaryToJson(dictionary):
        return json.dumps(dictionary, indent=2)

    @staticmethod
    def jsonToDictionary(jsonStr):
        return json.loads(jsonStr)

    def sendToServer(self, dictionary: dict):
        self.connection.send(self.dictionaryToJson(
            dictionary).encode(self.FORMAT))

    def receiveMessage(self):
        return self.jsonToDictionary(self.connection.recv(self.SIZE).decode(self.FORMAT))

    def pingServer(self):
        self.sendToServer({"action": "ping"})

    def printInvalidCommand(self, invalid, valid):
        self.console.print(invalid, style="warning")
        self.console.print(valid, style="success")

    def printInBox(self, str, style):
        table = Table(Column(justify="center"), show_header=False,
                      padding=(1, 1, 1, 1), expand=True, box=box.DOUBLE_EDGE, style="turquoise2")
        table.add_row(str, style=style)
        self.console.print(table)

    def printGrid(self, list):
        reverted = list[::-1]
        table = Table(show_header=False, padding=(
            1, 1, 1, 1), expand=True, show_lines=True, box=box.DOUBLE_EDGE, style="turquoise2" if self.isWinner else "white")
        for row in range(len(list)):
            table.add_column("", justify="center")
        for row in (reverted):
            words = []
            for cell in row:
                words.append(cell.get("word"))
            table.add_row(*words)
        self.console.print(table)

    def printError(self, error):
        self.console.print(error, style="error")

    def printInPanelBox(self, message, borderColor: str):
        # return f"[b]{name}[/b]\n[yellow]{country}"
        self.console.print(Panel(message, expand=True, style=borderColor))
