import json
class JSONHandler():
    def __init__(self, path):
        self.path = path

    def load_data(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_data(self, data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)