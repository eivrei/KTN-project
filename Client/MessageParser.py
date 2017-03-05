import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'history' : self.parse_history,
            'message' : self.parse_message
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = json.loads(payload) # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            raise NotImplementedError

    def parse_error(self, payload):
        raise NotImplementedError
    
    def parse_info(self, payload):
        raise NotImplementedError

    def parse_history(self, payload):
        raise NotImplementedError

    def parse_message(self, payload):
        raise NotImplementedError
    
    # Include more methods for handling the different responses... 
