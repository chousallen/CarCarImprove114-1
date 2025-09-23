import logging
from typing import Tuple, Optional
import csv
import time

log = logging.getLogger(__name__)

class LocalScoreboard:
    """
    A local scoreboard implementation for testing and development
    """
    def __init__(self, team_name: str, uid_file: str = "data/fakeUID.csv"):
        self.team_name = team_name
        self.total_score = 0
        self.start_time = time.time()
        self.game_duration = 600  # 10 minutes in seconds
        self.visited_uids = set()
        
        # Load UID scores from CSV
        self.uid_scores = {}
        try:
            with open(uid_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    uid, score = row
                    self.uid_scores[uid] = int(score)
            log.info(f"Loaded {len(self.uid_scores)} UIDs from {uid_file}")
        except Exception as e:
            log.error(f"Failed to load UID file: {e}")
            self.uid_scores = {}

    def add_UID(self, uid: str) -> Tuple[int, float]:
        """
        Add a new UID and get score
        Returns: (score for this UID, remaining time in seconds)
        """
        if not uid or not isinstance(uid, str):
            log.warning(f"Invalid UID format: {uid}")
            return 0, self._get_remaining_time()

        # Remove "0x" prefix if present and ensure 8 characters
        uid = uid.replace("0x", "").upper().zfill(8)
        
        # Check if UID exists and hasn't been visited
        if uid not in self.uid_scores:
            log.info(f"Unknown UID: {uid}")
            return 0, self._get_remaining_time()
        
        if uid in self.visited_uids:
            log.info(f"UID already visited: {uid}")
            return 0, self._get_remaining_time()
        
        # Add score
        score = self.uid_scores[uid]
        self.total_score += score
        self.visited_uids.add(uid)
        
        remaining_time = self._get_remaining_time()
        log.info(f"Added UID {uid}: +{score} points (Total: {self.total_score})")
        return score, remaining_time

    def get_current_score(self) -> int:
        """Get current total score"""
        return self.total_score

    def _get_remaining_time(self) -> float:
        """Calculate remaining game time in seconds"""
        elapsed = time.time() - self.start_time
        remaining = max(0, self.game_duration - elapsed)
        return remaining

def test_scoreboard():
    """Test the LocalScoreboard functionality"""
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create scoreboard instance
    board = LocalScoreboard("TestTeam", "data/fakeUID.csv")
    
    # Test valid UID
    score, time = board.add_UID("10BA617E")
    assert score > 0, "Should get points for valid UID"
    assert board.get_current_score() == score, "Total score should match"
    
    # Test duplicate UID
    score2, time = board.add_UID("10BA617E")
    assert score2 == 0, "Should get 0 points for duplicate UID"
    
    # Test invalid UID
    score3, time = board.add_UID("INVALID")
    assert score3 == 0, "Should get 0 points for invalid UID"
    
    # Test time remaining
    assert time > 0, "Should have time remaining"
    assert time <= 600, "Time should not exceed game duration"
    
    log.info("All tests passed!")

if __name__ == "__main__":
    test_scoreboard()
