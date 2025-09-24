#!/usr/bin/env python3
"""
Demo of terminal-only mode
"""
import time
from main import MazeCar

def demo_terminal_mode():
    """Demo the terminal-only scoring"""
    print("🚀 Terminal-Only Mode Demo")
    print("=" * 40)
    print("✅ No GUI scoreboard")
    print("✅ Score display every 5 seconds")
    print("✅ Immediate UID feedback")
    print("✅ All output in terminal")
    print()
    
    # Create car with short test duration
    car = MazeCar(bt_port="VIRTUAL", game_duration=20)
    
    print(f"Initial score: {car.total_score}")
    print("Simulating UID inputs...")
    print("(You will see score updates every 5 seconds)")
    print()
    
    # Simulate some UID processing
    test_uids = ["TEST0031", "41424344", "TEST0025"]
    
    for i, uid in enumerate(test_uids, 1):
        time.sleep(2)
        print(f"--- Input #{i}: {uid} ---")
        
        # Process UID manually to show behavior
        if uid not in car.visited_uids:
            car.total_score += 50
            car.visited_uids.add(uid)
            print(f"Valid UID received: {uid}")
            print(f"Score updated: +50 points, Total: {car.total_score}")
        
        print()
    
    # Wait to see the automatic score display
    print("Waiting to see automatic score display...")
    time.sleep(8)
    
    # Clean up
    car.score_display_active = False
    print(f"=== DEMO ENDED === Final Score: {car.total_score} points ===")

if __name__ == "__main__":
    demo_terminal_mode()
