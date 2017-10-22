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
