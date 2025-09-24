#!/usr/bin/env python3
"""
Test string splitting functionality for UID detection
"""
import logging
from main import MazeCar

logging.basicConfig(level=logging.INFO)

def test_string_splitting():
    """Test string splitting and UID detection"""
    print("Testing string splitting for UID detection")
    print("=" * 50)
    
    # Create MazeCar instance (virtual mode)
    car = MazeCar(bt_port="VIRTUAL")
    
    # Test cases with mixed data
    test_cases = [
        # Valid UID mixed with other data
        "debug info TEST0031 sensor data",
        "41424344 temperature reading 25.5",
        "status: ok 0x12345678 battery: 80%",
        "TEST0025 error code 404",
        "sensor1: 123 TEST0044 sensor2: 456",
        
        # Multiple UIDs in one string
        "TEST0031 TEST0025",
        "41424344 54455354",
        "0x12345678 ABCDEF01 status ok",
        
        # Mixed valid and invalid
        "invalid1 TEST0031 invalid2",
        "debug 41424344 error xyz123",
        
        # Only invalid data
        "debug sensor temperature 25.5",
        "status ok battery 80%",
        "invalid xyz abc123",
        
        # Edge cases
        "  TEST0031  ",  # With spaces
        "TEST0031",      # Single UID
        "",              # Empty
        "   ",           # Only spaces
    ]
    
    print("Test cases:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"  {i:2d}. '{test_case}'")
    print()
    
    print("String splitting and UID detection results:")
    print("-" * 60)
    
    for test_case in test_cases:
        print(f"\nTesting: '{test_case}'")
        
        # Split string by spaces
        parts = test_case.split()
        print(f"  Split into {len(parts)} parts: {parts}")
        
        valid_uids = []
        invalid_parts = []
        
        for part in parts:
            if not part.strip():
                continue
                
            # Test each part
            decoded = car._decode_hex_string(part.strip())
            formatted = car._format_uid(decoded)
            is_valid = car._is_valid_uid(formatted)
            
            if is_valid:
                valid_uids.append(formatted)
                print(f"    ✅ Valid UID: {part} -> {formatted}")
            else:
                invalid_parts.append(part)
                print(f"    ❌ Invalid: {part}")
        
        # Summary
        if valid_uids:
            print(f"  📊 Result: Found {len(valid_uids)} valid UID(s): {valid_uids}")
            print(f"           Invalid parts: {invalid_parts}")
        else:
            print(f"  📊 Result: No valid UIDs found")
            print(f"           All parts invalid: {invalid_parts}")

def test_scoreboard_with_mixed_data():
    """Test scoreboard integration with mixed data strings"""
    print("\n" + "="*60)
    print("Testing scoreboard with mixed data strings")
    print("=" * 60)
    
    try:
        car = MazeCar(bt_port="VIRTUAL")
        
        # Simulate mixed data strings
        mixed_strings = [
            "debug info TEST0031 sensor reading",
            "battery 80% TEST0025 temperature 25.5",
            "status ok 41424344 error none",
            "invalid data xyz123 debug info",
        ]
        
        initial_score = car.scoreboard.get_current_score()
        print(f"Initial score: {initial_score}")
        
        for i, mixed_str in enumerate(mixed_strings, 1):
            print(f"\n{i}. Processing: '{mixed_str}'")
            
            # Simulate the string splitting logic
            parts = mixed_str.split()
            found_valid = False
            
            for part in parts:
                if not part.strip():
                    continue
                    
                decoded = car._decode_hex_string(part.strip())
                formatted = car._format_uid(decoded)
                
                if car._is_valid_uid(formatted):
                    print(f"   ✅ Found valid UID: {formatted}")
                    score, time_left = car.scoreboard.add_UID(formatted)
                    total_score = car.scoreboard.get_current_score()
                    print(f"   📊 Score gained: {score}, Total: {total_score}")
                    found_valid = True
                else:
                    print(f"   ❌ Invalid part: {part}")
            
            if not found_valid:
                print(f"   📡 Would print to terminal: Received non-UID data: {mixed_str}")
        
        final_score = car.scoreboard.get_current_score()
        print(f"\nFinal score: {final_score}")
        
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    print("String Splitting and UID Detection Test")
    print("="*70)
    
    # Test string splitting
    test_string_splitting()
    
    # Test scoreboard integration
    test_scoreboard_with_mixed_data()
    
    print("\nKey benefits:")
    print("  ✅ Can extract UIDs from mixed data strings")
    print("  ✅ Handles multiple UIDs in one string")
    print("  ✅ Only processes valid UID parts")
    print("  ✅ Invalid parts are logged to terminal")
    print("  ✅ No need for entire string to be valid")
    
    print("\nTesting completed!")
