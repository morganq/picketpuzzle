import json
FILENAME = "save.json"
class Save:
    def __init__(self):
        try:
            data = json.load(open(FILENAME, "r"))
        except:
            data = {}

        self.level_state = {int(k):v for k,v in data.get("level_state", {}).items()}

    def save(self):
        data = {
            'level_state': self.level_state
        }
        json.dump(data, open(FILENAME, "w"))

    def get_level_state(self, level_index):
        if level_index not in self.level_state:
            return {'beaten':False, 'steps':0, 'stars':0}

        else:
            return self.level_state[level_index]

    def set_level_state(self, level_index, beaten, steps, stars):
        self.level_state[level_index] = {'beaten':beaten, 'steps':steps, 'stars':stars}