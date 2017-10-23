from Path import *
import random
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
        self.build_units(game_state)

        # An initial unexplored point is chosen
        # Consider all None tiles in map to be not blocked
        # If unit encounters obstacle, unit task cannot be completed and unit
        # becomes idle and is eventually given a new task

        # TODO only choose points from None tiles in rectangle bounding non-None tiles
        # Need ((bound_x), (bound_y)) which could be computed from tile_updates

        min_x = game_state.min_observed_x-5
        min_y = game_state.min_observed_y-5
        max_x = game_state.max_observed_x+5
        max_y = game_state.max_observed_y+5

        # For each unit
        points = []
        for u in game_state.my_units:
            if u.has_task():
                continue
            w = len(game_state.map[0])
            h = len(game_state.map)
            for i in range(1000):
                (x, y) = (random.uniform(min_x,max_x), random.uniform(min_y,max_y))
                y = int(min(max(y, 0), len(game_state.map)-1))
                x = int(min(max(x, 0), len(game_state.map[0])-1))
                if game_state.map[y][x] is None:
                    break
            u.give_task((MOVE_TASK, game_state.map, (x, y)))

    def build_units(self, game_state):
        # Gives build task to my_base
        if not game_state.my_base.has_task():
            if game_state.my_base.resource >= 100:
                game_state.my_base.give_task((BUILD_TASK, 'worker'))

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
                    print("Unit can't finish task, stopping")

        # Testing
        #if not game_state.my_units[0].has_task():
        #    game_state.my_units[0].give_task((MOVE_TASK, game_state.map, (7,9)))
        # game_state.print_world()
        #print(game_state.my_units[0].y)
        #print(game_state.my_units[0].x)

        T = 80
        if game_state.turn_counter < T:
            self.explore(game_state)
        elif game_state.resource_piles == T:
            for u in game_state.update_my_units:
                rx = game_state.resource_piles[0].x
                ry = game_state.resource_piles[0].y
                u.stop_task()
                u.give_task((GATHER_TASK, game_state.resource_piles))

            game_state.print_world()

        # if game_state.enemy_base:
        #     x = game_state.enemy_base.x
        #     y = game_state.enemy_base.y
        #     for u in game_state.my_units:
        #         if u.has_task():
        #             continue
        #         u.give_task((ATTACK_TASK, game_state.map, (x-1, y-1)))
        # else:
        #     self.explore(game_state)

        # self.explore(game_state)

        cmd_bat = self.get_commands_batch(game_state)
        return cmd_bat
