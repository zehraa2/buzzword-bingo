
from socket import socket
from modals.ClientModal import Client


DEV_JOIN = "join -name TestName"

# Client Service interacts with input and sends messages to server
# Also represents all business logic for the client


class ClientService(object):
    client: Client
    connected: bool

    check: int = 1
    check_minus: int = 6

    def __init__(self, IP: str, PORT: int, connection: socket):
        self.client = Client(IP, PORT, connection)
        self.connected = True

    # check if there are any winners in game
    def handleIsWinner(self):
        if self.client.getId() == None:
            return
        self.client.sendToServer({"action": "bingo"})
        response = self.client.receiveMessage()
        if response.get("action") == "bingo":
            for winner in response.get("winners"):
                if winner.get("id") == self.client.getId():
                    self.client.setIsWinner(True)
                    self.client.printInPanelBox(
                        f"🔥 [b]You are the winner![/b] 🎊 🎉", "bright_yellow")
            # string = " ".join(response['winners'])
            string = " ".join([winner.get("name")
                              for winner in response.get("winners")])
            self.client.printInPanelBox(
                f"[b]💥💥 Players with B I N G O:[/b]\n[yellow]{string}", "purple")

    # join command `join -name NAME`
    def handleJoinCommand(self, input: str):
        joinMessage = self.getJoinDictionary(input)
        if joinMessage != None:
            self.client.sendToServer(joinMessage)
            response = self.client.receiveMessage()
            if "error" in response:
                self.client.printError(response["message"])
            self.client.setId(response.get("id"))
            self.client.printInBox(response.get("text"), "turquoise")
            self.client.printGrid(response.get("grid"))
        else:
            self.client.printInvalidCommand(
                "Invalid command: " + input, "Valid: join -name YOUR_NAME")

    # check command `check -x 1 -y 3`
    def handleCheckCommand(self, input: str):
        checkMessage = self.getCheckDictionary(input)
        # "check -x " + str(self.check) + " -y " + str(1))
        try:
            if checkMessage != None:
                self.client.sendToServer(checkMessage)
                response = self.client.receiveMessage()
                if "error" in response:
                    self.client.printError(response["message"])
                else:
                    self.check += 1
                    self.check_minus -= 1
                    self.client.printInPanelBox(
                        f"## [b]You checked: [/b]\n[yellow]{response['word']}", "bright_white")
                    self.client.printGrid(response.get("grid"))
            else:
                self.client.pingServer()
                self.client.printInvalidCommand(
                    "Invalid command: " + input, "Valid: check -x NUMBER -y NUMBER")
        except:
            # TODO print help
            self.client.printError("Error: You must be joined to play.")

    # Leave or disconnect form game
    def handleLeaveCommand(self):
        self.client.sendToServer({"action": "quit"})
        self.connected = False

    # get command dictionary from input
    @staticmethod
    def getJoinDictionary(command):
        if command == None:
            return None
        obj = {}
        splitted = command.split(" ")
        if 2 not in range(-len(splitted), len(splitted)):
            return None
        if splitted[0] == "join":
            obj["action"] = splitted[0]
        else:
            return None
        if splitted[1] == "-name":
            obj["name"] = splitted[2]
        else:
            return None
        return (obj)

    def isClientWinner(self):
        return self.client.getIsWinner()

    # get command dictionary from input
    @staticmethod
    def getCheckDictionary(command):
        if command == None:
            return None
        splitted = command.split(" ")
        if 4 not in range(-len(splitted), len(splitted)):
            return None
        x_num = (splitted[2])
        y_num = (splitted[4])
        obj = {}
        if splitted[0] == "check":
            obj["action"] = splitted[0]
        else:
            return None
        if splitted[1] == "-x" and x_num.isnumeric():
            obj["x"] = x_num
        else:
            return None
        if splitted[3] == "-y" and y_num.isnumeric():
            obj["y"] = y_num
        else:
            return None
        return (obj)
