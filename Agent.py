class Agent:
    def __init__(self):
        pass

    def move_unit(self, unit, destination):
        pass

    def attack_unit(self, unit, enemy_id):
        # If next command in unit command list is an attack command,
        # will the attack succeed?
        # It would fail if the enemy unit is no longer in view or if enemy unit
        # has moved.
        # If enemy unit no longer in view, we need a new task.
        # If enemy unit in view but not in range (1 for worker, 5x5sq for tank),
        # then we need to insert some move commands before the attack command
        pass

    def collect_resource(self, unit, resource_id):
        pass

    def command_units(self, game_state):
        # Strategize given the game_state.
        # for each unit, update that unit's command list
        pass

    def build_units(self, game_state):
        pass

    def move_test(self, game_state):
        print('Turn: ', game_state.turn_counter)
        print(game_state.my_units[0].status)
        print()
        direction = 'N' if not game_state.my_units[0].resource else 'S'
        if direction == 'S':
            direction = 'N' if not game_state.my_units[0].status == 'idle' else 'S'
        elif direction == 'N':
            direction = 'S' if not game_state.my_units[0].status == 'idle' else 'N'
        cmd_list = []
        for ids in game_state.my_unit_ids:
            if game_state.my_units[game_state.my_unit_ids.index(ids)].status == 'idle':
                cmd_list.append({'command': 'MOVE', 'unit': ids, 'dir': direction})
                cmd_list.append({'command': 'GATHER', 'unit': ids, 'dir': direction})
                # cmd_list.append({'command': 'SHOOT', 'unit':ids,'dx':2, 'dy':2})
        command_batch = {'commands':cmd_list}
        return command_batch

    def get_commands_batch(self, game_state):
        # The worker goes to status idle at the 5th turn after the turn its move
        # command was issued on.
        # So on turn 0 I commanded a worker to move north
        # at turn 5 that worker went to status idle.
        # also on turn 5 I submitted a command to move north again
        # so I should expect the worker to complete that command and move north
        # on turn 10.

        # So if status idle then execute next command
        # ...

        cmd_bat = self.move_test(game_state)
        # For each unit, remove cmd_list[0] and add it to the command batch
        return cmd_bat

    def act(self, game_state):
        # Update unit command queues
        self.build_units(game_state)
        self.command_units(game_state)
        # Generate command list by poping off each units command queue.
        cmd_bat = self.get_commands_batch(game_state)
        return cmd_bat
