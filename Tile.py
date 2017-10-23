import math
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

def get_non_blocked_neighbor(my_map, A, home):
    nbrs = [(A[0]-1, A[1]),
            (A[0]+1, A[1]),
            (A[0], A[1]+1),
            (A[0], A[1]-1)]
    dlist = []
    for i,d in enumerate(nbrs):
        dlist.append((abs(d[0]-home[0]) + abs(d[1]-home[1]), i))
    dlist.sort()

    ret = []
    for n in dlist:
        y = nbrs[n[1]][1]
        x = nbrs[n[1]][0]
        if (0 <= x < len(my_map[0])) and (0 <= y < len(my_map)):
            if not my_map[y][x] or not my_map[y][x].blocked:
                return (x,y)

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