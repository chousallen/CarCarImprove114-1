import logging
import csv
import time
from typing import Tuple, Dict, Optional
import numpy as np

log = logging.getLogger(__name__)

class Scoreboard:
    """
    Scoreboard implementation with Manhattan distance scoring
    """
    def __init__(self, uid_file: str = "data/fakeUID.csv"):
        self.start_time = time.time()
        self.game_duration = 600  # 10 minutes
        self.total_score = 0
        self.visited_uids = set()
        self.uid_to_node = {}  # Maps UID to node number
        self.node_scores = {}  # Cache for node scores
        
        # Load UID mappings
        self._load_uids(uid_file)
        
    def _load_uids(self, uid_file: str):
        """Load UIDs and their corresponding node numbers"""
        try:
            with open(uid_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    uid, node = row
                    self.uid_to_node[uid] = int(node)
            log.info(f"Loaded {len(self.uid_to_node)} UIDs")
        except Exception as e:
            log.error(f"Failed to load UID file: {e}")
            
    def calculate_score(self, node_number: int) -> int:
        """Calculate score based on Manhattan distance from start"""
        if node_number in self.node_scores:
            return self.node_scores[node_number]
            
        # Simple scoring: node number * 10 (assuming node numbers roughly correspond to distance)
        score = node_number * 10
        self.node_scores[node_number] = score
        return score
        
    def add_UID(self, uid: str) -> Tuple[int, float]:
        """
        Process a new UID and return (score, remaining_time)
        """
        if not uid or uid == "0":
            return 0, self._get_remaining_time()
            
        # Format UID
        uid = uid.replace("0x", "").upper().zfill(8)
        
        # Check if UID exists and hasn't been visited
        if uid not in self.uid_to_node:
            log.info(f"Unknown UID: {uid}")
            return 0, self._get_remaining_time()
            
        if uid in self.visited_uids:
            log.info(f"UID already visited: {uid}")
            return 0, self._get_remaining_time()
            
        # Calculate score
        node_number = self.uid_to_node[uid]
        score = self.calculate_score(node_number)
        self.total_score += score
        self.visited_uids.add(uid)
        
        remaining_time = self._get_remaining_time()
        log.info(f"Added UID {uid} at node {node_number}: +{score} points (Total: {self.total_score})")
        return score, remaining_time
        
    def get_current_score(self) -> int:
        """Get current total score"""
        return self.total_score
        
    def _get_remaining_time(self) -> float:
        """Calculate remaining game time in seconds"""
        elapsed = time.time() - self.start_time
        return max(0, self.game_duration - elapsed)
