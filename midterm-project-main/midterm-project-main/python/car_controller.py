import logging
import time
from typing import Optional, List
from maze import Maze, Action
from BTinterface import BTInterface
from local_scoreboard import LocalScoreboard

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
log = logging.getLogger(__name__)

class CarController:
    """
    Main controller class for the maze-solving car
    """
    def __init__(self, maze_file: str, bt_port: Optional[str] = None):
        self.maze = Maze(maze_file)
        self.bt = BTInterface(port=bt_port)
        self.scoreboard = LocalScoreboard("TestTeam")
        self.current_node = self.maze.get_start_point()
        self.current_direction = 1  # Start facing NORTH
        
    def start(self):
        """Start the car control process"""
        log.info("Starting car control process...")
        self.bt.start()
        
        try:
            while True:
                # Check for RFID
                uid = self.bt.get_UID()
                if uid and uid != "0":
                    score, time_left = self.scoreboard.add_UID(uid)
                    log.info(f"Found treasure! Score: {score}, Time left: {time_left:.1f}s")
                    
                # Get next action
                next_node = self._get_next_node()
                if not next_node:
                    log.info("No more nodes to explore")
                    break
                    
                action = self.maze.getAction(self.current_direction, self.current_node, next_node)
                if not action:
                    log.error("Failed to get action")
                    break
                
                # Execute action
                log.debug(f"Executing action: {Action(action).name}")
                self.bt.send_action(self._action_to_command(action))
                
                # Wait for car to complete action
                response = self.bt.get_ok()
                if response != "ok":
                    log.error(f"Unexpected response from car: {response}")
                    break
                
                # Update current state
                self.current_node = next_node
                self.current_direction = self._update_direction(action)
                
        except KeyboardInterrupt:
            log.info("Control process interrupted by user")
        finally:
            self.bt.end_process()
            
    def _get_next_node(self):
        """Get the next node to visit"""
        # For now, just get the first unvisited successor
        successors = self.current_node.get_successors()
        return successors[0][0] if successors else None
    
    def _action_to_command(self, action: int) -> str:
        """Convert Action enum to command string"""
        cmd_map = {
            Action.ADVANCE: 'f',
            Action.U_TURN: 'b',
            Action.TURN_RIGHT: 'r',
            Action.TURN_LEFT: 'l',
            Action.HALT: 's'
        }
        return cmd_map.get(Action(action), 's')
    
    def _update_direction(self, action: int) -> int:
        """Update current direction based on action taken"""
        direction_after_action = {
            Action.ADVANCE: lambda d: d,
            Action.U_TURN: lambda d: d + 1 if d % 2 == 1 else d - 1,
            Action.TURN_RIGHT: lambda d: d + 3 if d == 1 else (d - 1 if d > 1 else 4),
            Action.TURN_LEFT: lambda d: d + 1 if d < 4 else 1,
            Action.HALT: lambda d: d
        }
        return direction_after_action[Action(action)](self.current_direction)

def test_controller():
    """Test the CarController functionality"""
    # Create controller with test maze
    controller = CarController("data/small_maze.csv")
    
    # Test action to command conversion
    assert controller._action_to_command(1) == 'f', "ADVANCE should map to 'f'"
    assert controller._action_to_command(3) == 'r', "TURN_RIGHT should map to 'r'"
    
    # Test direction updates
    assert controller._update_direction(1) == 1, "ADVANCE should not change direction"
    assert controller._update_direction(2) == 2, "U_TURN from NORTH should face SOUTH"
    
    log.info("All controller tests passed!")

if __name__ == "__main__":
    test_controller()
