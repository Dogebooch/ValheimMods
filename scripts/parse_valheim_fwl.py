#!/usr/bin/env python3
"""
Valheim World File Parser
Parses Valheim's .fwl world file format and converts to readable JSON
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

class ValheimFWLParser:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def parse_fwl_file(self, fwl_path: Path) -> Dict[str, Any]:
        """Parse Valheim world file (.fwl)"""
        print(f"Parsing Valheim world file: {fwl_path.name}")
        
        try:
            with open(fwl_path, 'rb') as f:
                data = f.read()
            
            world_data = {
                "file_info": {
                    "filename": fwl_path.name,
                    "size_bytes": len(data),
                    "size_mb": round(len(data) / (1024 * 1024), 2),
                    "parsed_at": datetime.now().isoformat()
                },
                "header": {},
                "world_info": {},
                "sections": {},
                "analysis": {}
            }
            
            # Parse header and world information
            world_data["header"] = self._parse_header(data)
            world_data["world_info"] = self._parse_world_info(data)
            
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
                    "filename": fwl_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def _parse_header(self, data: bytes) -> Dict[str, Any]:
        """Parse the header section of the .fwl file"""
        header = {}
        
        if len(data) >= 8:
            # First 4 bytes might be version or magic number
            header_value1 = struct.unpack('<I', data[:4])[0]
            header_value2 = struct.unpack('<I', data[4:8])[0]
            
            header["magic_number_1"] = header_value1
            header["magic_hex_1"] = f"0x{header_value1:08x}"
            header["magic_number_2"] = header_value2
            header["magic_hex_2"] = f"0x{header_value2:08x}"
        
        return header
    
    def _parse_world_info(self, data: bytes) -> Dict[str, Any]:
        """Parse world information from the .fwl file"""
        world_info = {}
        
        # Look for world name (usually appears early in the file)
        try:
            # Try to find the world name by looking for readable strings
            text = data.decode('utf-8', errors='ignore')
            lines = text.split('\n')
            
            # Look for potential world names (usually appear as standalone strings)
            for line in lines:
                line = line.strip()
                if len(line) > 3 and len(line) < 50 and line.isprintable():
                    # Check if it looks like a world name
                    if not any(char in line for char in ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x0b', '\x0c', '\x0e', '\x0f']):
                        world_info["potential_world_name"] = line
                        break
            
            # Also look for seed information
            for i in range(len(data) - 8):
                # Look for potential seed values (usually 4-byte integers)
                try:
                    seed_value = struct.unpack('<I', data[i:i+4])[0]
                    if 1000 <= seed_value <= 999999999:  # Reasonable seed range
                        world_info["potential_seed"] = seed_value
                        world_info["seed_offset"] = i
                        break
                except:
                    continue
                    
        except Exception as e:
            world_info["parse_error"] = str(e)
        
        return world_info
    
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
            
            # Find patterns that repeat more than 2 times
            repeating = [(p, c) for p, c in pattern_counts.items() if c > 2]
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
                if current_run > 10:  # Smaller threshold for .fwl files
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
                if i - start > 10:  # Smaller threshold for .fwl files
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
            "potential_names": [],
            "world_names": []
        }
        
        # Look for ASCII strings (printable characters)
        current_string = ""
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) > 2:  # Smaller minimum for .fwl files
                    strings["ascii_strings"].append(current_string)
                current_string = ""
        
        # Also try to decode as UTF-8
        try:
            text = data.decode('utf-8', errors='ignore')
            # Extract words that might be names
            words = text.split()
            potential_names = [word for word in words if len(word) > 2 and word.isalpha()]
            strings["potential_names"] = list(set(potential_names))[:20]  # Top 20 unique names
            
            # Look specifically for world names (usually appear as standalone strings)
            for word in potential_names:
                if len(word) > 3 and word.isalpha() and word[0].isupper():
                    strings["world_names"].append(word)
        except:
            pass
        
        # Remove duplicates and sort by length
        strings["ascii_strings"] = sorted(list(set(strings["ascii_strings"])), key=len, reverse=True)[:30]
        strings["world_names"] = list(set(strings["world_names"]))[:10]
        
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
        for i in range(0, len(data) - 512, 512):  # Smaller chunks for .fwl files
            chunk = data[i:i+512]
            if len(chunk) == 512:
                # Calculate entropy
                byte_counts = [0] * 256
                for byte in chunk:
                    byte_counts[byte] += 1
                
                entropy = 0
                for count in byte_counts:
                    if count > 0:
                        p = count / 512
                        entropy -= p * math.log2(p)  # Proper entropy calculation
                
                if entropy > 7.0:  # Lower threshold for .fwl files
                    compressed["potential_compressed"].append({
                        "offset": i,
                        "entropy": round(entropy, 2),
                        "sample": chunk[:20].hex()
                    })
        
        return compressed
    
    def parse_specific_fwl(self, fwl_filename: str) -> Dict[str, Any]:
        """Parse a specific .fwl file"""
        fwl_path = self.base_path / "Valheim_PlayerWorldData" / "worlds_local" / fwl_filename
        if not fwl_path.exists():
            return {"error": f"File {fwl_filename} not found"}
        
        return self.parse_fwl_file(fwl_path)
    
    def save_readable_version(self, fwl_filename: str, output_format: str = "json"):
        """Parse and save a readable version of the .fwl file"""
        result = self.parse_specific_fwl(fwl_filename)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return None
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = fwl_filename.replace('.fwl', '')
        
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
        f.write(f"=== Valheim World File Analysis ===\n\n")
        f.write(f"File: {result['file_info']['filename']}\n")
        f.write(f"Size: {result['file_info'].get('size_mb', 'Unknown')} MB\n")
        f.write(f"Parsed: {result['file_info']['parsed_at']}\n\n")
        
        f.write("=== Header Information ===\n")
        header = result['header']
        f.write(f"Magic Number 1: {header.get('magic_number_1', 'Unknown')}\n")
        f.write(f"Magic Hex 1: {header.get('magic_hex_1', 'Unknown')}\n")
        f.write(f"Magic Number 2: {header.get('magic_number_2', 'Unknown')}\n")
        f.write(f"Magic Hex 2: {header.get('magic_hex_2', 'Unknown')}\n\n")
        
        f.write("=== World Information ===\n")
        world_info = result['world_info']
        if 'potential_world_name' in world_info:
            f.write(f"World Name: {world_info['potential_world_name']}\n")
        if 'potential_seed' in world_info:
            f.write(f"World Seed: {world_info['potential_seed']}\n")
            f.write(f"Seed Offset: {world_info['seed_offset']}\n")
        f.write("\n")
        
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
        
        f.write("=== World Names ===\n")
        for name in strings['world_names']:
            f.write(f"  - {name}\n")
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
    parser = ValheimFWLParser(".")
    
    # Parse the specific .fwl file
    fwl_filename = "DogeheimTesting.fwl"
    print(f"Parsing {fwl_filename}...")
    
    # Save as both JSON and text formats
    json_file = parser.save_readable_version(fwl_filename, "json")
    txt_file = parser.save_readable_version(fwl_filename, "txt")
    
    if json_file and txt_file:
        print(f"\nSuccessfully created readable versions:")
        print(f"  JSON: {json_file}")
        print(f"  Text: {txt_file}")

if __name__ == "__main__":
    main()


