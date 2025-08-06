#!/usr/bin/env python3
"""
Valheim World Database Parser
Parses Valheim's custom .db world database format and converts to readable JSON
"""

import os
import json
import struct
import zlib
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import binascii

class ValheimWorldDBParser:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def parse_world_db(self, db_path: Path) -> Dict[str, Any]:
        """Parse Valheim world database file (.db)"""
        print(f"Parsing Valheim world database: {db_path.name}")
        
        try:
            with open(db_path, 'rb') as f:
                data = f.read()
            
            world_data = {
                "file_info": {
                    "filename": db_path.name,
                    "size_bytes": len(data),
                    "size_mb": round(len(data) / (1024 * 1024), 2),
                    "parsed_at": datetime.now().isoformat()
                },
                "header": {},
                "sections": {},
                "analysis": {}
            }
            
            # Parse header (first 4 bytes might be version or magic number)
            if len(data) >= 4:
                header_value = struct.unpack('<I', data[:4])[0]
                world_data["header"]["magic_number"] = header_value
                world_data["header"]["magic_hex"] = f"0x{header_value:08x}"
            
            # Analyze data patterns
            world_data["analysis"]["data_patterns"] = self._analyze_data_patterns(data)
            
            # Try to identify sections by looking for patterns
            world_data["sections"] = self._identify_sections(data)
            
            # Look for strings and readable content
            world_data["strings"] = self._extract_strings(data)
            
            # Look for potential compressed data
            world_data["compressed_sections"] = self._find_compressed_sections(data)
            
            return world_data
            
        except Exception as e:
            return {
                "file_info": {
                    "filename": db_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def _analyze_data_patterns(self, data: bytes) -> Dict[str, Any]:
        """Analyze patterns in the binary data"""
        patterns = {
            "null_bytes": data.count(b'\x00'),
            "null_percentage": round(data.count(b'\x00') / len(data) * 100, 2),
            "common_bytes": {},
            "repeating_patterns": []
        }
        
        # Find most common byte values
        byte_counts = {}
        for byte in data:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
        
        # Get top 10 most common bytes
        sorted_bytes = sorted(byte_counts.items(), key=lambda x: x[1], reverse=True)
        patterns["common_bytes"] = {f"0x{b:02x}": count for b, count in sorted_bytes[:10]}
        
        # Look for repeating patterns
        for pattern_len in [2, 4, 8]:
            pattern_counts = {}
            for i in range(len(data) - pattern_len):
                pattern = data[i:i+pattern_len]
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
            # Find patterns that repeat more than 3 times
            repeating = [(p, c) for p, c in pattern_counts.items() if c > 3]
            if repeating:
                patterns["repeating_patterns"].append({
                    "length": pattern_len,
                    "patterns": [(p.hex(), c) for p, c in sorted(repeating, key=lambda x: x[1], reverse=True)[:5]]
                })
        
        return patterns
    
    def _identify_sections(self, data: bytes) -> Dict[str, Any]:
        """Try to identify different sections in the data"""
        sections = {}
        
        # Look for potential section boundaries (large blocks of zeros, etc.)
        zero_runs = []
        current_run = 0
        for i, byte in enumerate(data):
            if byte == 0:
                current_run += 1
            else:
                if current_run > 100:  # Significant run of zeros
                    zero_runs.append((i - current_run, i - 1, current_run))
                current_run = 0
        
        sections["zero_runs"] = [
            {"start": start, "end": end, "length": length}
            for start, end, length in sorted(zero_runs, key=lambda x: x[2], reverse=True)[:10]
        ]
        
        # Look for potential data blocks (non-zero regions)
        non_zero_regions = []
        start = None
        for i, byte in enumerate(data):
            if byte != 0 and start is None:
                start = i
            elif byte == 0 and start is not None:
                if i - start > 50:  # Significant non-zero region
                    non_zero_regions.append((start, i - 1, i - start))
                start = None
        
        sections["data_regions"] = [
            {"start": start, "end": end, "length": length, "sample": data[start:start+20].hex()}
            for start, end, length in sorted(non_zero_regions, key=lambda x: x[2], reverse=True)[:10]
        ]
        
        return sections
    
    def _extract_strings(self, data: bytes) -> Dict[str, Any]:
        """Extract readable strings from the data"""
        strings = {
            "ascii_strings": [],
            "utf8_strings": [],
            "potential_names": []
        }
        
        # Look for ASCII strings (printable characters)
        current_string = ""
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) > 3:  # Minimum length for meaningful strings
                    strings["ascii_strings"].append(current_string)
                current_string = ""
        
        # Also try to decode as UTF-8
        try:
            text = data.decode('utf-8', errors='ignore')
            # Extract words that might be names
            words = text.split()
            potential_names = [word for word in words if len(word) > 2 and word.isalpha()]
            strings["potential_names"] = list(set(potential_names))[:20]  # Top 20 unique names
        except:
            pass
        
        # Remove duplicates and sort by length
        strings["ascii_strings"] = sorted(list(set(strings["ascii_strings"])), key=len, reverse=True)[:50]
        
        return strings
    
    def _find_compressed_sections(self, data: bytes) -> Dict[str, Any]:
        """Look for potentially compressed data sections"""
        compressed = {
            "zlib_signatures": [],
            "potential_compressed": []
        }
        
        # Look for zlib signatures
        for i in range(len(data) - 2):
            if data[i] == 0x78:  # zlib header
                if data[i+1] in [0x01, 0x5e, 0x9c, 0xda]:  # Common zlib flags
                    compressed["zlib_signatures"].append({
                        "offset": i,
                        "header": data[i:i+2].hex()
                    })
        
        # Look for sections with high entropy (potentially compressed)
        for i in range(0, len(data) - 1024, 1024):
            chunk = data[i:i+1024]
            if len(chunk) == 1024:
                # Calculate entropy
                byte_counts = [0] * 256
                for byte in chunk:
                    byte_counts[byte] += 1
                
                entropy = 0
                for count in byte_counts:
                    if count > 0:
                        p = count / 1024
                        entropy -= p * math.log2(p)  # Proper entropy calculation
                
                if entropy > 7.5:  # High entropy might indicate compression
                    compressed["potential_compressed"].append({
                        "offset": i,
                        "entropy": round(entropy, 2),
                        "sample": chunk[:20].hex()
                    })
        
        return compressed
    
    def parse_specific_db(self, db_filename: str) -> Dict[str, Any]:
        """Parse a specific database file"""
        db_path = self.base_path / "Valheim_PlayerWorldData" / "worlds_local" / db_filename
        if not db_path.exists():
            return {"error": f"File {db_filename} not found"}
        
        return self.parse_world_db(db_path)
    
    def save_readable_version(self, db_filename: str, output_format: str = "json"):
        """Parse and save a readable version of the database"""
        result = self.parse_specific_db(db_filename)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return None
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = db_filename.replace('.db', '')
        
        if output_format == "json":
            output_file = self.output_dir / f"{base_name}_readable_{timestamp}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        elif output_format == "txt":
            output_file = self.output_dir / f"{base_name}_readable_{timestamp}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                self._write_text_summary(result, f)
        
        print(f"Readable version saved to: {output_file}")
        return output_file
    
    def _write_text_summary(self, result: Dict[str, Any], f):
        """Write a human-readable text summary"""
        f.write(f"=== Valheim World Database Analysis ===\n\n")
        f.write(f"File: {result['file_info']['filename']}\n")
        f.write(f"Size: {result['file_info'].get('size_mb', 'Unknown')} MB\n")
        f.write(f"Parsed: {result['file_info']['parsed_at']}\n\n")
        
        f.write("=== Header Information ===\n")
        f.write(f"Magic Number: {result['header'].get('magic_number', 'Unknown')}\n")
        f.write(f"Magic Hex: {result['header'].get('magic_hex', 'Unknown')}\n\n")
        
        f.write("=== Data Analysis ===\n")
        patterns = result['analysis']['data_patterns']
        f.write(f"Null Bytes: {patterns['null_bytes']} ({patterns['null_percentage']}%)\n")
        f.write("Most Common Bytes:\n")
        for byte, count in patterns['common_bytes'].items():
            f.write(f"  {byte}: {count} times\n")
        f.write("\n")
        
        f.write("=== Extracted Strings ===\n")
        strings = result['strings']
        f.write(f"ASCII Strings Found: {len(strings['ascii_strings'])}\n")
        f.write("Sample Strings:\n")
        for i, string in enumerate(strings['ascii_strings'][:10]):
            f.write(f"  {i+1}. {string}\n")
        f.write("\n")
        
        f.write("=== Potential Names ===\n")
        for name in strings['potential_names'][:10]:
            f.write(f"  - {name}\n")
        f.write("\n")
        
        f.write("=== Data Sections ===\n")
        sections = result['sections']
        f.write(f"Large Zero Runs: {len(sections['zero_runs'])}\n")
        f.write(f"Data Regions: {len(sections['data_regions'])}\n")
        f.write("\n")
        
        f.write("=== Compression Analysis ===\n")
        compressed = result['compressed_sections']
        f.write(f"Zlib Signatures: {len(compressed['zlib_signatures'])}\n")
        f.write(f"High Entropy Sections: {len(compressed['potential_compressed'])}\n")

def main():
    parser = ValheimWorldDBParser(".")
    
    # Parse the specific database file
    db_filename = "DogeheimTesting.db"
    print(f"Parsing {db_filename}...")
    
    # Save as both JSON and text formats
    json_file = parser.save_readable_version(db_filename, "json")
    txt_file = parser.save_readable_version(db_filename, "txt")
    
    if json_file and txt_file:
        print(f"\nSuccessfully created readable versions:")
        print(f"  JSON: {json_file}")
        print(f"  Text: {txt_file}")

if __name__ == "__main__":
    main()
