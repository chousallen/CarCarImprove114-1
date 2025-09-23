import logging
import time
import argparse
from typing import Optional, List, Tuple
from maze import Maze, Action, Direction
from BTinterface import BTInterface
from gui_scoreboard import ScoreboardGUI
from path_planner import PathPlanner
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
log = logging.getLogger(__name__)


class MazeCar:
    """
    Main class that integrates all functionality for the maze-solving car
    """

    def __init__(self, maze_file: str = "data/maze.csv",
                 start_node: int = 1,
                 game_duration: int = 600,
                 bt_port: Optional[str] = None):
        # Initialize components
        maze_file = os.path.abspath(maze_file)
        self.maze = Maze(maze_file)
        self.bt = BTInterface(port=bt_port)
        self.current_node = start_node
        self.current_direction = Direction.NORTH
        self.scoreboard = ScoreboardGUI(start_position=start_node,
                                        game_duration=game_duration, maze_file=maze_file)
        self.scoreboard.update()

        # Initialize path planner
        self.planner = PathPlanner(self.maze)
        self.planned_path = self.planner.plan_exploration(start_node)
        self.action_sequence = self.planner.get_action_sequence(
            self.planned_path)
        self.current_action_index = 0

        # Load UID to node mapping
        self.uid_to_node = self._load_uid_mapping()

        log.info(f"Planned path: {self.planned_path}")
        log.info(
            f"Action sequence: {[action.name for action in self.action_sequence]}")

    def _load_uid_mapping(self) -> dict:
        """Load UID to node mapping from fakeUID.csv"""
        import csv
        uid_map = {}
        try:
            with open("data/fakeUID.csv", 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    uid, node = row
                    uid_map[uid] = int(node)
            log.info(f"Loaded {len(uid_map)} UID mappings")
        except Exception as e:
            log.error(f"Failed to load UID mappings: {e}")
        return uid_map

    def _action_to_cmd(self, action: Action) -> str:
        """Convert action enum to command string"""
        cmd_map = {
            Action.ADVANCE: 'f',
            Action.U_TURN: 'b',
            Action.TURN_RIGHT: 'r',
            Action.TURN_LEFT: 'l',
            Action.HALT: 's'
        }
        return cmd_map.get(action, 's')

    def _update_direction(self, action: Action):
        """Update current direction based on action"""
        if action == Action.ADVANCE:
            return
        elif action == Action.U_TURN:
            self.current_direction = Direction(self.current_direction + 1
                                               if self.current_direction % 2 == 1 else self.current_direction - 1)
        elif action == Action.TURN_RIGHT:
            self.current_direction = Direction(self.current_direction + 3
                                               if self.current_direction == 1
                                               else (self.current_direction - 1 if self.current_direction > 1 else 4))
        elif action == Action.TURN_LEFT:
            self.current_direction = Direction(self.current_direction + 1
                                               if self.current_direction < 4 else 1)

    def check_for_uid(self):
        """Check for UID and update score if found"""
        uid = self.bt.get_UID()
        if uid and uid != "0":
            # If UID exists in mapping, update current position
            if uid in self.uid_to_node:
                self.current_node = self.uid_to_node[uid]
                log.info(f"Found UID {uid} at node {self.current_node}")

            # Process UID for scoring
            score, time_left = self.scoreboard.add_UID(uid)
            log.info(f"Scored {score} points, Time left: {time_left:.1f}s")
            return time_left <= 0  # Return True if time's up
        return False

    def run(self):
        """Main control loop"""
        log.info("Starting maze exploration...")
        self.bt.start()

        try:
            while self.current_action_index < len(self.action_sequence):
                # Check for UID before each action
                if self.check_for_uid():
                    log.info("Time's up!")
                    break

                # Get next action
                action = self.action_sequence[self.current_action_index]
                cmd = self._action_to_cmd(action)

                # Send command
                log.info(f"Sending command: {action.name}")
                self.bt.send_action(cmd)

                # Wait for response while checking for UID
                max_wait = 10  # Maximum wait time in seconds
                wait_start = time.time()
                response = None

                while time.time() - wait_start < max_wait:
                    # Check for UID while waiting
                    if self.check_for_uid():
                        log.info("Time's up!")
                        return

                    # Check for OK response
                    response = self.bt.get_ok()
                    if response == "ok":
                        break
                    time.sleep(0.1)

                if response != "ok":
                    log.error(
                        f"No response or unexpected response: {response}")
                    break

                # Update state
                self._update_direction(action)
                if self.current_action_index + 1 < len(self.planned_path):
                    self.current_node = self.planned_path[self.current_action_index + 1]
                log.info(f"Moved to node {self.current_node}")

                self.current_action_index += 1
                time.sleep(0.1)  # Small delay between actions

        except KeyboardInterrupt:
            log.info("Exploration interrupted by user")
        finally:
            self.bt.end_process()
            final_score = self.scoreboard.get_current_score()
            log.info(f"Final score: {final_score}")


def parse_args():
    parser = argparse.ArgumentParser(
        description='Maze Explorer Control Program')
    parser.add_argument('--node', type=int, default=1,
                        help='Starting node number (default: 1)')
    parser.add_argument('--time', type=int, default=600,
                        help='Game duration in seconds (default: 600)')
    parser.add_argument('--port', type=str, default=None,
                        help='Bluetooth port (e.g., COM3)')
    parser.add_argument('--maze', type=str, default="python/data/maze.csv",
                        help='Maze file path (default: python/data/maze.csv)')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    car = MazeCar(
        maze_file=args.maze,
        start_node=args.node,
        game_duration=args.time,
        bt_port=args.port
    )
    car.run()
