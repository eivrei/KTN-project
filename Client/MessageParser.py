import json


class MessageParser:
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'history': self.parse_history,
            'message': self.parse_message
        }

    # payload = {'timestamp': <timestamp>, 'sender': <username>, 'response': <response>, 'content': <content>}
    def parse(self, payload):
        payload = json.loads(payload)  # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            raise NotImplementedError

    # Methods for handling the different responses
    def parse_error(self, payload):
        print(payload["content"])

    def parse_info(self, payload):
        print(payload["content"])

    def parse_history(self, payload):
        print(payload[0] + ": " + payload[1] + ": " + payload[3])

    def parse_message(self, payload):
        print(payload[0] + ": " + payload[1] + ": " + payload[3])
