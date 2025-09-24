#!/usr/bin/env python3
"""
Test terminal-only mode with score display every 5 seconds
"""
import time
import threading
from main import MazeCar

def test_terminal_mode():
    """Test terminal-only scoring mode"""
    print("Testing Terminal-Only Mode")
    print("=" * 50)
    
    # Create MazeCar with shorter duration for testing
    car = MazeCar(bt_port="VIRTUAL", game_duration=30)  # 30 seconds for testing
    
    print(f"Initial score: {car.total_score}")
    print("Score will be displayed every 5 seconds...")
    print("Simulating UID reception...")
    print()
    
    # Simulate some UID inputs
    test_uids = [
        "debug TEST0031 sensor",
        "status 41424344 ok", 
        "TEST0025 battery 80%",
        "invalid data xyz123",
        "TEST0031",  # Duplicate should not add points
        "0x12345678 temperature 25.5"
    ]
    
    # Send UIDs at intervals to see the scoring
    def simulate_uid_reception():
        for i, test_uid in enumerate(test_uids):
            time.sleep(3)  # Wait 3 seconds between UIDs
            print(f"\n--- Simulating input #{i+1}: '{test_uid}' ---")
            
            # Simulate the UID processing
            parts = test_uid.split()
            for part in parts:
                if not part.strip():
                    continue
                    
                decoded_uid = car._decode_hex_string(part.strip())
                formatted_uid = car._format_uid(decoded_uid)
                
                if car._is_valid_uid(formatted_uid):
                    print(f"Valid UID received: {formatted_uid}")
                    
                    if formatted_uid not in car.visited_uids:
                        car.total_score += 50
                        car.visited_uids.add(formatted_uid)
                        print(f"Score updated: +50 points, Total: {car.total_score}")
                    else:
                        print(f"UID {formatted_uid} already visited, no points added")
                else:
                    print(f"Received non-UID data part: {part}")
    
    # Start simulation thread
    sim_thread = threading.Thread(target=simulate_uid_reception, daemon=True)
    sim_thread.start()
    
    # Let it run for a while to see the score updates
    try:
        time.sleep(25)  # Run for 25 seconds
    except KeyboardInterrupt:
        pass
    finally:
        car.score_display_active = False
        print(f"\n=== TEST ENDED === Final Score: {car.total_score} points ===")

def test_quick_score_display():
    """Test just the score display functionality"""
    print("\nTesting Quick Score Display (every 2 seconds)")
    print("=" * 50)
    
    # Create a simple test
    total_score = 0
    visited_uids = set()
    score_display_active = True
    start_time = time.time()
    game_duration = 15
    
    def score_display_loop():
        while score_display_active:
            time.sleep(2)  # Faster for testing
            if score_display_active:
                remaining_time = max(0, game_duration - (time.time() - start_time))
                print(f"=== SCORE UPDATE === Total Score: {total_score} points | Time Left: {remaining_time:.1f}s ===")
    
    score_thread = threading.Thread(target=score_display_loop, daemon=True)
    score_thread.start()
    
    # Simulate some scoring
    test_scores = [50, 50, 50, 50]
    for i, points in enumerate(test_scores):
        time.sleep(3)
        total_score += points
        print(f"Added {points} points! New total: {total_score}")
    
    time.sleep(5)  # Let it display a few more times
    score_display_active = False
    print("Score display test completed!")

if __name__ == "__main__":
    print("Terminal-Only Mode Test")
    print("="*70)
    
    print("This test will:")
    print("  ✅ Show UID reception in terminal")
    print("  ✅ Display score updates immediately")
    print("  ✅ Show total score every 5 seconds")
    print("  ✅ No GUI scoreboard needed")
    print("")
    
    choice = input("Run full test? (y/N): ").lower()
    if choice == 'y':
        test_terminal_mode()
    else:
        test_quick_score_display()
    
    print("\nExpected behavior:")
    print("  📺 No GUI windows")
    print("  🖥️ All output in terminal")
    print("  ⏰ Score display every 5 seconds")
    print("  🎯 Immediate UID feedback")
    
    print("\nTesting completed!")
