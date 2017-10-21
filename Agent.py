class Agent:
    def __init__(self):
        pass

    def get_random_move(self, gate_state):
        pass

    def move_all(self, game_state):
        # units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        # self.units |= units # add any additional ids we encounter

        # Move Unit(id, direction)
        # {'command': 'MOVE', 'unit': 6, 'dir': 'E'},

        command_batch = {'commands':[{'command': 'MOVE', 'unit': 6, 'dir': 'S'}]}
        return command_batch

    def act(self, game_state):
        # Generate command list
        return self.move_all(game_state)
