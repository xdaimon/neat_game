from Constants import *
from Path import *
from Tile import *

class UnitType:
    """Contains information about each type of unit in the game.
    Not every unit has a certain attribute."""
    def __init__(self):
        self.name = ''
        self.hitpoints = None
        self.sight_range = None
        self.make_cost = None
        self.make_time = None
        self.speed = None
        self.attack_type = None
        self.attack_damage = None
        self.attack_cooldown_duration = None
        self.can_harvest = None

class Unit:
    """Information about a specific unit instance.
    Not every unit has a certain attribute.
    Instances of Unit are held in GameState.my_units and GameState.enemy_units.
    Indices to these lists of instances will be found in the game map tiles.
    """
    def __init__(self):
        # Who I belong to, int
        self.player_id = None

        # My identity, int
        self.id = None

        # My unit type
        self.type = None

        # My position, map array indices
        self.x = None
        self.y = None

        # What command I'm currently executing
        self.status = None

        self.health = None

        # How much resources am I carrying?
        self.resource = None

        # Am I ready to attack again? bool
        self.can_attack = None

        # Number of turns before I can attack again
        self.attack_cooldown = None

        # The next turn I can receive a command on
        self.can_cmd_on = None

        # My Tasks. Each element is in format (TASK_ENUM, task_parameters)
        # So for the move task -> (MOVE_TASK, map, (x_dest, y_dest))
        # for attack task -> (ATTACK_TASK, enemy_id)
        # for gather task -> (GATHER_TASK, resource_id)
        # ...
        self.task_list = None

        # My commands needed to complete my current task
        # {'command':'Move', 'unit':unit.id, 'dir':'N'}
        self.cmd_list = None

        # debuging
        self.current_path = None

    def follow_path(self, path):
        self.current_path = path
        for p in zip(path, path[1:]):
            direction = ''
            x = p[0][0] - p[1][0]
            if x:
                if x < 0:
                    direction = 'E'
                else:
                    direction = 'W'
            else:
                y = p[0][1] - p[1][1]
                if y > 0:
                    direction = 'N'
                else:
                    direction = 'S'
            self.cmd_list.insert(0, {'command':'MOVE', 'unit': self.id, 'dir': direction})

    def move_to(self, units, my_map, destination):
        start = (self.x, self.y)
        self.follow_path(Path().get_path(units, my_map, start, destination))

    def move(self, my_map, start, destination):
        self.follow_path(Path().get_path(None, my_map, start, destination))
    
    #def move_in_dir(self, map, direction, distance):
    #    # compute dest for unit
    #    # call move unit for unit
    #    pass

    def attack_unit(self, enemy_id):
        # If next command in unit command list is an attack command,
        # will the attack succeed?
        # It would fail if the enemy unit is no longer in view or if enemy unit
        # has moved.
        # If enemy unit no longer in view, we need a new task.
        # If enemy unit in view but not in range (1 for worker, 5x5sq for tank),
        # then we need to insert some move commands before the attack command
        pass

    def collect_resource(self):
        # Collect the resource and take it back to base.
        # Do this until the resource is empty.
        pass

    def tile_in_front(self, game_state):
        if self.cmd_list:
            if 'dir' in self.cmd_list[-1].keys():
                direction = self.cmd_list[-1]['dir']
                # check if unit obstructed
                if direction == 'N':
                    tile = game_state.map[self.y-1][self.x]
                elif direction == 'E':
                    tile = game_state.map[self.y][self.x+1]
                elif direction == 'S':
                    tile = game_state.map[self.y+1][self.x]
                elif direction == 'W':
                    tile = game_state.map[self.y][self.x-1]
                return tile


    def current_task_possible(self, game_state):
        if self.has_task():
            task = self.task_list[-1][0]
            param = self.task_list[-1][1]
            if task == MOVE_TASK:
                tile = self.tile_in_front(game_state)
                # MOVE_TASK is used for exploration
                # so if we've already seen the tile we are headed towards, then
                # find a new tile to discover
                if game_state.map[param[1]][param[0]]:
                    return False
                if not tile:
                    print('tile in front is still None')
                    exit(-1)
                else:
                    return not tile.blocked
            if task == BUILD_TASK:
                unit_type = param
                cost = 0
                if unit_type == 'worker':
                    cost = 100
                elif unit_type == 'scout':
                    cost = 130
                elif unit_type == 'tank':
                    cost = 150
                # if not enough resources
                if game_state.my_base.resource < cost:
                    return False
                else:
                    return True
            if task == GATHER_TASK:
                resource = param
                if resource.remaining == 0:
                    return False
                else:
                    return True
            if task == ATTACK_TASK:
                tile = self.tile_in_front(game_state)
                # MOVE_TASK is used for exploration
                # so if we've already seen the tile we are headed towards, then
                # find a new tile to discover
                if tile:
                    return not tile.blocked
                else:
                    return True
    
    def has_task(self):
        if self.task_list:
            return True
        else:
            return False
    
    def did_complete_cmd(self):
        # The worker goes to status idle at the 5th turn after the turn its move
        # command was issued on.
        # So on turn 0 I commanded a worker to move north
        # at turn 5 that worker's status became 'idle'
        # also on turn 5 I submitted a command to move north again
        # so I should expect the worker to complete that command and move north
        # on turn 10.

        # So if status idle then execute next command
        # ...
        if self.status == 'idle':
            return True
        else:
            return False
    
    def next_cmd(self, turn):
        cmd = self.cmd_list[-1]['command']
        delay = 0
        if cmd == 'MOVE':
           delay = self.type.speed
        elif cmd in ['MELEE', 'SHOOT']:
           delay = self.type.attack_cooldown_duration//10
        elif cmd == 'CREATE':
           unit = self.cmd_list[-1]['type']
           if unit == 'tank':
               delay = 15
           elif unit == 'scout':
               delay = 10
           else:
               delay = 5
        elif cmd == 'GATHER':
           delay = 2
        self.can_cmd_on = turn + delay

        next_cmd = self.cmd_list.pop()
        
        # did we finish task?
        if not self.cmd_list:
            self.task_list = []

        return next_cmd

    def give_task(self, task, game_state, param):
        self.stop_task()
        self.task_list.append((task, param))

        if task == BUILD_TASK:
            if self.type.name == 'base':
                self.cmd_list = [ {'command':'CREATE', 'type': param} ]
            else:
                print("Tried to issue build command on non base unit")
        elif task == MOVE_TASK:
            self.move_to(game_state.my_units, game_state.map, param)
        elif task == ATTACK_TASK:
            loc_of_attack = param
            self.move_to(game_state.my_units, game_state.map, loc_of_attack)
            for x in range(50):
                self.cmd_list.insert(0, {'command':'MELEE', 'unit':self.id, 'target':game_state.enemy_base.id})
        elif task == GATHER_TASK:
            resource = param
            home = (game_state.my_base.x,game_state.my_base.y)
            (x,y) = (resource.x, resource.y)
            (x,y) = get_non_blocked_neighbor(game_state.map, (x,y), home)
            self.move_to(None, game_state.map, (x,y))
            dirs = ['N','S','E','W']
            for d in dirs:
               self.cmd_list.insert(0, {'command':'GATHER', 'unit':self.id, 'dir':d})
            self.move(game_state.map, (x,y), home)
    
    def stop_task(self):
        self.task_list = []
        self.cmd_list = []