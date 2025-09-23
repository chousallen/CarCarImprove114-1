import logging
from typing import List, Tuple, Set, Dict
from collections import deque
from maze import Maze, Node, Direction, Action

log = logging.getLogger(__name__)

class PathPlanner:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.node_dict = maze.get_node_dict()
        
    def find_dead_ends(self) -> List[int]:
        """Find all dead ends (nodes with only one connection)"""
        dead_ends = []
        for node_num, node in self.node_dict.items():
            if len(node.get_successors()) == 1:
                dead_ends.append(node_num)
        return sorted(dead_ends)  # Sort for consistent output
        
    def find_shortest_path(self, start: int, end: int) -> List[int]:
        """Find shortest path between two nodes using BFS"""
        return self.maze.BFS_2(start, end)
        
    def plan_exploration(self, start: int) -> List[int]:
        """
        Plan complete exploration path visiting all dead ends
        Returns: List of node numbers representing the path
        """
        dead_ends = self.find_dead_ends()
        log.info(f"Found {len(dead_ends)} dead ends: {dead_ends}")
        
        current = start
        full_path = [start]
        visited_ends = set()
        
        while len(visited_ends) < len(dead_ends):
            # Find nearest unvisited dead end
            min_dist = float('inf')
            nearest_end = None
            nearest_path = None
            
            for end in dead_ends:
                if end not in visited_ends:
                    path = self.find_shortest_path(current, end)
                    if path and len(path) < min_dist:
                        min_dist = len(path)
                        nearest_end = end
                        nearest_path = path
            
            if nearest_end is None:
                break
                
            # Add path to nearest dead end (excluding start node if it's current position)
            full_path.extend(nearest_path[1:])
            visited_ends.add(nearest_end)
            current = nearest_end
            
        # Convert all nodes to integers
        full_path = [int(node) for node in full_path]
        log.info(f"Planned path visiting {len(visited_ends)} dead ends")
        return full_path

    def get_action_sequence(self, path: List[int]) -> List[Action]:
        """Convert node path to action sequence"""
        if len(path) < 2:
            return []
            
        actions = []
        current_dir = Direction.WEST  # Start facing left
        
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            
            # Get required action using maze's logic
            action = self.maze.getAction(current_dir, current, next_node)
            if action:
                action_enum = Action(action)
                actions.append(action_enum)
                
                # Update direction based on maze's logic
                if action == Action.U_TURN:
                    if current_dir == Direction.NORTH:
                        current_dir = Direction.SOUTH
                    elif current_dir == Direction.SOUTH:
                        current_dir = Direction.NORTH
                    elif current_dir == Direction.EAST:
                        current_dir = Direction.WEST
                    else:  # WEST
                        current_dir = Direction.EAST
                elif action == Action.TURN_RIGHT:
                    if current_dir == Direction.NORTH:
                        current_dir = Direction.EAST
                    elif current_dir == Direction.SOUTH:
                        current_dir = Direction.WEST
                    elif current_dir == Direction.EAST:
                        current_dir = Direction.SOUTH
                    else:  # WEST
                        current_dir = Direction.NORTH
                elif action == Action.TURN_LEFT:
                    if current_dir == Direction.NORTH:
                        current_dir = Direction.WEST
                    elif current_dir == Direction.SOUTH:
                        current_dir = Direction.EAST
                    elif current_dir == Direction.EAST:
                        current_dir = Direction.NORTH
                    else:  # WEST
                        current_dir = Direction.SOUTH
            
        return actions

def test_planner():
    """Test the path planner"""
    maze = Maze("data/maze.csv")
    planner = PathPlanner(maze)
    
    # Test dead end finding
    dead_ends = planner.find_dead_ends()
    print(f"\nDead ends: {dead_ends}")
    
    # Test path planning from node 1
    path = planner.plan_exploration(1)
    print(f"\nPlanned path sequence:")
    for i, node in enumerate(path):
        print(f"Step {i+1}: Node {node}")
    
    # Test action sequence generation
    actions = planner.get_action_sequence(path)
    print(f"\nAction sequence:")
    for i, (node, action) in enumerate(zip(path[:-1], actions)):
        print(f"At Node {node}: {action.name} -> Node {path[i+1]}")
    
    # Convert to command string
    cmd_map = {
        Action.ADVANCE: 'f',
        Action.U_TURN: 'b',
        Action.TURN_RIGHT: 'r',
        Action.TURN_LEFT: 'l',
        Action.HALT: 's'
    }
    cmd_sequence = [cmd_map[action] for action in actions]
    print(f"\nCommand sequence: {''.join(cmd_sequence)}")
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_planner()