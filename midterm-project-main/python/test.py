import logging
import unittest
from unittest.mock import Mock, patch
import time
from maze import Maze, Action, Direction
from BTinterface import BTInterface
from gui_scoreboard import ScoreboardGUI
from path_planner import PathPlanner

logging.basicConfig(level=logging.INFO)

def print_full_sequence(path: list, actions: list):
    """Print the complete movement sequence at the start"""
    print("\nComplete Movement Sequence")
    print("=========================")
    print("Initial state: Car facing LEFT at Node 1")
    print(f"Total steps: {len(actions)}")
    print("\nDetailed sequence:")
    print("------------------")
    
    # First move is always forward
    print(f"Step   1: At Node  1 -> {'ADVANCE':8s} -> Node  7 (First move: car facing left)")
    
    # Print rest of the sequence
    for i, (node, action) in enumerate(zip(path[1:-1], actions[1:]), 2):
        next_node = path[i]
        print(f"Step {i:3d}: At Node {node:2d} -> {action.name:8s} -> Node {next_node:2d}")
    
    # Print command string
    cmd_map = {
        Action.ADVANCE: 'f',
        Action.U_TURN: 'b',
        Action.TURN_RIGHT: 'r',
        Action.TURN_LEFT: 'l',
        Action.HALT: 's'
    }
    cmd_sequence = [cmd_map[action] for action in actions]
    print("\nComplete command string:")
    print("----------------------")
    print(f"{''.join(cmd_sequence)}")
    print(f"Total commands: {len(cmd_sequence)}")
    print("\n")

class MockBluetooth:
    """Mock Bluetooth for testing"""
    def __init__(self, maze: Maze):
        self.connected = False
        self.data = []
        self.current_node = 1
        self.maze = maze
        
        # Find dead ends and assign test UIDs
        self.dead_end_uids = {}
        for node_num in self._find_dead_ends():
            # Assign test UIDs to some dead ends
            if node_num in [3, 6, 24, 44]:  # Example dead ends
                self.dead_end_uids[node_num] = f"TEST{node_num:04d}"
    
    def _find_dead_ends(self):
        """Find all dead ends in the maze"""
        dead_ends = []
        for node_num, node in self.maze.get_node_dict().items():
            if len(node.get_successors()) == 1:
                dead_ends.append(node_num)
        return dead_ends
    
    def do_connect(self, port):
        print("Bluetooth: Connected")
        self.connected = True
        return True
        
    def disconnect(self):
        print("Bluetooth: Disconnected")
        self.connected = False
        
    def serial_write_string(self, data):
        print(f"Bluetooth TX: {data}")
        self.data.append(data)
        
    def serial_read_byte(self):
        # Only return UID if at a dead end
        if len(self.maze.get_node_dict()[self.current_node].get_successors()) == 1:
            uid = self.dead_end_uids.get(self.current_node, "0")
            if uid != "0":
                print(f"Bluetooth RX: UID {uid}")
            return uid
        return "0"
        
    def serial_read_string(self):
        print("Bluetooth RX: ok")
        return "ok"

def test_exploration():
    """
    Test complete maze exploration with mock bluetooth
    """
    print("\nMaze Exploration Test")
    print("====================")
    
    # Initialize components
    maze = Maze("data/maze.csv")
    planner = PathPlanner(maze)
    
    # Find dead ends
    dead_ends = planner.find_dead_ends()
    print(f"\nDead end nodes: {sorted(dead_ends)}")
    
    # Plan path
    start_node = 1
    path = planner.plan_exploration(start_node)
    actions = planner.get_action_sequence(path)
    
    # Force first action to be ADVANCE (car facing left)
    actions[0] = Action.ADVANCE
    
    # Print complete sequence at start
    print_full_sequence(path, actions)
    
    print("Starting simulation:")
    print("-------------------")
    
    # Initialize scoreboard
    scoreboard = ScoreboardGUI(start_position=start_node, game_duration=120)
    
    # Create mock bluetooth with maze information
    bt = MockBluetooth(maze)
    
    # Simulate exploration
    def simulate_exploration():
        current_node = start_node
        current_direction = Direction.WEST  # Starting facing left
        
        for i, action in enumerate(actions):
            time.sleep(1)  # Simulate movement time
            
            # Send command
            cmd_map = {
                Action.ADVANCE: 'f',
                Action.U_TURN: 'b',
                Action.TURN_RIGHT: 'r',
                Action.TURN_LEFT: 'l',
                Action.HALT: 's'
            }
            cmd = cmd_map[action]
            bt.serial_write_string(cmd)
            
            # Update position
            if i + 1 < len(path):
                bt.current_node = path[i + 1]
                print(f"Current position: Node {bt.current_node}")
                
                # Check for treasure
                uid = bt.serial_read_byte()
                if uid != "0":
                    score, time_left = scoreboard.add_UID(uid)
                    print(f"Found treasure at node {bt.current_node}!")
                    print(f"UID: {uid}, Score: {score}")
                
                # Get OK response
                response = bt.serial_read_string()
    
    # Start simulation in a separate thread
    import threading
    sim_thread = threading.Thread(target=simulate_exploration, daemon=True)
    sim_thread.start()
    
    # Start GUI
    print("\nStarting GUI (close window to end simulation)")
    scoreboard.mainloop()

if __name__ == "__main__":
    test_exploration()