#!/usr/bin/env python3
"""
Quick 90 Search for Valheim Database
Quickly searches for the value 90 in the database
"""

import struct
from pathlib import Path

def search_for_90(db_path: str):
    """Search for the value 90 in the database"""
    print(f"Searching for value 90 in: {db_path}")
    
    with open(db_path, 'rb') as f:
        data = f.read()
    
    count_32bit = 0
    count_16bit = 0
    count_8bit = 0
    
    # Search for 32-bit value 90
    for i in range(len(data) - 4):
        try:
            value = struct.unpack('<I', data[i:i+4])[0]
            if value == 90:
                count_32bit += 1
                if count_32bit <= 5:  # Show first 5 occurrences
                    print(f"  32-bit 90 found at offset {i}")
        except:
            continue
    
    # Search for 16-bit value 90
    for i in range(len(data) - 2):
        try:
            value = struct.unpack('<H', data[i:i+2])[0]
            if value == 90:
                count_16bit += 1
                if count_16bit <= 5:  # Show first 5 occurrences
                    print(f"  16-bit 90 found at offset {i}")
        except:
            continue
    
    # Search for 8-bit value 90
    for i in range(len(data) - 1):
        try:
            value = struct.unpack('<B', data[i:i+1])[0]
            if value == 90:
                count_8bit += 1
                if count_8bit <= 5:  # Show first 5 occurrences
                    print(f"  8-bit 90 found at offset {i}")
        except:
            continue
    
    print(f"\nSummary:")
    print(f"  32-bit value 90: {count_32bit} occurrences")
    print(f"  16-bit value 90: {count_16bit} occurrences")
    print(f"  8-bit value 90: {count_8bit} occurrences")
    print(f"  Total: {count_32bit + count_16bit + count_8bit} occurrences")

if __name__ == "__main__":
    db_path = "Valheim_PlayerWorldData/worlds_local/DogeheimTesting.db"
    search_for_90(db_path)


