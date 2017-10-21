import json
from Agent import Agent
from Constants import *


class Resource:
    """Represents a harvestable resources on a tile."""
    def __init__(self):
        self.id = None

        # Position of resource relative to homebase
        self.x = None
        self.y = None

        # Small or large, enum
        self.type = None

        # Amount initially available
        self.total_avail = None

        # How much a unit can carry
        self.carry_amount = None


class Tile:
    """The type of object that units move across.
    GameState.map is a list of Tile instances.
    """
    def __init__(self):
        # Is tile within view of some friendly?
        # TODO when I get tile update, is the visible bool true if an enemy unit
        # that I can't see can see the tile?
        self.visible = None

        # Tile's position relative to homebase
        # self.x = None
        # self.y = None

        # Can units traverse tile?
        # If tile holds empty resource or dead ship then blocked should be False
        self.blocked = None

        # A resource id
        self.resource = None

        # List of unit ids
        self.enemies = None
        self.friends = None


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

        # enum
        self.attack_type = None

        # int
        self.attack_damage = None

        # int
        self.attack_cooldown_duration = None

        # bool
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

        # My unit type. An index into GameState.unit_types, int and enum
        self.type = None

        # My position relative to homebase, int
        self.x = None
        self.y = None

        # What command I'm currently executing, enum
        self.status = None

        # int
        self.health = None

        # Am I carrying a resource? bool
        self.resource = None

        # Am I ready to attack again? bool
        self.can_attack = None

        # Number of turns before I can attack again
        self.attack_cooldown = None


class GameInfo:
    """Contains info about the game such  as game duration, map size and
    the different types of units.
    """
    def __init__(self, game_info_di):
        self.singleton()

        self.game_duration = game_info_di['game_duration']
        self.map_height = game_info_di['map_height']
        self.map_width = game_info_di['map_width']
        self.turn_duration = game_info_di['turn_duration']
        self.unit_types = []

        # Get unit type information. Some fields are optional.
        unit_types_di = game_info_di['unit_info']
        for unit_name,unit_di in zip(unit_types_di.keys(), unit_types_di.values()):
            ut = UnitType()
            ut.name = unit_name
            ut.hitpoints = unit_di['hp']
            ut.sight_range = unit_di['range']
            if 'cost' in unit_di.keys():
                ut.make_cost = unit_di['cost']
            if 'create_time' in unit_di.keys():
                ut.make_time = unit_di['create_time']
            if 'speed' in unit_di.keys():
                ut.speed = unit_di['speed']
            if 'attack_type' in unit_di.keys():
                at_str = unit_di['attack_type']
                if at_str == 'melee':
                    ut.attack_type = MELEE_ATK
                else:
                    ut.attack_type = RANGE_ATK
            if 'attack_damage' in unit_di.keys():
                ut.attack_damage = unit_di['attack_damage']
            if 'attack_cooldown_duration' in unit_di.keys():
                ut.attack_cooldown_duration = unit_di['attack_cooldown_duration']
            if 'can_carry' in unit_di.keys():
                ut.can_harvest = bool(unit_di['can_carry'])
            self.unit_types.append(ut)

    initialized = False
    def singleton(self):
        if GameInfo.initialized:
            print("Don't create more than one instance of GameInfo")
            exit(0)
        GameInfo.initialized = True


class GameState:
    '''
    TODO
    store all coordinates as map array indices?
    '''
    def __init__(self):
        self.game_info = None

        self.turn_counter = None
        self.time_remaining = None

        # A list of Unit instances
        self.my_units = []
        self.my_unit_ids = []
        self.enemy_units = []
        self.enemy_unit_ids = []
        self.my_base = None
        self.enemy_base = None

        # A list of tiles
        self.map = []

        # A list of resource instances
        self.resource_piles = []
        # A cluster of resources
        self.resource_cluster = None

        # Are any units or buildings being attacked
        self.being_attacked = None

    def set_game_info(self, gi_dict):
        self.game_info = GameInfo(gi_dict)

    def update_tiles(self, tu_dict):
        #   Add any new tiles
        #   Update attributes of tile instances
        pass

    def update_units(self, unit_updates):
        for unit in unit_updates:
            u = Unit()
            u.id = unit['id']
            u.player_id = unit['player_id']
            u.type = unit['type']
            u.status = unit['status']

            if 'attack_cooldown' in unit.keys():
                u.attack_cooldown = unit['attack_cooldown']
            if 'can_attack' in unit.keys():
                u.can_attack = bool(unit['can_attack'])
            if 'health' in unit.keys():
                u.health = unit['health']
            if 'resource' in unit.keys():
                u.resource = unit['resource']
            if 'x' in unit.keys():
                u.x = unit['x']
            if 'y' in unit.keys():
                u.y = unit['y']

            # Convert to enums
            if u.type == 'base':
                u.type = BASE_UTP
            elif u.type == 'worker':
                u.type = WORKER_UTP
            elif u.type == 'scout':
                u.type = SCOUT_UTP
            elif u.type == 'tank':
                u.type = TANK_UTP

            if u.status == 'idle':
                u.status = IDLE_STAT
            elif u.status == 'moving':
                u.status = MOVING_STAT
            elif u.status == 'building':
                u.status = BUILDING_STAT
            elif u.status == 'dead':
                u.status = DEAD_STAT

            if u.type == BASE_UTP:
                if u.player_id == 0:
                    self.my_base = u
                else:
                    self.enemy_base = u

            unit_list = self.enemy_units
            unit_id_list = self.enemy_unit_ids
            if u.player_id == 0:
                unit_list = self.my_units
                unit_id_list = self.my_unit_ids

            if u.id not in unit_id_list:
                unit_id_list.append(unit['id'])
                unit_list.append(u)
            else:
                indx = unit_id_list.index(u.id)
                unit_list[indx] = u


class Game:
    """Contains info about current state of the game. Updates this info given a
    msg from the game server.
    """
    def __init__(self):
        self.agent = Agent()
        self.game_state = GameState()

    def parse_msg(self, msg):
        """Updates game_state for msg."""
        print(json.dumps(msg, indent=3, sort_keys=True))

        # Update time info
        self.game_state.turn_counter = msg['turn']
        self.game_state.time_remaining = msg['time']

        # Init GameInfo
        if msg['turn'] == 0:
            self.game_state.set_game_info(msg['game_info'])
        self.game_state.update_tiles(msg['tile_updates'])
        self.game_state.update_units(msg['unit_updates'])

    def get_cmd(self):
        # Get agent's response to observing the environment.
        response = self.agent.act(self.game_state)
        return response
