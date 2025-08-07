#!/usr/bin/env python3
"""
Current Day Search for Valheim Database
Searches for current day count and realistic time values
"""

import os
import json
import struct
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import binascii

class ValheimCurrentDaySearcher:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def search_current_day_data(self, db_path: Path) -> Dict[str, Any]:
        """Search for current day and realistic time data"""
        print(f"Searching for current day data in: {db_path.name}")
        
        try:
            with open(db_path, 'rb') as f:
                data = f.read()
            
            day_data = {
                "file_info": {
                    "filename": db_path.name,
                    "size_bytes": len(data),
                    "parsed_at": datetime.now().isoformat()
                },
                "day_values": [],
                "realistic_durations": [],
                "small_time_values": [],
                "potential_day_strings": [],
                "time_related_strings": []
            }
            
            # Search for various day-related patterns
            day_data["day_values"] = self._find_day_values(data)
            day_data["realistic_durations"] = self._find_realistic_durations(data)
            day_data["small_time_values"] = self._find_small_time_values(data)
            day_data["potential_day_strings"] = self._find_day_strings(data)
            day_data["time_related_strings"] = self._find_time_strings(data)
            
            return day_data
            
        except Exception as e:
            return {
                "file_info": {
                    "filename": db_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def _find_day_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find potential day count values (1-1000 range)"""
        day_values = []
        
        # Look for values that could represent current day count
        for i in range(len(data) - 8):
            try:
                # Try 32-bit unsigned integer for day count
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if 1 <= value_32 <= 1000:  # Reasonable day range
                    day_values.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_day",
                        "interpretation": f"Day {value_32}"
                    })
                
                # Try 16-bit unsigned integer for day count
                value_16 = struct.unpack('<H', data[i:i+2])[0]
                if 1 <= value_16 <= 1000:  # Reasonable day range
                    day_values.append({
                        "offset": i,
                        "value": value_16,
                        "type": "16bit_day",
                        "interpretation": f"Day {value_16}"
                    })
                    
            except:
                continue
        
        # Sort by value and remove duplicates
        seen = set()
        unique_values = []
        for item in sorted(day_values, key=lambda x: x["value"]):
            key = (item["value"], item["type"])
            if key not in seen:
                seen.add(key)
                unique_values.append(item)
        
        return unique_values[:30]  # Limit to top 30
    
    def _find_realistic_durations(self, data: bytes) -> List[Dict[str, Any]]:
        """Find realistic duration values (minutes to hours)"""
        durations = []
        
        # Look for values that could represent realistic play sessions
        for i in range(len(data) - 8):
            try:
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                # 1 minute to 24 hours in seconds
                if 60 <= value_32 <= 86400:
                    durations.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_duration",
                        "human_readable": self._format_realistic_duration(value_32)
                    })
                    
            except:
                continue
        
        return sorted(durations, key=lambda x: x["value"], reverse=True)[:20]
    
    def _find_small_time_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find small time values (seconds to minutes)"""
        small_times = []
        
        for i in range(len(data) - 8):
            try:
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                # 1 second to 1 hour
                if 1 <= value_32 <= 3600:
                    small_times.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_small_time",
                        "human_readable": self._format_small_time(value_32)
                    })
                    
            except:
                continue
        
        return sorted(small_times, key=lambda x: x["value"])[:30]
    
    def _find_day_strings(self, data: bytes) -> List[str]:
        """Find strings that might contain day information"""
        day_strings = []
        
        try:
            text = data.decode('utf-8', errors='ignore')
            
            import re
            
            # Look for day-related patterns
            day_patterns = [
                r'day\s*\d+',  # "day 90", "day90"
                r'\d+\s*days?',  # "90 days", "90 day"
                r'current\s*day',
                r'world\s*day',
                r'game\s*day'
            ]
            
            for pattern in day_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                day_strings.extend(matches)
                
        except:
            pass
        
        return list(set(day_strings))[:20]
    
    def _find_time_strings(self, data: bytes) -> List[str]:
        """Find time-related strings"""
        time_strings = []
        
        try:
            text = data.decode('utf-8', errors='ignore')
            
            import re
            
            # Look for time-related patterns
            time_patterns = [
                r'\d{1,2}:\d{2}:\d{2}',  # HH:MM:SS
                r'\d{1,2}:\d{2}',        # HH:MM
                r'\d+\s*minutes?',
                r'\d+\s*hours?',
                r'\d+\s*seconds?'
            ]
            
            for pattern in time_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                time_strings.extend(matches)
                
        except:
            pass
        
        return list(set(time_strings))[:20]
    
    def _format_realistic_duration(self, seconds: int) -> str:
        """Format realistic duration"""
        if seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minutes"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def _format_small_time(self, seconds: int) -> str:
        """Format small time values"""
        if seconds < 60:
            return f"{seconds} seconds"
        else:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds}s"
    
    def search_specific_db(self, db_filename: str) -> Dict[str, Any]:
        """Search for current day data in a specific database file"""
        db_path = self.base_path / "Valheim_PlayerWorldData" / "worlds_local" / db_filename
        if not db_path.exists():
            return {"error": f"File {db_filename} not found"}
        
        return self.search_current_day_data(db_path)
    
    def save_current_day_analysis(self, db_filename: str):
        """Search and save current day analysis"""
        result = self.search_specific_db(db_filename)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return None
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = db_filename.replace('.db', '')
        
        # Save JSON
        json_file = self.output_dir / f"{base_name}_current_day_analysis_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Save text summary
        txt_file = self.output_dir / f"{base_name}_current_day_analysis_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            self._write_current_day_summary(result, f)
        
        print(f"Current day analysis saved to:")
        print(f"  JSON: {json_file}")
        print(f"  Text: {txt_file}")
        
        return json_file, txt_file
    
    def _write_current_day_summary(self, result: Dict[str, Any], f):
        """Write a human-readable current day analysis summary"""
        f.write(f"=== Valheim Current Day Analysis ===\n\n")
        f.write(f"File: {result['file_info']['filename']}\n")
        f.write(f"Size: {result['file_info']['size_bytes']} bytes\n")
        f.write(f"Analyzed: {result['file_info']['parsed_at']}\n\n")
        
        f.write("=== Day Values (Potential Current Day) ===\n")
        day_values = result['day_values']
        if day_values:
            f.write(f"Found {len(day_values)} potential day values:\n")
            for dv in day_values:
                f.write(f"  {dv['interpretation']} (value: {dv['value']}, offset: {dv['offset']}, type: {dv['type']})\n")
        else:
            f.write("No day values found.\n")
        f.write("\n")
        
        f.write("=== Realistic Durations (Minutes to Hours) ===\n")
        durations = result['realistic_durations']
        if durations:
            f.write(f"Found {len(durations)} realistic duration values:\n")
            for dur in durations[:10]:  # Show first 10
                f.write(f"  {dur['human_readable']} (value: {dur['value']}, offset: {dur['offset']})\n")
        else:
            f.write("No realistic duration values found.\n")
        f.write("\n")
        
        f.write("=== Small Time Values (Seconds to Minutes) ===\n")
        small_times = result['small_time_values']
        if small_times:
            f.write(f"Found {len(small_times)} small time values:\n")
            for st in small_times[:15]:  # Show first 15
                f.write(f"  {st['human_readable']} (value: {st['value']}, offset: {st['offset']})\n")
        else:
            f.write("No small time values found.\n")
        f.write("\n")
        
        f.write("=== Day-Related Strings ===\n")
        day_strings = result['potential_day_strings']
        if day_strings:
            f.write(f"Found {len(day_strings)} day-related strings:\n")
            for ds in day_strings:
                f.write(f"  {ds}\n")
        else:
            f.write("No day-related strings found.\n")
        f.write("\n")
        
        f.write("=== Time-Related Strings ===\n")
        time_strings = result['time_related_strings']
        if time_strings:
            f.write(f"Found {len(time_strings)} time-related strings:\n")
            for ts in time_strings:
                f.write(f"  {ts}\n")
        else:
            f.write("No time-related strings found.\n")

def main():
    searcher = ValheimCurrentDaySearcher(".")
    
    # Search for current day data in the specific database file
    db_filename = "DogeheimTesting.db"
    print(f"Searching for current day data in {db_filename}...")
    
    json_file, txt_file = searcher.save_current_day_analysis(db_filename)
    
    if json_file and txt_file:
        print(f"\nCurrent day analysis complete!")
        print(f"Check the text file for a summary of found day data.")

if __name__ == "__main__":
    main()


