import queue
import math
class Path:
    # Find shortest path from A to B on some graph.
    # Use A* algorithm

    def __init__(self):
        # Take the graph to be a set of waypoints on the game map.
        # self.map_waypoints_list = None
        pass

    def neighbors(self, A, map):
        nbrs = [(A[0]+1, A[1]),
                (A[0]-1, A[1]),
                (A[0], A[1]+1),
                (A[0], A[1]-1)]
        ret = []
        for n in nbrs:
            y = n[1]
            x = n[0]
            if (0 <= x < len(map[0])) and (0 <= y < len(map)):
                if not map[y][x] or not map[y][x].blocked:
                   ret.append(n)

        return ret
    
    def heuristic(self, dest, nxt):
        return abs(dest[0] - nxt[0]) + abs(dest[1] - nxt[1])

    def get_path(self, units, map, start, dest):
        """Compute A* path from start to dest given map.
        map == 2D list of tile instances
        start == coordinate tuple, map indices
        dest == like start
        """
        frontier = queue.PriorityQueue()
        frontier.put((0, start))
        came_from = {}
        came_from[str(start)] = None
        cost_so_far = {}
        cost_so_far[str(start)] = 0

        current = start
        while not frontier.empty():
            current = frontier.get()[1]
            current_str = str(current)

            if current == dest:
                break

            for nxt in self.neighbors(current, map):
                unit_here = False
                if units:
                    for u in units:
                        if u.x == nxt[0] and u.y == nxt[1]:
                            unit_here = True
                new_cost = cost_so_far[current_str] + 1
                if unit_here:
                    new_cost += 8
                nxt_str = str(nxt)
                # if str(nxt) not in came_from:
                if (nxt_str not in cost_so_far) or (new_cost < cost_so_far[nxt_str]):
                    cost_so_far[nxt_str] = new_cost
                    priority = new_cost + self.heuristic(dest, nxt)
                    # priority = self.heuristic(dest, nxt)
                    frontier.put((priority, nxt))
                    came_from[nxt_str] = current

        path = [current]
        while current != start: 
            current = came_from[str(current)]
            path.append(current)
        path.reverse()
        return path