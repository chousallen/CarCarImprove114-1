#!/usr/bin/env python3
"""
Test hex string decoding functionality
"""
import logging
from main import MazeCar

logging.basicConfig(level=logging.INFO)

def test_hex_string_decoding():
    """Test various hex string formats"""
    print("Testing hex string decoding functionality")
    print("=" * 50)
    
    # Create MazeCar instance (virtual mode)
    car = MazeCar(bt_port="VIRTUAL")
    
    # Test cases for hex string decoding
    test_cases = [
        # Raw hex strings that might come from Arduino
        "41424344",      # ABCD in hex
        "54455354",      # TEST in hex  
        "31323334",      # 1234 in hex
        "ABCDEF01",      # Direct hex
        "12345678",      # Direct hex
        
        # Already formatted hex
        "0x41424344",    # 0x prefix
        "0xABCDEF01",    # 0x prefix
        
        # TEST format
        "TEST0031",      # Normal TEST format
        "TEST0025",      # Normal TEST format
        
        # Invalid formats
        "INVALID",       # Invalid
        "12G34",         # Invalid hex
        "",              # Empty
        "0",            # Zero
    ]
    
    print("Test cases:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"  {i:2d}. {test_case}")
    print()
    
    print("Hex string decoding results:")
    print("-" * 50)
    
    for test_case in test_cases:
        # Test decoding
        decoded = car._decode_hex_string(test_case)
        
        # Test formatting
        formatted = car._format_uid(decoded)
        
        # Test validation
        is_valid = car._is_valid_uid(formatted)
        
        # Convert hex to ASCII if possible for display
        ascii_repr = ""
        try:
            if decoded.startswith('0x'):
                hex_clean = decoded[2:]
            else:
                hex_clean = decoded
                
            if len(hex_clean) % 2 == 0 and all(c in '0123456789ABCDEFabcdef' for c in hex_clean):
                bytes_data = bytes.fromhex(hex_clean)
                ascii_repr = f" (ASCII: {bytes_data.decode('utf-8', errors='ignore')})"
        except:
            pass
        
        status = "Valid" if is_valid else "Invalid"
        print(f"{test_case:12s} -> {decoded:12s} -> {formatted:12s} [{status}]{ascii_repr}")
    
    print()
    print("Key points:")
    print("  - Hex strings like '41424344' should be decoded and processed")
    print("  - TEST format should be preserved")
    print("  - All valid UIDs should update scoreboard")
    print("  - Invalid data should be printed to terminal")
    print()

def test_scoreboard_integration():
    """Test scoreboard integration with various formats"""
    print("Testing scoreboard integration")
    print("=" * 50)
    
    try:
        car = MazeCar(bt_port="VIRTUAL")
        
        # Test different UID formats
        test_uids = [
            "TEST0031",     # Direct TEST format
            "41424344",     # Hex string (should decode to some value)
            "0x12345678",   # Hex with prefix
            "ABCDEF01",     # Direct hex
        ]
        
        print("Scoreboard update test:")
        initial_score = car.scoreboard.get_current_score()
        print(f"Initial score: {initial_score}")
        
        for uid in test_uids:
            print(f"\nTesting UID: {uid}")
            
            # Decode and format
            decoded = car._decode_hex_string(uid)
            formatted = car._format_uid(decoded)
            is_valid = car._is_valid_uid(formatted)
            
            print(f"  Decoded: {decoded}")
            print(f"  Formatted: {formatted}")
            print(f"  Valid: {is_valid}")
            
            if is_valid:
                score, time_left = car.scoreboard.add_UID(formatted)
                total_score = car.scoreboard.get_current_score()
                print(f"  Score gained: {score}")
                print(f"  Total score: {total_score}")
            else:
                print(f"  Would print to terminal: Received non-UID data: {uid}")
        
        print(f"\nFinal score: {car.scoreboard.get_current_score()}")
        
    except Exception as e:
        print(f"Error during scoreboard test: {e}")

if __name__ == "__main__":
    print("Hex String Decoding Test Tool")
    print("="*60)
    
    # Test hex string decoding
    test_hex_string_decoding()
    
    # Test scoreboard integration
    test_scoreboard_integration()
    
    print("Testing completed")
