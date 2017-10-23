import random
from Path import *

# makes me want to play some AOEII

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

    def explore(self, map, unit_group):
        # Randomly visit unseen tiles within a radius of base.
        # If worker idle, select next random point from unseen tiles within
        # a radius of base (try in general direction of worker_point - base_point).

        # An initial path is chosen
        # Consider all None tiles in map to be not blocked
        # If obstacle, select new random point in the darkness
        # Restart

        # TODO neccessary optimizations
        # Cache path from resource to base ( a path could be a member of Resource class )
        # Only compute path in area where we have visited tiles
        pass

    def command_units(self, game_state):
        # Implement strategy
        # Harvest nearby resources until have enough units to destroy enemy base
        # If a unit has no task then it should be given a new task.

        # Idle workers
        # Busy workers
        #u = game_state.my_units[0]
        #if game_state.turn_counter == 0:
        #    u.cmd_list = [{'command':'MOVE', 'unit':u.id, 'dir':'S'}, {'command':'GATHER', 'unit':u.id, 'dir':'N'}, {'command':'MOVE', 'unit':u.id, 'dir':'N'}, {'command':'MOVE', 'unit':u.id, 'dir':'N'}]

        # TESTING
        for u in game_state.my_units:
           if game_state.turn_counter == 100:
               # Find path from base to unit
               dest = (u.x, u.y)
               start = game_state.indices(0, 0)
               path_finder = Path()
               path = path_finder.get_path(game_state.map, start, dest)
               u.cmd_list = []
               for p in zip(path, path[1:]):
                   Dir = ''
                   x = p[0][0] - p[1][0]
                   if x:
                       if x < 0:
                           Dir = 'E'
                       else:
                           Dir = 'W'
                   else:
                       y = p[0][1] - p[1][1]
                       if y > 0:
                           Dir = 'N'
                       else:
                           Dir = 'S'
                   u.cmd_list.insert(0, {'command':'MOVE', 'unit':u.id, 'dir':Dir})
               # game_state.path = path
               # game_state.print_world()
           elif game_state.turn_counter < 95:
               if u.did_complete_cmd():
                   if game_state.turn_counter % 2:
                       u.cmd_list = [{'command':'MOVE', 'unit':u.id, 'dir':['N','S','E','W'][u.id%4]}]
                   else:
                       u.cmd_list = [{'command':'MOVE', 'unit':u.id, 'dir':['N','S','E','W'][(int(random.random()*102)+u.id)%4]}]
        pass

    def build_units(self, game_state):
        # Build workers until we have a certain number of units.

        # Gives build task to my_base
        pass

    def get_commands_batch(self, game_state):
        # For each unit, remove unit.cmd_list[-1] and add it to the command batch.
        # order of commands in my_cmd_list does not matter.
        my_cmd_list = []
        turn = game_state.turn_counter
        for unit in game_state.my_units:
            if unit.did_complete_cmd() and unit.cmd_list and turn >= unit.can_cmd_on:
                my_cmd_list.append(unit.next_cmd(turn))

        if game_state.my_base.cmd_list:
            my_cmd_list.append(game_state.my_base.cmd_list.pop())

        cmd_bat = {'commands':my_cmd_list}
        return cmd_bat

    def act(self, game_state):
        # Update unit command queues
        self.build_units(game_state)
        self.command_units(game_state)

        cmd_bat = self.get_commands_batch(game_state)
        return cmd_bat
