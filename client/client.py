import socket
from services.ClientService import ClientService

from rich import print
from rich.console import Console
from rich.markdown import Markdown

HELP_INFO = """
# Welcome to Buzzword Bingo Game

This is a small help board to join the game.

These are COMMANDS that you should pass to the program:

* join -name YOUR_NAME: Command to join the game with your name.
* check -x NUMBER -y NUMBER: Command to check the word with coordinates.
* q: Command to quit Game.

Example: join -name John
Example: check -x 1 -y 1

--------------------------------------------------------------------------------

"""


def printHelp():
    console = Console()
    md = Markdown(HELP_INFO)
    console.print(md)


# static variables for ip and port
IP = socket.gethostbyname("localhost")
PORT = 5566
ADDR = (IP, PORT)


# check if string has command
def hasCommand(input: str, searchCommand: str):
    arr = input.split(" ")
    for i in range(len(arr)):
        if arr[i] == searchCommand:
            return True
    return False


# main function that connects to server and handles input
# all input interaction functions are in ClientService
def run_client():
    printHelp()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientService = ClientService(IP, PORT, client)
    print(
        f"[bold green][CONNECTED][/bold green] Client connected to server at {IP}:{PORT}")

    while clientService.connected:
        clientService.handleIsWinner()
        if clientService.isClientWinner():
            clientService.handleLeaveCommand()
            break
        # Wait for INPUT
        cmd = input("> ")
        # handle commands and send to server
        if hasCommand(cmd, "join"):
            clientService.handleJoinCommand(cmd)
        elif hasCommand(cmd, "check"):
            clientService.handleCheckCommand(cmd)
        elif hasCommand(cmd, "q"):
            clientService.handleLeaveCommand()
        else:
            printHelp()


if __name__ == "__main__":
    run_client()
