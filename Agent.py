class Agent:
    def __init__(self):
        pass

    def spread_units(self, unit_group):
        # Might not do this

        # Spreads the units right now!

        # Compute mean point of group
        # Move units away from mean point
        # Move units who are closer together farther

        # This will require modifying the task of a unit.
        #   If a unit is moving to B and I want it to move through A to B, then
        #   add move(A) to the top of the task list

        # The units must re-evaluate the move(B) task once move(A) task completes
        # The reason is that the path generated for units might no longer be valid
        # after the units leave the path

        # So, I can delete the cmd_list and replace it with the cmd_list for move(A)
        # Then once move(A) is completed, executing move(B) will generate a new cmd_list.
        pass

    def surround_enemy(self, unit_group):
        pass

    def command_units(self, game_state):
        # Implement strategy
        # Harvest nearest resources until have enough units to destroy enemy base
        # If a unit has no task then it should be given a new task.

        # Idle workers
        # Busy workers
        pass

    def build_units(self, game_state):
        # Build workers until we have a certain number of units.

        # Gives build task to my_base
        pass

    def get_commands_batch(self, game_state):
        # For each unit, remove unit.cmd_list[-1] and add it to the command batch.
        # order of commands in my_cmd_list does not matter.
        my_cmd_list = []
        for unit in game_state.my_units:
            if unit.did_complete_cmd() and unit.cmd_list:
                my_cmd_list.append(unit.cmd_list.pop())

        if game_state.my_base.cmd_list:
            my_cmd_list.append(game_state.my_base.cmd_list.pop())

        # print(cmd_list)

        cmd_bat = {'commands':my_cmd_list}
        return cmd_bat

    def act(self, game_state):
        # Update unit command queues
        self.build_units(game_state)
        self.command_units(game_state)

        cmd_bat = self.get_commands_batch(game_state)
        return cmd_bat
