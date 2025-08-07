#!/usr/bin/env python3
"""
Time Data Search for Valheim Database
Searches for time-related information in Valheim .db files
"""

import os
import json
import struct
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import binascii

class ValheimTimeSearcher:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def search_time_data(self, db_path: Path) -> Dict[str, Any]:
        """Search for time-related data in the database"""
        print(f"Searching for time data in: {db_path.name}")
        
        try:
            with open(db_path, 'rb') as f:
                data = f.read()
            
            time_data = {
                "file_info": {
                    "filename": db_path.name,
                    "size_bytes": len(data),
                    "parsed_at": datetime.now().isoformat()
                },
                "time_values": [],
                "timestamp_values": [],
                "duration_values": [],
                "date_strings": [],
                "time_strings": [],
                "potential_time_data": []
            }
            
            # Search for various time-related patterns
            time_data["time_values"] = self._find_time_values(data)
            time_data["timestamp_values"] = self._find_timestamp_values(data)
            time_data["duration_values"] = self._find_duration_values(data)
            time_data["date_strings"] = self._find_date_strings(data)
            time_data["time_strings"] = self._find_time_strings(data)
            time_data["potential_time_data"] = self._find_potential_time_data(data)
            
            return time_data
            
        except Exception as e:
            return {
                "file_info": {
                    "filename": db_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def _find_time_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find potential time values (seconds, minutes, hours)"""
        time_values = []
        
        # Look for 32-bit and 64-bit values that could represent time
        for i in range(len(data) - 8):
            try:
                # Try 32-bit unsigned integer
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if 1 <= value_32 <= 3153600000:  # Reasonable time range (up to 100 years in seconds)
                    time_values.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_uint",
                        "interpretation": self._interpret_time_value(value_32)
                    })
                
                # Try 64-bit unsigned integer
                value_64 = struct.unpack('<Q', data[i:i+8])[0]
                if 1 <= value_64 <= 3153600000000000:  # Reasonable time range
                    time_values.append({
                        "offset": i,
                        "value": value_64,
                        "type": "64bit_uint",
                        "interpretation": self._interpret_time_value(value_64)
                    })
                    
            except:
                continue
        
        # Sort by value and remove duplicates
        seen = set()
        unique_values = []
        for item in sorted(time_values, key=lambda x: x["value"]):
            key = (item["value"], item["type"])
            if key not in seen:
                seen.add(key)
                unique_values.append(item)
        
        return unique_values[:50]  # Limit to top 50
    
    def _find_timestamp_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find potential timestamp values (Unix timestamps)"""
        timestamps = []
        
        # Look for Unix timestamps (seconds since epoch)
        current_time = int(time.time())
        min_reasonable = current_time - (365 * 24 * 3600 * 10)  # 10 years ago
        max_reasonable = current_time + (365 * 24 * 3600 * 10)  # 10 years in future
        
        for i in range(len(data) - 8):
            try:
                # Try 32-bit timestamp
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if min_reasonable <= value_32 <= max_reasonable:
                    timestamps.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_timestamp",
                        "datetime": datetime.fromtimestamp(value_32).isoformat(),
                        "human_readable": datetime.fromtimestamp(value_32).strftime("%Y-%m-%d %H:%M:%S")
                    })
                
                # Try 64-bit timestamp (milliseconds)
                value_64 = struct.unpack('<Q', data[i:i+8])[0]
                if min_reasonable * 1000 <= value_64 <= max_reasonable * 1000:
                    timestamp_seconds = value_64 / 1000
                    timestamps.append({
                        "offset": i,
                        "value": value_64,
                        "type": "64bit_timestamp_ms",
                        "datetime": datetime.fromtimestamp(timestamp_seconds).isoformat(),
                        "human_readable": datetime.fromtimestamp(timestamp_seconds).strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
            except:
                continue
        
        return sorted(timestamps, key=lambda x: x["value"])[:20]
    
    def _find_duration_values(self, data: bytes) -> List[Dict[str, Any]]:
        """Find potential duration values (playtime, session time)"""
        durations = []
        
        # Look for values that could represent duration in seconds
        for i in range(len(data) - 8):
            try:
                value_32 = struct.unpack('<I', data[i:i+4])[0]
                if 60 <= value_32 <= 31536000:  # 1 minute to 1 year in seconds
                    durations.append({
                        "offset": i,
                        "value": value_32,
                        "type": "32bit_duration",
                        "human_readable": self._format_duration(value_32)
                    })
                    
            except:
                continue
        
        return sorted(durations, key=lambda x: x["value"], reverse=True)[:20]
    
    def _find_date_strings(self, data: bytes) -> List[str]:
        """Find date-like strings in the data"""
        date_strings = []
        
        # Try to decode as text and look for date patterns
        try:
            text = data.decode('utf-8', errors='ignore')
            
            # Look for various date patterns
            import re
            
            # YYYY-MM-DD pattern
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
                r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, text)
                date_strings.extend(matches)
                
        except:
            pass
        
        return list(set(date_strings))[:20]
    
    def _find_time_strings(self, data: bytes) -> List[str]:
        """Find time-like strings in the data"""
        time_strings = []
        
        try:
            text = data.decode('utf-8', errors='ignore')
            
            import re
            
            # Look for time patterns
            time_patterns = [
                r'\d{2}:\d{2}:\d{2}',  # HH:MM:SS
                r'\d{2}:\d{2}',        # HH:MM
                r'\d{1,2}:\d{2}:\d{2}', # H:MM:SS
            ]
            
            for pattern in time_patterns:
                matches = re.findall(pattern, text)
                time_strings.extend(matches)
                
        except:
            pass
        
        return list(set(time_strings))[:20]
    
    def _find_potential_time_data(self, data: bytes) -> List[Dict[str, Any]]:
        """Find other potential time-related data"""
        potential_data = []
        
        # Look for strings that might contain time information
        try:
            text = data.decode('utf-8', errors='ignore')
            
            time_keywords = [
                'time', 'duration', 'session', 'playtime', 'hours', 'minutes', 'seconds',
                'start', 'end', 'created', 'modified', 'last', 'first', 'total'
            ]
            
            lines = text.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower()
                for keyword in time_keywords:
                    if keyword in line_lower:
                        potential_data.append({
                            "line_number": i,
                            "line": line.strip(),
                            "keyword": keyword
                        })
                        break
                        
        except:
            pass
        
        return potential_data[:50]
    
    def _interpret_time_value(self, value: int) -> str:
        """Interpret a numeric value as time"""
        if value < 60:
            return f"{value} seconds"
        elif value < 3600:
            minutes = value // 60
            seconds = value % 60
            return f"{minutes}m {seconds}s"
        elif value < 86400:
            hours = value // 3600
            minutes = (value % 3600) // 60
            return f"{hours}h {minutes}m"
        else:
            days = value // 86400
            hours = (value % 86400) // 3600
            return f"{days}d {hours}h"
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in a human-readable way"""
        if seconds < 60:
            return f"{seconds} seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minutes"
        elif seconds < 86400:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours} hours {minutes} minutes"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            return f"{days} days {hours} hours"
    
    def search_specific_db(self, db_filename: str) -> Dict[str, Any]:
        """Search for time data in a specific database file"""
        db_path = self.base_path / "Valheim_PlayerWorldData" / "worlds_local" / db_filename
        if not db_path.exists():
            return {"error": f"File {db_filename} not found"}
        
        return self.search_time_data(db_path)
    
    def save_time_analysis(self, db_filename: str):
        """Search and save time analysis"""
        result = self.search_specific_db(db_filename)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return None
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = db_filename.replace('.db', '')
        
        # Save JSON
        json_file = self.output_dir / f"{base_name}_time_analysis_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Save text summary
        txt_file = self.output_dir / f"{base_name}_time_analysis_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            self._write_time_summary(result, f)
        
        print(f"Time analysis saved to:")
        print(f"  JSON: {json_file}")
        print(f"  Text: {txt_file}")
        
        return json_file, txt_file
    
    def _write_time_summary(self, result: Dict[str, Any], f):
        """Write a human-readable time analysis summary"""
        f.write(f"=== Valheim Time Data Analysis ===\n\n")
        f.write(f"File: {result['file_info']['filename']}\n")
        f.write(f"Size: {result['file_info']['size_bytes']} bytes\n")
        f.write(f"Analyzed: {result['file_info']['parsed_at']}\n\n")
        
        f.write("=== Timestamp Values ===\n")
        timestamps = result['timestamp_values']
        if timestamps:
            f.write(f"Found {len(timestamps)} timestamp values:\n")
            for ts in timestamps[:10]:  # Show first 10
                f.write(f"  {ts['human_readable']} (value: {ts['value']}, offset: {ts['offset']})\n")
        else:
            f.write("No timestamp values found.\n")
        f.write("\n")
        
        f.write("=== Duration Values ===\n")
        durations = result['duration_values']
        if durations:
            f.write(f"Found {len(durations)} duration values:\n")
            for dur in durations[:10]:  # Show first 10
                f.write(f"  {dur['human_readable']} (value: {dur['value']}, offset: {dur['offset']})\n")
        else:
            f.write("No duration values found.\n")
        f.write("\n")
        
        f.write("=== Time Values ===\n")
        time_values = result['time_values']
        if time_values:
            f.write(f"Found {len(time_values)} potential time values:\n")
            for tv in time_values[:10]:  # Show first 10
                f.write(f"  {tv['interpretation']} (value: {tv['value']}, offset: {tv['offset']})\n")
        else:
            f.write("No time values found.\n")
        f.write("\n")
        
        f.write("=== Date Strings ===\n")
        date_strings = result['date_strings']
        if date_strings:
            f.write(f"Found {len(date_strings)} date strings:\n")
            for ds in date_strings:
                f.write(f"  {ds}\n")
        else:
            f.write("No date strings found.\n")
        f.write("\n")
        
        f.write("=== Time Strings ===\n")
        time_strings = result['time_strings']
        if time_strings:
            f.write(f"Found {len(time_strings)} time strings:\n")
            for ts in time_strings:
                f.write(f"  {ts}\n")
        else:
            f.write("No time strings found.\n")
        f.write("\n")
        
        f.write("=== Potential Time Data ===\n")
        potential_data = result['potential_time_data']
        if potential_data:
            f.write(f"Found {len(potential_data)} lines with time-related keywords:\n")
            for pd in potential_data[:10]:  # Show first 10
                f.write(f"  Line {pd['line_number']}: {pd['line']} (keyword: {pd['keyword']})\n")
        else:
            f.write("No potential time data found.\n")

def main():
    searcher = ValheimTimeSearcher(".")
    
    # Search for time data in the specific database file
    db_filename = "DogeheimTesting.db"
    print(f"Searching for time data in {db_filename}...")
    
    json_file, txt_file = searcher.save_time_analysis(db_filename)
    
    if json_file and txt_file:
        print(f"\nTime analysis complete!")
        print(f"Check the text file for a summary of found time data.")

if __name__ == "__main__":
    main()
