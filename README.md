I wrote this code at a small code competition at Atomic Object in Ann Arbor. It was a lot of fun to participate and compete with the other programmers.

For what this agent does, lightly gather resources and then rush, I think it does well. The path finding seems to be glitch free (should test it more though).


Some things I've thought about since writing this code.


Improvements

    - try to avoid tiles that contain enemy units
    - use game info to calculate best unit when using a rush strategy
    - change strategy based on map and initial exploration (tank, rush, mix)
    - cause units to regroup some when beginning to move in for the strike on the enemy base
    - make sure units dont try to gather from or move to resources that don't exist
    - queue attack commands based on enemy hp
    - attack an enemy unit with a just a certain number of friendly units
		- maximize resources gained per turn given coordinates and resource type


Write test cases.


TODO
    use dict.get(key) or dict.pop(key, or_value) instead of tons of if statements in json parser.
