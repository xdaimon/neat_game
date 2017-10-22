import json
from Agent import Agent
from Constants import *

### TODO ###
# it would be nice if the agent never had to mutate the game_state.
# When the agent targets an enemy from the enemy_list, be sure to check that the
# enemy's tile is visible, otherwise we can't be sure that the enemy is actually
# there (remove the entry in the enemy_list ? No, the enemy's unit count might be useful).

# when I get a tile update, is the visible bool true if an enemy unit
# that I can't see can see the tile?

class Resource:
    """Represents a harvestable resources on a tile."""
    def __init__(self):
        self.id = None

        # Position of resource, map array indices
        self.x = None
        self.y = None

        # Small or large, enum
        self.type = None

        # Remaining resources
        self.remaining = None

        # How much a unit can carry
        self.carry_amount = None


class Tile:
    """The type of object that units move across.
    game_state.map is a 2D list of Tile instances.
    """
    def __init__(self):
        # Is tile within view of some friendly?
        self.visible = None

        # Tile's position, map array indices
        # self.x = None
        # self.y = None

        # Can units traverse tile?
        # If tile holds empty resource or dead ship then blocked should be False
        self.blocked = None

        # A resource id
        self.resource_id = None

        # List of unit ids
        self.enemy_ids = None


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

        # My unit type. An index into GameState.unit_types, int and enum
        self.type = None

        # My position, map array indices
        self.x = None
        self.y = None

        # What command I'm currently executing
        self.status = None

        # The id of the game entity that I'm targeting (resource_id or enemy_id)
        self.target = None

        self.health = None

        # Am I carrying a resource? bool
        self.resource = None

        # Am I ready to attack again? bool
        self.can_attack = None

        # Number of turns before I can attack again
        self.attack_cooldown = None

        # My command list
        self.cmd_list = None


class GameInfo:
    """Contains info about the game such  as game duration, map size and
    the different types of units.

    attack_cooldown_duration is 3 in README but 30 in json msg.
    build_time is 5 in README but 50 in json msg.
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
        for unit_type in unit_types_di.keys():
            ut = UnitType()
            ut.name = unit_type
            unit_di = unit_types_di[unit_type]
            ut.hitpoints = unit_di['hp']
            ut.sight_range = unit_di['range']
            keys = unit_di.keys()
            if 'cost' in keys:
                ut.make_cost = unit_di['cost']
            if 'create_time' in keys:
                ut.make_time = unit_di['create_time']
            if 'speed' in keys:
                ut.speed = unit_di['speed']
            if 'attack_type' in keys:
                ut.attack_type = unit_di['attack_type']
            if 'attack_damage' in keys:
                ut.attack_damage = unit_di['attack_damage']
            if 'attack_cooldown_duration' in keys:
                ut.attack_cooldown_duration = unit_di['attack_cooldown_duration']
            if 'can_carry' in keys:
                ut.can_harvest = bool(unit_di['can_carry'])
            self.unit_types.append(ut)

    initialized = False
    def singleton(self):
        if GameInfo.initialized:
            print("Don't create more than one instance of GameInfo")
            exit(0)
        GameInfo.initialized = True


class GameState:
    def __init__(self):
        self.game_info = None
        self.player_id = None

        self.turn_counter = None
        self.time_remaining = None

        # A list of Unit instances
        self.my_units = []
        self.my_unit_ids = []
        self.enemy_units = []
        self.enemy_unit_ids = []
        self.my_base = None
        self.enemy_base = None

        # A 2D list of tiles
        self.map = []

        # A list of Resource instances
        self.resource_piles = []
        self.resource_ids = []

        # Are any units or buildings being attacked
        self.being_attacked = None

    def indices(self, x_rel, y_rel):
        """Convert a pair of relative coordinates to map indices where
        (x_rel, y_rel) == (0,0) maps to (w, h), that is to the center of the map
        array (of size (2w+1, 2h+1).
        """
        w = self.game_info.map_width
        h = self.game_info.map_height
        return (x_rel + w, y_rel + h)

    def set_game_info(self, gi_di):
        self.game_info = GameInfo(gi_di)

    def init_map(self):
        w = self.game_info.map_width
        h = self.game_info.map_height
        w, h = self.indices(w, h)
        # There will always be a middle tile in map.
        # We will place the homebase there.
        w += 1
        h += 1
        self.map = [[None]*w for h in range(h)]

    def update_tiles(self, tile_updates):
        for tile in tile_updates:
            t = Tile()
            keys = tile.keys()

            x, y = self.indices(tile['x'], tile['y'])
            # non viewable tiles will not have any other keys because they're
            # under fog of war
            t.visible = bool(tile['visible'])

            if 'blocked' in keys:
                t.blocked = bool(tile['blocked'])

            if 'resources' in keys and tile['resources']:
                resource_di = tile['resources']
                r = Resource()
                r.id = resource_di['id']
                r.remaining = resource_di['total']
                if r.remaining > 0:
                    if r.id not in self.resource_ids:
                        r.carry_amount = resource_di['value']
                        r.type = resource_di['type']
                        r.x, r.y = x, y
                        self.resource_ids.append(r.id)
                        self.resource_piles.append(r)
                    t.resource_id = r.id
                else:
                    t.resource_id = None
                    if r.id in self.resource_ids:
                        indx = self.resource_ids.index(r.id)
                        self.resource_ids.remove(r.id)
                        self.resource_piles.remove(self.resource_piles[indx])

            if 'units' in keys:
                for enemy in tile['units']:
                    u = Unit()
                    u.player_id = enemy['player_id']
                    u.id = enemy['id']
                    u.type = enemy['type']
                    u.status = enemy['status']
                    u.health = enemy['health']
                    u.x, u.y = x, y

                    if u.type == 'base':
                        self.enemy_base = u
                    elif u.id not in self.enemy_unit_ids and u.status != 'dead':
                        self.enemy_unit_ids.append(u.id)
                        self.enemy_units.append(u)
                    else:
                        indx = self.enemy_unit_ids.index(u.id)
                        if u.status == 'dead':
                            self.enemy_unit_ids.remove(u.id)
                            self.enemy_units.remove(self.enemy_units[indx])
                        else:
                            self.enemy_units[indx] = u

            self.map[y][x] = t

    def update_unit(self, u, base, unit_ids, unit_list):
        if u.type == 'base':
            # Dont over write command list
            if base:
                u.cmd_list = base.cmd_list
            base = u
        elif u.id not in unit_ids and u.status != 'dead':
            unit_ids.append(u.id)
            unit_list.append(u)
        else:
            # Dont over write command list or target
            indx = unit_ids.index(u.id)
            u.cmd_list = unit_list[indx].cmd_list
            u.target = unit_list[indx].target
            if u.status == 'dead':
                unit_ids.remove(u.id)
                unit_list.remove(unit_list[indx])
            else:
                unit_list[indx] = u

    def init_unit(self, unit_di):
        """Make a unit instance given the unit_di."""
        u = Unit()
        u.id = unit_di['id']
        u.player_id = unit_di['player_id']
        u.type = unit_di['type']
        u.status = unit_di['status']
        u.x, u.y = self.indices(unit_di['x'], unit_di['y'])

        keys = unit_di.keys()
        if 'attack_cooldown' in keys:
            u.attack_cooldown = unit_di['attack_cooldown']
        if 'can_attack' in keys:
            u.can_attack = bool(unit_di['can_attack'])
        if 'health' in keys:
            u.health = unit_di['health']
        if 'resource' in keys:
            u.resource = unit_di['resource']

        return u

    def update_my_units(self, unit_updates_di):
        for unit_di in unit_updates_di:
            u = self.init_unit(unit_di)
            self.update_unit(u, self.my_base, self.my_unit_ids, self.my_units)


class Game:
    """Manages current game state. Updates game state when given a msg from the
    game server.
    """
    def __init__(self):
        self.agent = Agent()
        self.game_state = GameState()

    def parse_msg(self, msg):
        """Updates game_state for msg.
        msg is a dictionary."""
        # print(json.dumps(msg, indent=3, sort_keys=True))

        # Update time info
        self.game_state.turn_counter = msg['turn']
        self.game_state.time_remaining = msg['time']

        # Init GameInfo
        if msg['turn'] == 0:
            self.game_state.set_game_info(msg['game_info'])
            self.game_state.init_map()
            self.game_state.player_id = msg['player']

        # Update GameState
        if msg['tile_updates']:
            self.game_state.update_tiles(msg['tile_updates'])
        if msg['unit_updates']:
            self.game_state.update_my_units(msg['unit_updates'])

    def get_cmd(self):
        # Get agent's response to observing the environment.
        response = self.agent.act(self.game_state)
        return response
