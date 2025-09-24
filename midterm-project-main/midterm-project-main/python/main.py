import logging
import time
import argparse
import threading
from typing import Optional, List, Tuple
from maze import Maze, Action, Direction
from BTinterface import BTInterface
from path_planner import PathPlanner

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
        self.maze = Maze(maze_file)
        self.bt = BTInterface(port=bt_port)
        self.current_node = start_node
        self.current_direction = Direction.NORTH
        
        # Simple scoreboard variables
        self.total_score = 0
        self.visited_uids = set()
        self.start_time = time.time()
        self.game_duration = game_duration
        self.score_display_active = True
        
        # Initialize path planner
        self.planner = PathPlanner(self.maze)
        self.planned_path = self.planner.plan_exploration(start_node)
        self.action_sequence = self.planner.get_action_sequence(self.planned_path)
        self.current_action_index = 0
        
        # Load UID to node mapping
        self.uid_to_node = self._load_uid_mapping()
        
        log.info(f"Planned path: {self.planned_path}")
        log.info(f"Action sequence: {[action.name for action in self.action_sequence]}")
        
        # Start score display thread
        self._start_score_display_thread()

    def _start_score_display_thread(self):
        """Start background thread to display score every 5 seconds"""
        def score_display_loop():
            while self.score_display_active:
                time.sleep(5)
                if self.score_display_active:
                    remaining_time = max(0, self.game_duration - (time.time() - self.start_time))
                    print(f"=== SCORE UPDATE === Total Score: {self.total_score} points | Time Left: {remaining_time:.1f}s ===")
        
        score_thread = threading.Thread(target=score_display_loop, daemon=True)
        score_thread.start()

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
        if uid and uid != "0" and uid != 0:
            # Convert UID to string and process
            uid_str = str(uid)
            log.debug(f"Received raw data: {uid_str}")
            
            # Split string by spaces and check each part
            parts = uid_str.split()
            valid_uid_found = False
            
            for part in parts:
                if not part.strip():  # Skip empty parts
                    continue
                    
                # Decode hex string if needed and format UID for this part
                decoded_uid = self._decode_hex_string(part.strip())
                formatted_uid = self._format_uid(decoded_uid)
                
                if self._is_valid_uid(formatted_uid):
                    # Show in terminal
                    print(f"Valid UID received: {formatted_uid}")
                    log.info(f"Valid UID detected in part: {formatted_uid}")
                    
                    # Update score with fixed 50 points (avoid duplicates)
                    if formatted_uid not in self.visited_uids:
                        self.total_score += 50
                        self.visited_uids.add(formatted_uid)
                        print(f"Score updated: +50 points, Total: {self.total_score}")
                        log.info(f"UID {formatted_uid} scored 50 points, total: {self.total_score}")
                    else:
                        print(f"UID {formatted_uid} already visited, no points added")
                    
                    valid_uid_found = True
                    
                    # Check if time is up
                    remaining_time = max(0, self.game_duration - (time.time() - self.start_time))
                    if remaining_time <= 0:
                        return True
                else:
                    # This part is not UID format, output to terminal
                    print(f"Received non-UID data part: {part}")
            
            # If no valid UID found in any part, print the whole string
            if not valid_uid_found:
                print(f"Received non-UID data: {uid_str}")
                
        return False
    
    def _decode_hex_string(self, data_str: str) -> str:
        """Decode hex string to actual hex value"""
        try:
            # If data is already in hex format (0x...), return as is
            if data_str.startswith('0x'):
                return data_str
                
            # If data looks like hex string representation, try to decode
            clean_data = data_str.strip()
            
            # Check if it's a hex string like "41424344" (ABCD in hex)
            if len(clean_data) % 2 == 0 and all(c in '0123456789ABCDEFabcdef' for c in clean_data):
                try:
                    # Convert hex string to actual value
                    hex_bytes = bytes.fromhex(clean_data)
                    # Convert back to hex representation
                    return '0x' + clean_data.upper()
                except ValueError:
                    pass
            
            # Try to interpret as hex string encoding ASCII
            try:
                if all(c in '0123456789ABCDEFabcdef' for c in clean_data):
                    # Treat as direct hex representation
                    return '0x' + clean_data.upper()
            except:
                pass
                
            # Return original if cannot decode
            return data_str
            
        except Exception as e:
            log.debug(f"Error decoding hex string {data_str}: {e}")
            return data_str
    
    def _format_uid(self, uid_str: str) -> str:
        """Format UID to standard format"""
        # Remove 0x prefix
        clean_uid = uid_str.replace("0x", "").strip().upper()
        
        # If HEX format, pad to 8 digits
        if all(c in '0123456789ABCDEF' for c in clean_uid):
            return clean_uid.zfill(8)
        
        # If TEST format, keep as is
        return clean_uid
    
    def _is_valid_uid(self, uid_str: str) -> bool:
        """Check if UID format is valid"""
        # Remove possible 0x prefix
        clean_uid = uid_str.replace("0x", "").strip().upper()
        
        # Check if TEST format
        if clean_uid.startswith("TEST") and len(clean_uid) >= 8:
            return True
        
        # Check if HEX format (4-8 hex digits)
        if len(clean_uid) >= 4 and len(clean_uid) <= 8 and all(c in '0123456789ABCDEF' for c in clean_uid):
            return True
            
        # Check if pure number format (some RFID may return this)
        if clean_uid.isdigit() and len(clean_uid) >= 4:
            return True
            
        return False

    def run(self):
        """Main control loop - Auto execution mode"""
        
        # Print complete command string first, before any other output
        # Build the actual command string that will be sent (skipping first 'f' if present)
        actual_commands = []
        for i, action in enumerate(self.action_sequence):
            cmd = self._action_to_cmd(action)
            if i == 0 and cmd == 'f':
                continue  # Skip first 'f'
            actual_commands.append(cmd)
        
        command_string = 'g' + ''.join(actual_commands)
        print(f"=== ACTUAL COMMAND STRING === {command_string} ===")
        
        log.info("Starting maze exploration...")
        self.bt.start()
        
        try:
            # Send all commands without waiting for response
            log.info(f"Preparing to send {len(self.action_sequence)} commands")
            
            for i, action in enumerate(self.action_sequence):
                # Check if time is up
                if self.check_for_uid():
                    log.info("Time's up!")
                    break
                
                # Skip the first 'f' command (index 0 and cmd is 'f')
                cmd = self._action_to_cmd(action)
                if i == 0 and cmd == 'f':
                    log.info(f"[{i+1}/{len(self.action_sequence)}] Skipping first 'f' command: {action.name} ({cmd})")
                    continue
                
                # Send command directly
                log.info(f"[{i+1}/{len(self.action_sequence)}] Sending command: {action.name} ({cmd})")
                self.bt.send_action(cmd)
                
                # Update state (without waiting for response)
                self._update_direction(action)
                if i + 1 < len(self.planned_path):
                    self.current_node = self.planned_path[i + 1]
                    log.info(f"Moving to node {self.current_node}")
                
                # Very short delay to avoid sending commands too fast
                time.sleep(0.05)
            
            log.info("All commands sent successfully!")
            
            # Continue listening for UID until game ends
            log.info("Continuously listening for UID...")
            while True:
                if self.check_for_uid():
                    log.info("Game time finished!")
                    break
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            log.info("Program interrupted by user")
        finally:
            self.score_display_active = False  # Stop score display thread
            self.bt.end_process()
            print(f"=== GAME ENDED === Final Score: {self.total_score} points ===")
            log.info(f"Final score: {self.total_score}")

def parse_args():
    parser = argparse.ArgumentParser(description='Maze Explorer Control Program')
    parser.add_argument('--node', type=int, default=24,
                      help='Starting node number (default: 24)')
    parser.add_argument('--time', type=int, default=600,
                      help='Game duration in seconds (default: 600)')
    parser.add_argument('--port', type=str, default=None,
                      help='Bluetooth port (e.g., COM3)')
    parser.add_argument('--maze', type=str, default="data/maze.csv",
                      help='Maze file path (default: data/maze.csv)')
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