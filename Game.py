import json
from Agent import *
from Unit import *
from Tile import *
from Constants import *

# It would be nice if the agent never had to mutate the game_state.

# TODO I had some errors when using [].index(.)

# When the agent targets an enemy from the enemy_list, be sure to check that the
# enemy's tile is visible, otherwise we can't be sure that the enemy is actually
# there (remove the entry in the enemy_list ? No, the enemy's unit count might be useful).

# when I get a tile update, is the visible bool true if an enemy unit
# that I can't see can see the tile?

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
        self.unit_types = {}

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
            self.unit_types[ut.name] = ut

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
        self.seen_base = False

        # A 2D list of tiles
        self.map = []
        self.min_observed_x = 10**6
        self.min_observed_y = 10**6
        self.max_observed_x = -10**6
        self.max_observed_y = -10**6

        # A list of Resource instances
        self.resource_piles = []
        self.resource_ids = []

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
        # TODO extract some functionality out of this function
        for tile in tile_updates:
            t = Tile()
            keys = tile.keys()

            x, y = self.indices(tile['x'], tile['y'])
            self.min_observed_x = min(self.min_observed_x, x)
            self.min_observed_y = min(self.min_observed_y, y)
            self.max_observed_x = max(self.max_observed_x, x)
            self.max_observed_y = max(self.max_observed_y, y)
            # non viewable tiles will not have any other keys because they're
            # under fog of war
            t.visible = bool(tile['visible'])

            if 'blocked' in keys:
                t.blocked = bool(tile['blocked'])
            elif self.map[y][x].blocked != None:
                # We don't want to loose this information when the tile becomes hidden.
                # (when blocked not in keys).
                t.blocked = self.map[y][x].blocked
            if t.blocked == None:
                print('No tile that has been viewed by a unit should have blocked that isnt a bool')
                exit(-1)

            # Updates about enemy units come with tile_updates
            if 'resources' in keys and tile['resources']:
                resource_di = tile['resources']
                r = Resource()
                r.id = resource_di['id']
                r.remaining = resource_di['total']
                # if r.remaining > 0:  This fixes a bug I think, I forget which one.
                if r.id not in self.resource_ids:
                    r.carry_amount = resource_di['value']
                    r.type = resource_di['type']
                    r.x, r.y = x, y
                    self.resource_ids.append(r.id)
                    self.resource_piles.append(r)
                t.resource_id = r.id
                t.blocked = True

            if 'resources' in keys and not t.resource_id and self.map[y][x]:
                t.resource_id = None
                rid = self.map[y][x].resource_id
                if rid in self.resource_ids:
                    indx = self.resource_ids.index(rid)
                    self.resource_ids.remove(rid)
                    self.resource_piles.remove(self.resource_piles[indx])

            # Updates about enemy units come with tile_updates
            if 'units' in keys:
                for enemy in tile['units']:
                    u = Unit()
                    u.player_id = enemy['player_id']
                    u.id = enemy['id']
                    u.type = self.game_info.unit_types[enemy['type']]
                    u.status = enemy['status']
                    u.health = enemy['health']
                    u.x, u.y = x, y

                    if u.type.name == 'base':
                        self.enemy_base = u
                    elif u.id not in self.enemy_unit_ids and u.status != 'dead':
                        self.enemy_unit_ids.append(u.id)
                        self.enemy_units.append(u)
                    else:
                        if self.enemy_unit_ids and u.id in self.enemy_unit_ids:
                            indx = self.enemy_unit_ids.index(u.id)
                        if u.status == 'dead':
                            if self.enemy_unit_ids and u.id in self.enemy_unit_ids:
                                self.enemy_unit_ids.remove(u.id)
                                self.enemy_units.remove(self.enemy_units[indx])
                        else:
                            self.enemy_units[indx] = u

            self.map[y][x] = t

    def update_my_units(self, unit_updates):
        for unit in unit_updates:
            u = Unit()
            u.id = unit['id']
            u.player_id = unit['player_id']
            u.type = self.game_info.unit_types[unit['type']]
            u.status = unit['status']
            u.x, u.y = self.indices(unit['x'], unit['y'])
            u.can_cmd_on = 0
            u.cmd_list = []
            u.task_list = []

            if 'attack_cooldown' in unit.keys():
                u.attack_cooldown = unit['attack_cooldown']
            if 'can_attack' in unit.keys():
                u.can_attack = bool(unit['can_attack'])
            if 'health' in unit.keys():
                u.health = unit['health']
            if 'resource' in unit.keys():
                u.resource = unit['resource']

            if u.type.name == 'base':
                # Dont over write command/task list
                if self.my_base:
                    u.can_cmd_on = self.my_base.can_cmd_on
                    u.task_list = self.my_base.task_list
                    u.cmd_list = self.my_base.cmd_list
                self.my_base = u
            elif u.id not in self.my_unit_ids and u.status != 'dead':
                self.my_unit_ids.append(unit['id'])
                self.my_units.append(u)
            else:
                if self.my_unit_ids and u.id in self.my_unit_ids:
                    indx = self.my_unit_ids.index(u.id)

                # Dont over write command/task list
                u.can_cmd_on = self.my_units[indx].can_cmd_on
                u.task_list = self.my_units[indx].task_list
                u.cmd_list = self.my_units[indx].cmd_list
                u.current_path = self.my_units[indx].current_path

                indx = self.my_unit_ids.index(u.id)
                if u.status == 'dead':
                    self.my_unit_ids.remove(u.id)
                    self.my_units.remove(self.my_units[indx])
                else:
                    self.my_units[indx] = u
    
    def print_world(self):
        u = self.my_units[0]
        pt = u.current_path
        for y,r in enumerate(self.map):
            for x,c in enumerate(r):
                if c and c.blocked:
                    print(',',end='')
                elif c and not c.blocked:
                    if x == u.x and y == u.y:
                        if pt and (x,y) in pt:
                            print('+',end='')
                        else:
                            print('<',end='')
                    else:
                        if (x,y) == (self.my_base.x, self.my_base.y):
                            print('H',end='')
                        elif pt and (x,y) in pt:
                            print('*',end='')
                        else:
                            print(' ',end='')
                else:
                    print('.', end='')
            print()


class Game:
    """Manages current game state. Updates game state when given a msg from the
    game server. Mediates between the Agent and the game server.
    """
    def __init__(self):
        self.agent = Agent()
        self.game_state = GameState()

    def parse_msg(self, msg):
        """Updates game_state for msg. msg is a dictionary."""
        # print(json.dumps(msg, indent=3, sort_keys=True))

        # Update time info
        if 'turn' in msg.keys():
            self.game_state.turn_counter = msg['turn']
        else:
            print("no turn key in msg")

        if 'time' in msg.keys():
            self.game_state.time_remaining = msg['time']
        else:
            print("no time key in msg")

        # Init GameInfo
        if 'turn' in msg.keys() and msg['turn'] == 0:
            self.game_state.set_game_info(msg['game_info'])
            self.game_state.init_map()
            self.game_state.player_id = msg['player']

        # Update GameState
        if 'tile_updates' in msg.keys():
            if msg['tile_updates']:
                self.game_state.update_tiles(msg['tile_updates'])
        else:
            print("no tile_updates key in msg")

        if 'unit_updates' in msg.keys():
            if msg['unit_updates']:
                self.game_state.update_my_units(msg['unit_updates'])
        else:
            print("no unit_updates key in msg")

    def get_cmd(self):
        # Get agent's response to observing the environment.
        response = self.agent.act(self.game_state)
        return response
