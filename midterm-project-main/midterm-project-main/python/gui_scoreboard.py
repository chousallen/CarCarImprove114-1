import tkinter as tk
from tkinter import ttk
import time
import csv
from typing import Tuple, Optional, Dict
import logging
from datetime import datetime
import threading
from maze import Maze
import numpy as np
from collections import deque

log = logging.getLogger(__name__)

class ScoreboardGUI(tk.Tk):
    def __init__(self, start_position: int = 1, 
                 game_duration: int = 600,
                 maze_file: str = "data/maze.csv", 
                 uid_file: str = "data/fakeUID.csv"):
        super().__init__()

        # Initialize scoreboard data
        self.total_score = 0
        self.start_time = time.time()
        self.game_duration = game_duration
        self.visited_uids = set()
        self.uid_positions = {}
        self.start_position = start_position
        self.maze = Maze(maze_file)
        self.position_coords = self._load_maze_positions()
        
        # Calculate maze dimensions for display
        self.maze_dims = self._calculate_maze_dimensions()
        
        # Load UID mappings
        self._load_uids(uid_file)

        # Configure window
        self.title(f"Maze Explorer - Starting from Node {start_position}")
        self.geometry("1200x800")  # Increased window size
        self.configure(bg='#2C3E50')

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create left frame for maze visualization
        self.left_frame = ttk.Frame(self.container)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create maze canvas
        self.canvas_size = 400
        self.canvas = tk.Canvas(self.left_frame, 
                              width=self.canvas_size, 
                              height=self.canvas_size,
                              bg='#34495E')
        self.canvas.pack(padx=10, pady=10)
        
        # Create right frame for scoreboard
        self.right_frame = ttk.Frame(self.container)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configure style
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=('Helvetica', 24, 'bold'), foreground='#ECF0F1')
        self.style.configure("Score.TLabel", font=('Helvetica', 48, 'bold'), foreground='#E74C3C')
        self.style.configure("Info.TLabel", font=('Helvetica', 16), foreground='#95A5A6')
        
        # Create header
        self.header_frame = ttk.Frame(self.right_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(self.header_frame, 
                 text=f"MAZE EXPLORER (Start: Node {start_position})", 
                 style="Title.TLabel").pack()

        # Create score display
        self.score_frame = ttk.Frame(self.right_frame)
        self.score_frame.pack(fill=tk.X, pady=10)
        ttk.Label(self.score_frame, text="TOTAL SCORE", style="Info.TLabel").pack()
        self.score_label = ttk.Label(self.score_frame, text="0", style="Score.TLabel")
        self.score_label.pack()

        # Create timer display
        self.timer_frame = ttk.Frame(self.right_frame)
        self.timer_frame.pack(fill=tk.X, pady=10)
        ttk.Label(self.timer_frame, text="TIME REMAINING", style="Info.TLabel").pack()
        self.timer_label = ttk.Label(self.timer_frame, text=self._format_time(game_duration), 
                                   style="Info.TLabel")
        self.timer_label.pack()

        # Create history display
        self.history_frame = ttk.Frame(self.right_frame)
        self.history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        ttk.Label(self.history_frame, text="TREASURE HISTORY", style="Info.TLabel").pack()
        
        # Create treeview for history
        self.tree = ttk.Treeview(self.history_frame, 
                                columns=('Time', 'UID', 'Position', 'Distance', 'Score'), 
                                show='headings')
        self.tree.heading('Time', text='Time')
        self.tree.heading('UID', text='UID')
        self.tree.heading('Position', text='Position')
        self.tree.heading('Distance', text='Manhattan Dist')
        self.tree.heading('Score', text='Score')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Draw initial maze
        self.draw_maze()
        
        # Start timer update
        self._update_timer()

    def _calculate_maze_dimensions(self) -> Tuple[int, int, int, int]:
        """Calculate maze dimensions and normalize coordinates"""
        x_coords = [x for x, y in self.position_coords.values()]
        y_coords = [y for x, y in self.position_coords.values()]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        return min_x, max_x, min_y, max_y

    def draw_maze(self):
        """Draw the maze on the canvas"""
        self.canvas.delete("all")  # Clear canvas
        
        # Calculate scaling factors
        min_x, max_x, min_y, max_y = self.maze_dims
        width = max_x - min_x
        height = max_y - min_y
        margin = 40
        scale = min((self.canvas_size - 2 * margin) / width,
                   (self.canvas_size - 2 * margin) / height)

        def transform_coord(x, y):
            """Transform maze coordinates to canvas coordinates"""
            canvas_x = margin + (x - min_x) * scale
            canvas_y = margin + (y - min_y) * scale
            return canvas_x, canvas_y

        # Draw connections (corridors)
        node_dict = self.maze.get_node_dict()
        drawn_paths = set()
        
        for node_num, coords in self.position_coords.items():
            x1, y1 = transform_coord(*coords)
            node = node_dict[node_num]
            
            for next_node, direction, _ in node.get_successors():
                if (node_num, next_node) not in drawn_paths and \
                   (next_node, node_num) not in drawn_paths:
                    next_coords = self.position_coords[next_node]
                    x2, y2 = transform_coord(*next_coords)
                    self.canvas.create_line(x1, y1, x2, y2, fill='#95A5A6', width=2)
                    drawn_paths.add((node_num, next_node))

        # Draw nodes
        node_radius = 15
        for node_num, coords in self.position_coords.items():
            x, y = transform_coord(*coords)
            
            # Choose node color
            if node_num == self.start_position:
                color = '#E74C3C'  # Red for start
            elif node_num in [self.uid_positions.get(uid) for uid in self.visited_uids]:
                color = '#2ECC71'  # Green for visited
            else:
                color = '#3498DB'  # Blue for unvisited
            
            # Draw node
            self.canvas.create_oval(x - node_radius, y - node_radius,
                                  x + node_radius, y + node_radius,
                                  fill=color, outline='#ECF0F1')
            # Draw node number (as integer)
            self.canvas.create_text(x, y, text=str(int(node_num)),
                                  fill='#ECF0F1', font=('Helvetica', 10, 'bold'))

    def _format_time(self, seconds: int) -> str:
        """Format seconds into MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def _load_maze_positions(self) -> Dict[int, Tuple[int, int]]:
        """
        Load position coordinates from maze using BFS to assign coordinates
        Returns a dictionary mapping node numbers to (x, y) coordinates
        """
        node_dict = self.maze.get_node_dict()
        coords = {}
        visited = set()
        queue = deque([(self.start_position, 0, 0)])  # (node_num, x, y)
        coords[self.start_position] = (0, 0)
        visited.add(self.start_position)

        while queue:
            node_num, x, y = queue.popleft()
            node = node_dict[node_num]
            
            # Check all successors
            for next_node, direction, _ in node.get_successors():
                if next_node not in visited:
                    # Calculate new coordinates based on direction
                    if direction == 1:  # NORTH
                        new_x, new_y = x, y - 1
                    elif direction == 2:  # SOUTH
                        new_x, new_y = x, y + 1
                    elif direction == 3:  # WEST
                        new_x, new_y = x - 1, y
                    else:  # EAST
                        new_x, new_y = x + 1, y
                    
                    coords[next_node] = (new_x, new_y)
                    queue.append((next_node, new_x, new_y))
                    visited.add(next_node)

        log.info(f"Calculated coordinates for {len(coords)} nodes")
        return coords

    def _load_uids(self, uid_file: str):
        """Load UIDs and their corresponding positions"""
        try:
            with open(uid_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    uid, pos = row
                    self.uid_positions[uid] = int(pos)
            log.info(f"Loaded {len(self.uid_positions)} UIDs")
        except Exception as e:
            log.error(f"Failed to load UID file: {e}")

    def calculate_manhattan_distance(self, position: int) -> int:
        """Calculate Manhattan distance from start position to given position"""
        if position not in self.position_coords or self.start_position not in self.position_coords:
            log.warning(f"Position {position} or start position not found in coordinates")
            return 0
            
        start = self.position_coords[self.start_position]
        end = self.position_coords[position]
        distance = abs(end[0] - start[0]) + abs(end[1] - start[1])
        log.debug(f"Manhattan distance from {self.start_position}{start} to {position}{end}: {distance}")
        return distance

    def calculate_score(self, uid: str) -> int:
        """Calculate score - always return 50 points for any valid UID"""
        # Always return fixed 50 points regardless of UID type or position
        return 50

    def add_UID(self, uid: str) -> Tuple[int, float]:
        """Process a new UID and return (score, remaining_time)"""
        if not uid or uid == "0":
            return 0, self._get_remaining_time()
            
        # Format UID - 保持原格式，只移除0x前綴並轉大寫
        uid = uid.replace("0x", "").upper()
        
        # 只對純HEX格式補足到8位，TEST格式保持原樣
        if not uid.startswith("TEST") and all(c in '0123456789ABCDEF' for c in uid):
            uid = uid.zfill(8)
        
        # Check if already visited
        if uid in self.visited_uids:
            log.info(f"UID already visited: {uid}")
            return 0, self._get_remaining_time()
            
        # Calculate score
        score = self.calculate_score(uid)
        self.total_score += score
        self.visited_uids.add(uid)
        
        # Get position and distance for known UIDs
        position = self.uid_positions.get(uid, "Unknown")
        distance = self.calculate_manhattan_distance(position) if isinstance(position, int) else "N/A"
        
        # Update GUI
        self._update_score(score, uid, position, distance)
        
        # Redraw maze to update visited nodes
        self.draw_maze()
        
        remaining_time = self._get_remaining_time()
        return score, remaining_time

    def get_current_score(self) -> int:
        """Get current total score"""
        return self.total_score

    def _get_remaining_time(self) -> float:
        """Calculate remaining game time in seconds"""
        elapsed = time.time() - self.start_time
        return max(0, self.game_duration - elapsed)

    def _update_timer(self):
        """Update timer display"""
        remaining = self._get_remaining_time()
        self.timer_label.config(text=self._format_time(int(remaining)))
        
        if remaining > 0:
            self.after(1000, self._update_timer)
        else:
            self.timer_label.config(text="TIME'S UP!")

    def _update_score(self, score: int, uid: str, position: int, distance: int):
        """Update score display and history"""
        self.score_label.config(text=str(self.total_score))
        
        # Add to history
        current_time = datetime.now().strftime("%H:%M:%S")
        self.tree.insert('', 0, values=(current_time, uid, position, distance, score))

if __name__ == "__main__":
    # This is just for testing the GUI
    scoreboard = ScoreboardGUI(start_position=1, game_duration=60)  # 1 minute test
    scoreboard.mainloop()