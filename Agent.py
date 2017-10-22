class Agent:
    def __init__(self):
        pass

    def get_random_move(self, gate_state):
        pass

    def move_test(self, game_state):
        direction = 'N' if not game_state.my_units[0].resource else 'S'
        cmd_list = []
        for ids in game_state.my_unit_ids:
            cmd_list.append({'command': 'MOVE', 'unit': ids, 'dir': direction})
            cmd_list.append({'command': 'GATHER', 'unit': ids, 'dir': direction})
            # cmd_list.append({'command': 'CREATE', 'type':'worker'})
        command_batch = {'commands':cmd_list}

        return command_batch

    def act(self, game_state):
        # Generate command list
        return self.move_test(game_state)
