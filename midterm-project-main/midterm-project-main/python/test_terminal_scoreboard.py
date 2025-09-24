#!/usr/bin/env python3
"""
Test terminal output and scoreboard update for valid UIDs
"""
import logging
import time
from main import MazeCar

logging.basicConfig(level=logging.INFO)

def test_terminal_and_scoreboard():
    """Test that valid UIDs show in terminal and update scoreboard with 50 points"""
    print("Testing Terminal Output and Scoreboard Update")
    print("=" * 60)
    
    # Create MazeCar instance (virtual mode)
    car = MazeCar(bt_port="VIRTUAL")
    
    # Test mixed data strings
    test_cases = [
        "debug info TEST0031 sensor data",
        "temperature 25.5 41424344 status ok",
        "TEST0025 battery 80%",
        "sensor reading 0x12345678 error none",
        "invalid data xyz123 debug info",  # No valid UID
        "multiple TEST0044 and ABCDEF01 UIDs here",
    ]
    
    print(f"Initial score: {car.scoreboard.get_current_score()}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. Testing: '{test_case}'")
        print("   Terminal output:")
        
        # Simulate the string processing
        parts = test_case.split()
        valid_uid_found = False
        
        for part in parts:
            if not part.strip():
                continue
                
            # Process each part
            decoded_uid = car._decode_hex_string(part.strip())
            formatted_uid = car._format_uid(decoded_uid)
            
            if car._is_valid_uid(formatted_uid):
                # Show in terminal (this is what will be printed)
                print(f"   Valid UID received: {formatted_uid}")
                
                # Update scoreboard
                score, time_left = car.scoreboard.add_UID(formatted_uid)
                total_score = car.scoreboard.get_current_score()
                print(f"   Scoreboard updated: +{score} points, Total: {total_score}")
                
                valid_uid_found = True
            else:
                # Non-UID data
                print(f"   Received non-UID data part: {part}")
        
        if not valid_uid_found:
            print(f"   Received non-UID data: {test_case}")
        
        print()

def test_scoreboard_fixed_points():
    """Test that all UIDs get exactly 50 points"""
    print("Testing Fixed 50 Points for All UIDs")
    print("=" * 40)
    
    car = MazeCar(bt_port="VIRTUAL")
    
    # Different types of UIDs
    test_uids = [
        "TEST0031",      # Known UID in CSV
        "TEST0025",      # Known UID in CSV  
        "TEST0044",      # Known UID in CSV
        "41424344",      # Hex string
        "0x12345678",    # Hex with prefix
        "ABCDEF01",      # Pure hex
        "UNKNOWN123",    # Unknown UID (should still get 50)
    ]
    
    initial_score = car.scoreboard.get_current_score()
    print(f"Initial score: {initial_score}")
    
    for uid in test_uids:
        print(f"\nTesting UID: {uid}")
        
        # Process UID
        decoded = car._decode_hex_string(uid)
        formatted = car._format_uid(decoded)
        
        if car._is_valid_uid(formatted):
            score, time_left = car.scoreboard.add_UID(formatted)
            total_score = car.scoreboard.get_current_score()
            
            print(f"  Formatted: {formatted}")
            print(f"  Score gained: {score}")
            print(f"  Total score: {total_score}")
            
            # Verify it's exactly 50 points
            if score == 50:
                print(f"  ✅ Correct: Got exactly 50 points")
            else:
                print(f"  ❌ Error: Expected 50 points, got {score}")
        else:
            print(f"  ❌ Invalid UID format")
    
    final_score = car.scoreboard.get_current_score()
    expected_score = initial_score + (len([uid for uid in test_uids if car._is_valid_uid(car._format_uid(car._decode_hex_string(uid)))]) * 50)
    
    print(f"\nFinal score: {final_score}")
    print(f"Expected score: {expected_score}")
    
    if final_score == expected_score:
        print("✅ All UIDs correctly scored 50 points each")
    else:
        print("❌ Scoring error detected")

if __name__ == "__main__":
    print("Terminal Output and Scoreboard Test")
    print("="*70)
    
    # Test terminal output and scoreboard update
    test_terminal_and_scoreboard()
    
    print("\n" + "="*70)
    
    # Test fixed 50 points scoring
    test_scoreboard_fixed_points()
    
    print("\nExpected behavior:")
    print("  ✅ Valid UIDs shown in terminal")
    print("  ✅ Scoreboard updated with +50 points each")
    print("  ✅ Non-UID data shown in terminal")
    print("  ✅ No position/node status updates needed")
    
    print("\nTesting completed!")
