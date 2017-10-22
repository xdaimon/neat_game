from Game import Game
from Constants import *

# Submit data to Game
# Verify that Game parses data correctly

game_info = {
   "game_info": {
      "game_duration": 300000,
      "map_height": 32,
      "map_width": 32,
      "turn_duration": 200,
      "unit_info": {
         "base": {
            "hp": 300,
            "range": 2
         },
         "scout": {
            "attack_cooldown_duration": 30,
            "attack_damage": 1,
            "attack_type": "melee",
            "cost": 130,
            "create_time": 100,
            "hp": 5,
            "range": 5,
            "speed": 3
         },
         "tank": {
            "attack_cooldown_duration": 70,
            "attack_damage": 4,
            "attack_type": "ranged",
            "cost": 150,
            "create_time": 150,
            "hp": 30,
            "range": 2,
            "speed": 10
         },
         "worker": {
            "attack_cooldown_duration": 30,
            "attack_damage": 2,
            "attack_type": "melee",
            "can_carry": True,
            "cost": 100,
            "create_time": 50,
            "hp": 10,
            "range": 2,
            "speed": 5
         }
      }
   },
   "player": 0,
   "tile_updates": [
      {
         "blocked": True,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -2,
         "y": -2
      },
      {
         "blocked": True,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -2,
         "y": -1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -2,
         "y": 0
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -2,
         "y": 1
      },
      {
         "blocked": True,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -2,
         "y": 2
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -1,
         "y": -2
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -1,
         "y": -1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -1,
         "y": 0
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -1,
         "y": 1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": -1,
         "y": 2
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 0,
         "y": -2
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 0,
         "y": -1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 0,
         "y": 0
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 0,
         "y": 1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 0,
         "y": 2
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 1,
         "y": -2
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 1,
         "y": -1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 1,
         "y": 0
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 1,
         "y": 1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 1,
         "y": 2
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 2,
         "y": -2
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 2,
         "y": -1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 2,
         "y": 0
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 2,
         "y": 1
      },
      {
         "blocked": False,
         "resources": None,
         "units": [],
         "visible": True,
         "x": 2,
         "y": 2
      }
   ],
   "time": 299820,
   "turn": 0,
   "unit_updates": [
      {
         "health": 300,
         "id": 5,
         "player_id": 0,
         "resource": 750,
         "status": "idle",
         "type": "base",
         "x": 0,
         "y": 0
      },
      {
         "attack_cooldown": 0,
         "attack_cooldown_duration": 30,
         "attack_damage": 2,
         "attack_type": "melee",
         "can_attack": True,
         "health": 10,
         "id": 6,
         "player_id": 0,
         "range": 2,
         "resource": 0,
         "speed": 5,
         "status": "idle",
         "type": "worker",
         "x": 0,
         "y": 0
      },
      {
         "attack_cooldown": 0,
         "attack_cooldown_duration": 30,
         "attack_damage": 2,
         "attack_type": "melee",
         "can_attack": True,
         "health": 10,
         "id": 7,
         "player_id": 0,
         "range": 2,
         "resource": 0,
         "speed": 5,
         "status": "idle",
         "type": "worker",
         "x": 0,
         "y": 0
      },
      {
         "attack_cooldown": 0,
         "attack_cooldown_duration": 30,
         "attack_damage": 2,
         "attack_type": "melee",
         "can_attack": True,
         "health": 10,
         "id": 8,
         "player_id": 0,
         "range": 2,
         "resource": 0,
         "speed": 5,
         "status": "idle",
         "type": "worker",
         "x": 0,
         "y": 0
      },
      {
         "attack_cooldown": 0,
         "attack_cooldown_duration": 30,
         "attack_damage": 2,
         "attack_type": "melee",
         "can_attack": True,
         "health": 10,
         "id": 9,
         "player_id": 0,
         "range": 2,
         "resource": 0,
         "speed": 5,
         "status": "idle",
         "type": "worker",
         "x": 0,
         "y": 0
      },
      {
         "attack_cooldown": 0,
         "attack_cooldown_duration": 30,
         "attack_damage": 2,
         "attack_type": "melee",
         "can_attack": True,
         "health": 10,
         "id": 10,
         "player_id": 0,
         "range": 2,
         "resource": 0,
         "speed": 5,
         "status": "idle",
         "type": "worker",
         "x": 0,
         "y": 0
      },
      {
         "attack_cooldown": 0,
         "attack_cooldown_duration": 30,
         "attack_damage": 2,
         "attack_type": "melee",
         "can_attack": True,
         "health": 10,
         "id": 11,
         "player_id": 0,
         "range": 2,
         "resource": 0,
         "speed": 5,
         "status": "idle",
         "type": "worker",
         "x": 0,
         "y": 0
      }
   ]
}


test1 = {
    "player": 0,
    "tile_updates": [],
    "time": 299420,
    "turn": 2,
    "unit_updates": [
    {
        "attack_cooldown": 0,
        "attack_cooldown_duration": 30,
        "attack_damage": 2,
        "attack_type": "melee",
        "can_attack": True,
        "health": 10,
        "id": 6,
        "player_id": 0,
        "range": 2,
        "resource": 0,
        "speed": 5,
        "status": "moving",
        "type": "worker",
        "x": 0,
        "y": 0
    },
    {
        "attack_cooldown": 0,
        "attack_cooldown_duration": 30,
        "attack_damage": 2,
        "attack_type": "melee",
        "can_attack": True,
        "health": 10,
        "id": 7,
        "player_id": 0,
        "range": 2,
        "resource": 0,
        "speed": 5,
        "status": "moving",
        "type": "worker",
        "x": 0,
        "y": 0
    },
    {
        "attack_cooldown": 0,
        "attack_cooldown_duration": 30,
        "attack_damage": 2,
        "attack_type": "melee",
        "can_attack": True,
        "health": 10,
        "id": 8,
        "player_id": 0,
        "range": 2,
        "resource": 0,
        "speed": 5,
        "status": "moving",
        "type": "worker",
        "x": 0,
        "y": 0
    },
    {
        "attack_cooldown": 0,
        "attack_cooldown_duration": 30,
        "attack_damage": 2,
        "attack_type": "melee",
        "can_attack": True,
        "health": 10,
        "id": 9,
        "player_id": 0,
        "range": 2,
        "resource": 0,
        "speed": 5,
        "status": "moving",
        "type": "worker",
        "x": 0,
        "y": 0
    },
    {
        "attack_cooldown": 0,
        "attack_cooldown_duration": 30,
        "attack_damage": 2,
        "attack_type": "melee",
        "can_attack": True,
        "health": 10,
        "id": 10,
        "player_id": 0,
        "range": 2,
        "resource": 0,
        "speed": 5,
        "status": "moving",
        "type": "worker",
        "x": 0,
        "y": 0
    },
    {
        "attack_cooldown": 0,
        "attack_cooldown_duration": 30,
        "attack_damage": 2,
        "attack_type": "melee",
        "can_attack": True,
        "health": 10,
        "id": 11,
        "player_id": 0,
        "range": 2,
        "resource": 0,
        "speed": 5,
        "status": "moving",
        "type": "worker",
        "x": 0,
        "y": 0
    }]
}

def test():
    game = Game()
    # necessary game_info message
    game.parse_msg(game_info)

    # Test Game info
    gi = game.game_state.game_info
    if len(gi.unit_types) != 4:
        print("unit_types length failed test")
        return

    for ut in gi.unit_types:
        fail = False
        uinfo = (ut.make_cost,
                ut.sight_range,
                ut.speed,
                ut.hitpoints,
                ut.attack_cooldown_duration,
                ut.attack_damage,
                ut.make_time)
        if ut.name == 'worker':
            if uinfo != (100, 2, 5, 10, 30, 2, 50):
                fail = True
        elif ut.name == 'scout':
            if uinfo != (130, 5, 3, 5, 30, 1, 100):
                fail = True
        elif ut.name == 'tank':
            if uinfo != (150, 2, 10, 30, 70, 4, 150):
                fail = True
        elif ut.name == 'base':
            if uinfo != (None, 2, None, 300, None, None, None):
                fail = True

        if fail:
            print("ut.name:", ut.name)
            print("ut.make_cost:", ut.make_cost)
            print("ut.sight_range:", ut.sight_range)
            print("ut.speed:", ut.speed)
            print("ut.hitpoints:", ut.hitpoints)
            print("ut.attack_cooldown_duration:", ut.attack_cooldown_duration)
            print("ut.attack_damage:", ut.attack_damage)
            print("ut.make_time:", ut.make_time)
            print("Unit types not being initialized properly")
            return

    # Test unit_updates()
    game.parse_msg(test1)
    if len(game.game_state.my_unit_ids) != 6:
        print("My unit ids length failed test")
        return

