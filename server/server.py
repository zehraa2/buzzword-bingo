from asyncio import exceptions
import sys
import socket
import threading
import re
from os.path import exists
from controllers.GameController import GameController
from services.GameService import GameService

import time

from rich.progress import Progress
from rich import print

from rich.console import Console
from rich.markdown import Markdown


HELP_INFO = """
# Buzzword bingo

This is a small help board to start the game.

These are arguments that you should pass to the programm:

* -wordsfile : The file that contains the words that will be used in the game.
* -grid : The resolution of the game.

Example: python3 server/server.py -wordsfile ~/uni/bsrn/words.txt -grid 4x4

--------------------------------------------------------------------------------

"""


def printHelp():
    console = Console()
    md = Markdown(HELP_INFO)
    console.print(md)


IP = socket.gethostbyname("localhost")
PORT = 5566
ADDR = (IP, PORT)

# get arguments from array (sys.argv) and return dict from it


def handleCommands(arr):
    obj = dict()
    for i, arg in enumerate(arr):
        if(arg == "-wordsfile"):
            obj["wordsfile"] = arr[i + 1]
        if(arg == "-grid"):
            obj["grid"] = arr[i + 1]
        if(arg == "-maxplayers"):
            obj["maxplayers"] = arr[i + 1]
    return obj


# check if arguments are valid
def validateCommands(wordsFile, resolution):
    errors = []
    if not exists(wordsFile):
        errors.append("Words file not found")
    if not re.match(r"^[0-9]{1}x[0-9]{1}$", resolution):
        errors.append("Resolution format is not valid, Example: 5x5")
    return errors


# The starter function, that handles all messages from client and runs business logic
def start_server_connection(conn, addr, wordsFile, resolution):
    app = GameService(IP, PORT, conn, addr, wordsFile, 2, resolution)
    print(f"[bold green][NEW CONNECTION][/bold green] {addr} connected!")
    controller = GameController(app)
    while app.game.connected:
        message = app.game.receiveMessage()
        print(f"[orange1][RECEIVED][/orange1] {message}")
        if message.get("action") == "quit":
            controller.handleConnectionBreak(addr)
        if message.get("action") == "join":
            controller.handleJoin(message, addr)
        if message.get("action") == "check":
            controller.handleCheck(message, addr)
        if message.get("action") == "bingo":
            controller.handleIsWinner()
        if "ping" in message:
            print("[orange1][RECEIVED][/orange1] ping message")
            app.game.sendToClient({"ping": "response ping"})
    app.game.closeClientConnection()


# Creates server for game
def main(wordsFile, resolution):
    print(f"[bold green][STARTING][/bold green] Server is starting...!")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(
        f"[bold gold1][LISTENING][/bold gold1] Server is listening on {IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=start_server_connection, args=(
            conn, addr, wordsFile,  resolution))
        print(threading.active_count())
        thread.start()
        print(
            f"[green][ACTIVE CONNECTIONS][/green] {threading.activeCount() - 1}")


# Main Function, that runs all pre check functions and starts the server
if __name__ == "__main__":
    # EXAMPLE: python3 server/server.py -wordsfile ~/uni/bsrn/words.txt -grid 4x4
    printHelp()
    try:
        if len(sys.argv) == 1:
            print("[ERROR] No arguments were passed")
            exit()
        obj = handleCommands(sys.argv)
        wordsFIle = obj.get("wordsfile")
        resolution = obj.get("grid")
        if wordsFIle is None or resolution is None:
            print("[ERROR] Missing arguments")
            exit()
        err = validateCommands(wordsFIle, resolution)
        if len(err) > 0:
            print("[ERRORS] " + str(err))
        else:
            with Progress() as progress:
                task2 = progress.add_task("[green]Processing...", total=100)
                task3 = progress.add_task("[cyan]Installing...", total=100)
                while not progress.finished:
                    progress.update(task2, advance=1)
                    progress.update(task3, advance=0.8)
                    time.sleep(0.02)
        main(wordsFIle, resolution)
    except KeyboardInterrupt:
        print("[red][INTERRUPT][/red] Server was closed")
        exit()
    except Exception:
        print("[red][ERROR][/red] Server was closed")
        exit()
