from copy import deepcopy
import random

from Path import *
from Tile import *
from Constants import *

# makes me want to play some AOEII

class Agent:
    def __init__(self):
        pass

    def spread_units(self, unit_group):
        # Compute mean point of group
        # Move units away from mean point
        # Move units who are closer together farther

        # This will require modifying the task of a unit.?
        #   If a unit is moving to B and I want it to move through A to B, then
        #   add move(A) to the top of the task list

        # The units must re-evaluate the move(B) task once move(A) task completes
        # The reason is that the path generated for units might no longer be valid
        # after the units leave the path

        # So, I can delete the cmd_list and replace it with the cmd_list for move(A)
        # Then once move(A) is completed, executing move(B) will generate a new cmd_list.
        pass

    def surround_enemy(self, units):
        pass
    
    def explore(self, game_state):

        # An initial unexplored point is chosen
        # Consider all None tiles in map to be not blocked
        # If unit encounters obstacle, unit task (to follow the path) cannot be
        # completed and unit becomes idle and is eventually given a new task

        min_x = game_state.min_observed_x-11
        min_y = game_state.min_observed_y-11
        max_x = game_state.max_observed_x+11
        max_y = game_state.max_observed_y+11

        unexplored_list = []
        min_x = max(min_x, 0)
        min_y = max(min_y, 0)
        max_x = min(max_x, len(game_state.map[0])-1)
        max_y = min(max_y, len(game_state.map)-1)
        for i in range(min_x, max_x):
           for j in range(min_y, max_y):
               if game_state.map[j][i] is None:
                   unexplored_list.append((i,j))
        random.shuffle(unexplored_list)

        if not unexplored_list:
            # TODO agent should handle this case
            for u in game_state.my_units:
                u.stop_task()
        else:
            for u in game_state.my_units:
                if u.has_task():
                    continue
                coord = unexplored_list.pop()
                u.give_task(MOVE_TASK, game_state, (coord[0], coord[1]))

    def build_units(self, game_state):
        # Gives build task to my_base
        if not game_state.my_base.has_task():
            if game_state.my_base.resource >= 100:
                game_state.my_base.give_task(BUILD_TASK, game_state, 'worker')

    def get_commands_batch(self, game_state):
        # order of commands in my_cmd_list does not matter.
        my_cmd_list = []
        turn = game_state.turn_counter
        for unit in game_state.my_units:
            if unit.did_complete_cmd() and unit.has_task() and turn >= unit.can_cmd_on:
                my_cmd_list.append(unit.next_cmd(turn))

        my_base = game_state.my_base
        if my_base.has_task():
            my_cmd_list.append(my_base.next_cmd(turn))

        cmd_bat = {'commands':my_cmd_list}
        return cmd_bat

    def harvest(self, game_state):
        if game_state.resource_ids:
            for i,u in enumerate(game_state.my_units):
                # Choose one of the first few
                if not u.has_task() and game_state.turn_counter >= u.can_cmd_on:
                    indx = i%min(3,len(game_state.resource_ids))
                    u.stop_task()
                    u.give_task(GATHER_TASK, game_state, game_state.resource_piles[indx])
    
    def ready_harvest(self, game_state):
        # Sort the resources based on their distance to homebase so that
        # I always harvest from the closest resources first.
        if game_state.resource_ids:
            home = (game_state.my_base.x,game_state.my_base.y)
            dist_list = []
            for i,r in enumerate(game_state.resource_piles):
                px = r.x - home[0]
                py = r.y - home[1]
                cost = math.sqrt(px**2+py**2)
                is_big = r.carry_amount > 10
                if is_big:
                    cost -= 10
                dist_list.append((cost, i))
            dist_list.sort()
            dist_list = dist_list[::-1]

            temp_piles = deepcopy(game_state.resource_piles)
            temp_ids = deepcopy(game_state.resource_ids)
            game_state.resource_ids = []
            game_state.resource_piles = []
            while dist_list:
                i = dist_list.pop()[1]
                game_state.resource_ids.append(temp_ids[i])
                game_state.resource_piles.append(temp_piles[i])


    def act(self, game_state):
        # Implement strategy
        # If on a map with little resources,
        # then prioritize finding and destroying the enemy base
        # If on a map with lots of resources,
        # then prioritize building tons of units, up to a threshold

        # In each phase, all units will have same task
        # While in explore mode
        #     build units
        #     explore with units until find resources
        #     if found enough resources then move too harvest phase
        #     if not found enough resources and explored greater than 60 percent
        #     then move to attack
        # While in harvest phase
        #     build units
        #     make sure all workers are on harvest task
        #     if have enough units or resources empty, then move to attack phase
        # While in attack phase
        #     build units
        #     explore until find enemy base
        #     find enemy base
        #     attack enemy base

        # If a unit cannot complete its task then that task should be canceled.
        for u in game_state.my_units:
            # If a unit has no task then it should be given a new task.
            if u.has_task():
                if not u.current_task_possible(game_state):
                    u.stop_task()
                    # print("Unit can't finish task, stopping")

        # TODO needs refactoring.
        #   (Agent mode management, impossible task management, apply direction to coordinate)

        # I've modified the code so that the sequence of modes the agent is in is
        # a function of the size of the map and the number of resources available
        # after / during initial exploration

        T = 50
        T2 = 200
        if game_state.turn_counter < T:
            self.explore(game_state)
            if len(game_state.resource_ids) > 5 or game_state.game_info.map_height < 23:
                T = game_state.turn_counter+1
        elif game_state.turn_counter == T:
            for u in game_state.my_units:
                u.stop_task()
            if len(game_state.resource_ids) > 2:
                self.ready_harvest(game_state)
            else:
                T2 = 50

        self.build_units(game_state)
        if game_state.turn_counter < T2:
            if not game_state.resource_ids:
                self.explore(game_state)
            else:
                self.harvest(game_state)
        elif game_state.enemy_base:
            if not game_state.seen_base:
                for u in game_state.my_units:
                    u.stop_task()
                game_state.seen_base = True

            x = game_state.enemy_base.x
            y = game_state.enemy_base.y
            dirs = [(x+1,y),
                    (x-1,y),
                    (x,y+1),
                    (x,y-1)]
            for u in game_state.my_units:
                if u.has_task():
                    continue
                # surround base randomly
                rand = int(random.random()*4)
                u.give_task(ATTACK_TASK, game_state, dirs[rand])
        else:
            # Now find base
            self.explore(game_state)

        # game_state.print_world()

        cmd_bat = self.get_commands_batch(game_state)
        return cmd_bat
