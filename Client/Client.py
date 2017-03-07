# -*- coding: utf-8 -*-
import socket
import json
from Client.MessageReceiver import MessageReceiver
from Client.MessageParser import MessageParser


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Run server
        self.host = host
        self.server_port = server_port
        self.run()

        # Set valid inputs
        self.possible_inputs = {
            "login": self.login(self.input_content),
            "logout": self.logout(),
            "msg": self.message(self.input_content),
            "names": self.names(),
            "help": self.help()
        }

        self.input_content = ""
        self.request = {"request": None, "content": None}

        # Create message parser
        self.message_parser = MessageParser()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        message_receiver = MessageReceiver(self, self.connection)
        message_receiver.run()

        # Forever read user input
        while True:
            input_data = input("Input: ").split()
            self.input_content = input_data[1]
            if input_data[0] in self.possible_inputs:
                self.request["request"] = input_data[0]
                self.possible_inputs[input_data[0]]
            else:
                print("This is not a valid request")

    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        # Handle incoming message
        self.message_parser.parse(message)

    def send_payload(self):
        json_request = json.dumps(self.request)
        self.connection.sendall(json_request)

    def login(self, username):
        if len(username) <= 1:
            print("Please type in username after 'login'.")
        else:
            self.request["content"] = username
            self.send_payload()

    def logout(self):
        self.send_payload()

    def help(self):
        self.send_payload()

    def message(self, message):
        if len(message) <= 1:
            print("Please type in message after 'msg'.")
        else:
            self.request["content"] = message
            self.send_payload()

    def names(self):
        self.send_payload()

        # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
