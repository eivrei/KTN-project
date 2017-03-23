# -*- coding: utf-8 -*-
import json
import socket
from client.MessageParser import MessageParser
from client.MessageReceiver import MessageReceiver


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

        # Set host and port
        self.host = host
        self.server_port = server_port

        # Set valid inputs
        self.possible_inputs = {
            "login": self.login,
            "logout": self.logout,
            "msg": self.message,
            "names": self.names,
            "help": self.help
        }

        self.input_content = ""
        self.request = {"request": None, "content": None}

        # Create message parser
        self.message_parser = MessageParser()

        # Run server
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        message_receiver = MessageReceiver(self, self.connection)

        # Forever read user input
        while True:
            input_data = input("Input: ").split()
            if input_data[0] in self.possible_inputs:
                self.possible_inputs[input_data[0]](input_data)
                message_receiver.run()
                print()
            else:
                print("This is not a valid request. Try again.")

    def disconnect(self):
        self.connection.shutdown(1)
        self.connection.close()
        print("You are now disconnected")

    def receive_message(self, message):
        # Handle incoming message
        self.message_parser.parse(message.decode())

    def send_payload(self):
        json_request = json.dumps(self.request)
        self.connection.sendall(json_request.encode())

    def login(self, input_data):
        if len(input_data) <= 1:
            print("Please type in username after 'login'.")
        else:
            self.set_request(input_data[0])
            self.request["content"] = input_data[1]
            self.send_payload()

    def logout(self, input_data):
        self.set_request(input_data[0])
        self.send_payload()
        # self.disconnect()

    def help(self, input_data):
        self.set_request(input_data[0])
        self.send_payload()

    def message(self, input_data):
        if len(input_data) <= 1:
            print("Please type in message after 'msg'.")
        else:
            self.set_request(input_data[0])
            self.request["content"] = " ".join(word for word in input_data[1:])
            self.send_payload()

    def names(self, input_data):
        self.set_request(input_data[0])
        self.send_payload()

    def set_request(self, input_data):
        self.request["request"] = input_data


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
