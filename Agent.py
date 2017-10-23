from Path import *
from Tile import *
import random
from copy import deepcopy
from Constants import *

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

    def surround_enemy(self, units):
        pass
    
    def explore(self, game_state):

        # An initial unexplored point is chosen
        # Consider all None tiles in map to be not blocked
        # If unit encounters obstacle, unit task cannot be completed and unit
        # becomes idle and is eventually given a new task

        # TODO only choose points from None tiles in rectangle bounding non-None tiles
        # Need ((bound_x), (bound_y)) which could be computed from tile_updates

        min_x = game_state.min_observed_x-11
        min_y = game_state.min_observed_y-11
        max_x = game_state.max_observed_x+11
        max_y = game_state.max_observed_y+11

        # point a vector from home to the mean
        mid_x = (min_x + max_x)/2
        mid_y = (min_y + max_y)/2
        home_x = game_state.my_base.x
        home_y = game_state.my_base.y
        dif_x = 1.5*(mid_x - home_x)
        dif_y = 1.5*(mid_y - home_y)

        # For each unit
        points = []
        for u in game_state.my_units:
            if u.has_task():
                continue
            w = len(game_state.map[0])
            h = len(game_state.map)
            for i in range(1000):
                (x, y) = (random.uniform(min_x,max_x), random.uniform(min_y,max_y))
                y = int(min(max(y+dif_y, 0), len(game_state.map)-1))
                x = int(min(max(x+dif_x, 0), len(game_state.map[0])-1))
                if game_state.map[y][x] is None:
                    break
            u.give_task(MOVE_TASK, game_state, (x, y))

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
        # I always harvest from the closest resources first.j
        if game_state.resource_ids:
            home = (game_state.my_base.x,game_state.my_base.y)
            dist_list = []
            for i,r in enumerate(game_state.resource_piles):
                px = r.x - home[0]
                py = r.y - home[1]
                dist_list.append((math.sqrt(px**2+py**2), i))
            dist_list.sort()
            dist_list = dist_list[::-1]

            temp_piles = deepcopy(game_state.resource_piles)
            temp_ids = deepcopy(game_state.resource_ids)
            j = 0
            while dist_list:
                i = dist_list.pop()[1]
                game_state.resource_ids[i] = temp_ids[j]
                game_state.resource_piles[i] = temp_piles[j]
                j+=1


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

        # Testing
        #if not game_state.my_units[0].has_task():
        #    game_state.my_units[0].give_task(MOVE_TASK, game_state, (7,9)
        # game_state.print_world()
        #print(game_state.my_units[0].y)
        #print(game_state.my_units[0].x)

        T = 50
        if game_state.turn_counter < T:
            self.explore(game_state)
        elif game_state.turn_counter == T:
            for u in game_state.my_units:
                u.stop_task()
            self.ready_harvest(game_state)

        self.build_units(game_state)
        if game_state.turn_counter < 500:
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
