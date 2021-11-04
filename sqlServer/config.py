import json

class Config():
    def __init__(self, location):
        self.location = location

        self.config = json.load(open(location))