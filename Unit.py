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

        # Am I carrying a resource? bool
        self.have_resource = None

        # Am I ready to attack again? bool
        self.can_attack = None

        # Number of turns before I can attack again
        self.attack_cooldown = None

        # The next turn I can receive a command on
        self.can_cmd_on = None

        # My Tasks. Each element is in format (TASK_ENUM, task_parameters)
        # So for the move task -> (MOVE_TASK, x_dest, y_dest)
        # for attack task -> (ATTACK_TASK, enemy_id)
        # for gather task -> (GATHER_TASK, resource_id)
        # ...
        self.task_list = None

        # My commands needed to complete my current task
        # {'command':'Move', 'unit':unit.id, 'dir':'N'}
        self.cmd_list = None

    def move_to(self, destination):
        # add move task to unit task list
        pass
    
    def move_in_dir(self, direction, distance):
        # compute dest for unit
        # call move unit for unit
        pass

    def attack_unit(self, enemy_id):
        # If next command in unit command list is an attack command,
        # will the attack succeed?
        # It would fail if the enemy unit is no longer in view or if enemy unit
        # has moved.
        # If enemy unit no longer in view, we need a new task.
        # If enemy unit in view but not in range (1 for worker, 5x5sq for tank),
        # then we need to insert some move commands before the attack command
        pass

    def collect_resource(self, resource_id):
        # Collect the resource and take it back to base.
        # Do this until the resource is empty.
        pass
    
    def is_task_complete(self):
        if self.cmd_list:
            return False
        else:
            return True
    
    def current_task_possible(self):
        # If task cannot complete, then self.cancel_current_task()
        pass
    
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
           delay = 1
        self.can_cmd_on = turn + delay
        # print(self.cmd_list[-1])
        return self.cmd_list.pop()
    
    def update_cmd_list(self):
        # given the unit's current task, set cmd_list equal to commands needed to
        # make sure the unit completes its task.
        # if the cmd_list goes empty then the unit will be reported as having
        # completed its task.
        pass
    
    def give_task(self, task):
        # If add task, then new task is given top priority.
        self.task_list.append(task)
        self.update_cmd_list()
    
    def cancel_current_task(self):
        # stop task
        # automatically start next task?
        pass
    
    def stop_all_tasks(self):
        self.task_list = []
        self.cmd_list = []