#!/usr/bin/env python3
"""
Specific Value Search for Valheim Database
Searches for specific values like 90 and other realistic day counts
"""

import os
import json
import struct
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import binascii

class ValheimSpecificValueSearcher:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def search_specific_values(self, db_path: Path) -> Dict[str, Any]:
        """Search for specific values in the database"""
        print(f"Searching for specific values in: {db_path.name}")
        
        try:
            with open(db_path, 'rb') as f:
                data = f.read()
            
            specific_data = {
                "file_info": {
                    "filename": db_path.name,
                    "size_bytes": len(data),
                    "parsed_at": datetime.now().isoformat()
                },
                "day_90_values": [],
                "day_80_100_values": [],
                "day_50_150_values": [],
                "exact_90_values": [],
                "time_related_90s": []
            }
            
            # Search for specific day-related values
            specific_data["day_90_values"] = self._find_day_90_values(data)
            specific_data["day_80_100_values"] = self._find_day_80_100_values(data)
            specific_data["day_50_150_values"] = self._find_day_50_150_values(data)
            specific_data["exact_90_values"] = self._find_exact_90_values(data)
            specific_data["time_related_90s"] = self._find_time_related_90s(data)
            
            return specific_data
            
        except Exception as e:
            return {
                "file_info": {
                    "filename": db_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def _find_day_90_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find values specifically around 90 (85-95)"""
        day_90_values = []
        
        for i in range(len(data) - 8):
            try:
                # Try 32-bit unsigned integer
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if 85 <= value_32 <= 95:  # Around day 90
                    day_90_values.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_uint",
                        "interpretation": f"Day {value_32}"
                    })
                
                # Try 16-bit unsigned integer
                value_16 = struct.unpack('<H', data[i:i+2])[0]
                if 85 <= value_16 <= 95:  # Around day 90
                    day_90_values.append({
                        "offset": i,
                        "value": value_16,
                        "type": "16bit_uint",
                        "interpretation": f"Day {value_16}"
                    })
                    
            except:
                continue
        
        return sorted(day_90_values, key=lambda x: x["value"])
    
    def _find_day_80_100_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find values in the 80-100 range"""
        day_80_100_values = []
        
        for i in range(len(data) - 8):
            try:
                # Try 32-bit unsigned integer
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if 80 <= value_32 <= 100:
                    day_80_100_values.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_uint",
                        "interpretation": f"Day {value_32}"
                    })
                
                # Try 16-bit unsigned integer
                value_16 = struct.unpack('<H', data[i:i+2])[0]
                if 80 <= value_16 <= 100:
                    day_80_100_values.append({
                        "offset": i,
                        "value": value_16,
                        "type": "16bit_uint",
                        "interpretation": f"Day {value_16}"
                    })
                    
            except:
                continue
        
        return sorted(day_80_100_values, key=lambda x: x["value"])
    
    def _find_day_50_150_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find values in the 50-150 range"""
        day_50_150_values = []
        
        for i in range(len(data) - 8):
            try:
                # Try 32-bit unsigned integer
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if 50 <= value_32 <= 150:
                    day_50_150_values.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_uint",
                        "interpretation": f"Day {value_32}"
                    })
                
                # Try 16-bit unsigned integer
                value_16 = struct.unpack('<H', data[i:i+2])[0]
                if 50 <= value_16 <= 150:
                    day_50_150_values.append({
                        "offset": i,
                        "value": value_16,
                        "type": "16bit_uint",
                        "interpretation": f"Day {value_16}"
                    })
                    
            except:
                continue
        
        return sorted(day_50_150_values, key=lambda x: x["value"])[:50]  # Limit to top 50
    
    def _find_exact_90_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find exact value 90"""
        exact_90_values = []
        
        for i in range(len(data) - 8):
            try:
                # Try 32-bit unsigned integer
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if value_32 == 90:
                    exact_90_values.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_uint",
                        "interpretation": "Day 90"
                    })
                
                # Try 16-bit unsigned integer
                value_16 = struct.unpack('<H', data[i:i+2])[0]
                if value_16 == 90:
                    exact_90_values.append({
                        "offset": i,
                        "value": value_16,
                        "type": "16bit_uint",
                        "interpretation": "Day 90"
                    })
                
                # Try 8-bit unsigned integer
                value_8 = struct.unpack('<B', data[i:i+1])[0]
                if value_8 == 90:
                    exact_90_values.append({
                        "offset": i,
                        "value": value_8,
                        "type": "8bit_uint",
                        "interpretation": "Day 90"
                    })
                    
            except:
                continue
        
        return exact_90_values
    
    def _find_time_related_90s(self, data: bytes) -> List[Dict[str, Any]]:
        """Find time-related values that might be 90 seconds/minutes"""
        time_90s = []
        
        for i in range(len(data) - 8):
            try:
                # Look for 90 seconds (5400 seconds = 90 minutes)
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if value_32 == 90:  # 90 seconds
                    time_90s.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_seconds",
                        "interpretation": "90 seconds"
                    })
                elif value_32 == 5400:  # 90 minutes
                    time_90s.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_seconds",
                        "interpretation": "90 minutes"
                    })
                    
            except:
                continue
        
        return time_90s
    
    def search_specific_db(self, db_filename: str) -> Dict[str, Any]:
        """Search for specific values in a specific database file"""
        db_path = self.base_path / "Valheim_PlayerWorldData" / "worlds_local" / db_filename
        if not db_path.exists():
            return {"error": f"File {db_filename} not found"}
        
        return self.search_specific_values(db_path)
    
    def save_specific_analysis(self, db_filename: str):
        """Search and save specific value analysis"""
        result = self.search_specific_db(db_filename)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return None
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = db_filename.replace('.db', '')
        
        # Save JSON
        json_file = self.output_dir / f"{base_name}_specific_values_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Save text summary
        txt_file = self.output_dir / f"{base_name}_specific_values_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            self._write_specific_summary(result, f)
        
        print(f"Specific value analysis saved to:")
        print(f"  JSON: {json_file}")
        print(f"  Text: {txt_file}")
        
        return json_file, txt_file
    
    def _write_specific_summary(self, result: Dict[str, Any], f):
        """Write a human-readable specific value analysis summary"""
        f.write(f"=== Valheim Specific Value Analysis ===\n\n")
        f.write(f"File: {result['file_info']['filename']}\n")
        f.write(f"Size: {result['file_info']['size_bytes']} bytes\n")
        f.write(f"Analyzed: {result['file_info']['parsed_at']}\n\n")
        
        f.write("=== Exact Day 90 Values ===\n")
        exact_90s = result['exact_90_values']
        if exact_90s:
            f.write(f"Found {len(exact_90s)} exact day 90 values:\n")
            for val in exact_90s:
                f.write(f"  {val['interpretation']} (value: {val['value']}, offset: {val['offset']}, type: {val['type']})\n")
        else:
            f.write("No exact day 90 values found.\n")
        f.write("\n")
        
        f.write("=== Day Values Around 90 (85-95) ===\n")
        day_90s = result['day_90_values']
        if day_90s:
            f.write(f"Found {len(day_90s)} day values around 90:\n")
            for val in day_90s:
                f.write(f"  {val['interpretation']} (value: {val['value']}, offset: {val['offset']}, type: {val['type']})\n")
        else:
            f.write("No day values around 90 found.\n")
        f.write("\n")
        
        f.write("=== Day Values 80-100 ===\n")
        day_80_100s = result['day_80_100_values']
        if day_80_100s:
            f.write(f"Found {len(day_80_100s)} day values in 80-100 range:\n")
            for val in day_80_100s:
                f.write(f"  {val['interpretation']} (value: {val['value']}, offset: {val['offset']}, type: {val['type']})\n")
        else:
            f.write("No day values in 80-100 range found.\n")
        f.write("\n")
        
        f.write("=== Day Values 50-150 (Top 20) ===\n")
        day_50_150s = result['day_50_150_values']
        if day_50_150s:
            f.write(f"Found {len(day_50_150s)} day values in 50-150 range (showing top 20):\n")
            for val in day_50_150s[:20]:
                f.write(f"  {val['interpretation']} (value: {val['value']}, offset: {val['offset']}, type: {val['type']})\n")
        else:
            f.write("No day values in 50-150 range found.\n")
        f.write("\n")
        
        f.write("=== Time-Related 90s ===\n")
        time_90s = result['time_related_90s']
        if time_90s:
            f.write(f"Found {len(time_90s)} time-related 90 values:\n")
            for val in time_90s:
                f.write(f"  {val['interpretation']} (value: {val['value']}, offset: {val['offset']}, type: {val['type']})\n")
        else:
            f.write("No time-related 90 values found.\n")

def main():
    searcher = ValheimSpecificValueSearcher(".")
    
    # Search for specific values in the database file
    db_filename = "DogeheimTesting.db"
    print(f"Searching for specific values in {db_filename}...")
    
    json_file, txt_file = searcher.save_specific_analysis(db_filename)
    
    if json_file and txt_file:
        print(f"\nSpecific value analysis complete!")
        print(f"Check the text file for a summary of found values.")

if __name__ == "__main__":
    main()


