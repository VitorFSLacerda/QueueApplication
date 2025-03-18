from twisted.protocols.basic import LineReceiver
from twisted.internet import protocol, reactor
import json
import cmd


class CallCenterClient(LineReceiver):
    
    def connectionMade(self):
        """When the connection to the server is established, start the command loop."""

        reactor.callInThread(self.start_command_loop)


    def start_command_loop(self):
        """Starts the command interpreter in a separate thread."""

        cmd_interpreter = CommandInterpreter(self)
        cmd_interpreter.cmdloop()


    def lineReceived(self, line):
        """Processes each line received from the server."""

        response = json.loads(line.decode('utf-8'))
        print(f"{response['response']}")


    def sendCommand(self, command):
        """Sends a JSON command to the server."""

        self.sendLine(json.dumps(command).encode('utf-8'))


class CallCenterFactory(protocol.ClientFactory):

    def buildProtocol(self, _):

        return CallCenterClient()


class CommandInterpreter(cmd.Cmd):
    prompt = ""

    def __init__(self, client):
        super().__init__()
        self.client = client


    def do_call(self, line):
        """Command to initiate a call with the given ID."""

        command = {"command": "call", "id": line.strip()}
        self.client.sendCommand(command)


    def do_answer(self, line):
        """Command to answer a call associated with the operator."""

        command = {"command": "answer", "id": line.strip()}
        self.client.sendCommand(command)


    def do_reject(self, line):
        """Command to reject a call associated with the operator."""

        command = {"command": "reject", "id": line.strip()}
        self.client.sendCommand(command)


    def do_hangup(self, line):
        """Command to hang up the call with the given ID."""

        command = {"command": "hangup", "id": line.strip()}
        self.client.sendCommand(command)


def start_client():
    reactor.connectTCP("localhost", 5678, CallCenterFactory())
    reactor.run()


if __name__ == "__main__":
    start_client()
