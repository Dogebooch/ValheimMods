#!/usr/bin/env python3
"""
Comprehensive Valheim Binary File Parser
Parses .db, .r2z, .fwl, texture cache, and WackyDatabase files
"""

import os
import json
import struct
import zlib
import sqlite3
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import binascii

class ValheimBinaryParser:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def parse_world_db(self, db_path: Path) -> Dict[str, Any]:
        """Parse Valheim world database files (.db)"""
        print(f"Parsing world database: {db_path.name}")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            world_data = {
                "file_info": {
                    "filename": db_path.name,
                    "size_mb": round(db_path.stat().st_size / (1024 * 1024), 2),
                    "parsed_at": datetime.now().isoformat()
                },
                "tables": {},
                "summary": {}
            }
            
            for table in tables:
                try:
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = [{"name": row[1], "type": row[2]} for row in cursor.fetchall()]
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    row_count = cursor.fetchone()[0]
                    
                    # Get sample data (first 10 rows)
                    cursor.execute(f"SELECT * FROM {table} LIMIT 10")
                    sample_data = []
                    for row in cursor.fetchall():
                        sample_data.append(list(row))
                    
                    world_data["tables"][table] = {
                        "columns": columns,
                        "row_count": row_count,
                        "sample_data": sample_data
                    }
                    
                    # Add to summary
                    world_data["summary"][table] = {
                        "columns": len(columns),
                        "rows": row_count
                    }
                    
                except Exception as e:
                    print(f"Error parsing table {table}: {e}")
                    world_data["tables"][table] = {"error": str(e)}
            
            conn.close()
            return world_data
            
        except Exception as e:
            return {
                "file_info": {
                    "filename": db_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def parse_r2z_file(self, r2z_path: Path) -> Dict[str, Any]:
        """Parse R2ModManager export files (.r2z)"""
        print(f"Parsing R2Z file: {r2z_path.name}")
        
        try:
            with open(r2z_path, 'rb') as f:
                # Read header
                header = f.read(4)
                if header != b'r2z\x00':
                    raise ValueError("Invalid R2Z file format")
                
                # Read version
                version = struct.unpack('<I', f.read(4))[0]
                
                # Read metadata size
                metadata_size = struct.unpack('<I', f.read(4))[0]
                
                # Read metadata
                metadata_compressed = f.read(metadata_size)
                metadata_json = zlib.decompress(metadata_compressed).decode('utf-8')
                metadata = json.loads(metadata_json)
                
                # Read file count
                file_count = struct.unpack('<I', f.read(4))[0]
                
                files_data = []
                for i in range(file_count):
                    # Read file entry
                    name_length = struct.unpack('<I', f.read(4))[0]
                    name = f.read(name_length).decode('utf-8')
                    
                    size = struct.unpack('<Q', f.read(8))[0]
                    compressed_size = struct.unpack('<I', f.read(4))[0]
                    
                    # Skip file data for now
                    f.seek(compressed_size, 1)
                    
                    files_data.append({
                        "name": name,
                        "size": size,
                        "compressed_size": compressed_size
                    })
                
                return {
                    "file_info": {
                        "filename": r2z_path.name,
                        "size_mb": round(r2z_path.stat().st_size / (1024 * 1024), 2),
                        "parsed_at": datetime.now().isoformat()
                    },
                    "r2z_info": {
                        "version": version,
                        "file_count": file_count
                    },
                    "metadata": metadata,
                    "files": files_data
                }
                
        except Exception as e:
            return {
                "file_info": {
                    "filename": r2z_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def parse_fwl_file(self, fwl_path: Path) -> Dict[str, Any]:
        """Parse Valheim world file headers (.fwl)"""
        print(f"Parsing FWL file: {fwl_path.name}")
        
        try:
            with open(fwl_path, 'rb') as f:
                # Read world name length
                name_length = struct.unpack('<I', f.read(4))[0]
                world_name = f.read(name_length).decode('utf-8')
                
                # Read world seed
                seed = struct.unpack('<I', f.read(4))[0]
                
                # Read world version
                version = struct.unpack('<I', f.read(4))[0]
                
                # Read world size
                world_size = struct.unpack('<I', f.read(4))[0]
                
                # Read world offset
                world_offset = struct.unpack('<I', f.read(4))[0]
                
                return {
                    "file_info": {
                        "filename": fwl_path.name,
                        "size_bytes": fwl_path.stat().st_size,
                        "parsed_at": datetime.now().isoformat()
                    },
                    "world_info": {
                        "name": world_name,
                        "seed": seed,
                        "version": version,
                        "size": world_size,
                        "offset": world_offset
                    }
                }
                
        except Exception as e:
            return {
                "file_info": {
                    "filename": fwl_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def parse_texture_cache(self, cache_path: Path) -> Dict[str, Any]:
        """Parse texture cache files"""
        print(f"Parsing texture cache: {cache_path.name}")
        
        try:
            with open(cache_path, 'rb') as f:
                # Read header
                header = f.read(4)
                
                # Try to read as text first
                f.seek(0)
                try:
                    content = f.read().decode('utf-8')
                    lines = content.split('\n')
                    
                    return {
                        "file_info": {
                            "filename": cache_path.name,
                            "size_mb": round(cache_path.stat().st_size / (1024 * 1024), 2),
                            "parsed_at": datetime.now().isoformat()
                        },
                        "cache_info": {
                            "type": "texture_cache",
                            "format": "text",
                            "line_count": len(lines)
                        },
                        "sample_lines": lines[:20] if len(lines) > 20 else lines
                    }
                except UnicodeDecodeError:
                    # Binary format
                    f.seek(0)
                    data = f.read()
                    
                    return {
                        "file_info": {
                            "filename": cache_path.name,
                            "size_mb": round(cache_path.stat().st_size / (1024 * 1024), 2),
                            "parsed_at": datetime.now().isoformat()
                        },
                        "cache_info": {
                            "type": "texture_cache",
                            "format": "binary",
                            "data_size": len(data)
                        },
                        "binary_info": {
                            "header_hex": binascii.hexlify(data[:16]).decode(),
                            "total_bytes": len(data)
                        }
                    }
                    
        except Exception as e:
            return {
                "file_info": {
                    "filename": cache_path.name,
                    "error": str(e),
                    "parsed_at": datetime.now().isoformat()
                }
            }
    
    def parse_wackydatabase_files(self, wdb_path: Path) -> Dict[str, Any]:
        """Parse WackyDatabase YAML files"""
        print(f"Parsing WackyDatabase files from: {wdb_path}")
        
        wdb_data = {
            "file_info": {
                "source_path": str(wdb_path),
                "parsed_at": datetime.now().isoformat()
            },
            "categories": {},
            "summary": {}
        }
        
        try:
            for category_dir in wdb_path.iterdir():
                if category_dir.is_dir():
                    category_name = category_dir.name
                    wdb_data["categories"][category_name] = {
                        "files": {},
                        "file_count": 0
                    }
                    
                    # Recursively find all YAML files
                    yaml_files = list(category_dir.rglob("*.yml")) + list(category_dir.rglob("*.yaml"))
                    
                    for yaml_file in yaml_files:
                        try:
                            with open(yaml_file, 'r', encoding='utf-8') as f:
                                content = yaml.safe_load(f)
                                
                            relative_path = str(yaml_file.relative_to(wdb_path))
                            wdb_data["categories"][category_name]["files"][relative_path] = {
                                "size_bytes": yaml_file.stat().st_size,
                                "content_type": type(content).__name__,
                                "sample_data": self._get_sample_data(content)
                            }
                            wdb_data["categories"][category_name]["file_count"] += 1
                            
                        except Exception as e:
                            relative_path = str(yaml_file.relative_to(wdb_path))
                            wdb_data["categories"][category_name]["files"][relative_path] = {
                                "error": str(e)
                            }
                    
                    # Add category summary
                    wdb_data["summary"][category_name] = {
                        "file_count": wdb_data["categories"][category_name]["file_count"],
                        "total_size_mb": round(sum(
                            f.get("size_bytes", 0) for f in wdb_data["categories"][category_name]["files"].values()
                        ) / (1024 * 1024), 2)
                    }
        
        except Exception as e:
            wdb_data["error"] = str(e)
        
        return wdb_data
    
    def _get_sample_data(self, data: Any, max_depth: int = 3, max_items: int = 5) -> Any:
        """Extract sample data from complex structures"""
        if max_depth <= 0:
            return f"[{type(data).__name__}] (max depth reached)"
        
        if isinstance(data, dict):
            sample = {}
            for i, (key, value) in enumerate(data.items()):
                if i >= max_items:
                    sample[f"... ({len(data) - max_items} more items)"] = None
                    break
                sample[key] = self._get_sample_data(value, max_depth - 1, max_items)
            return sample
        elif isinstance(data, list):
            sample = []
            for i, item in enumerate(data):
                if i >= max_items:
                    sample.append(f"... ({len(data) - max_items} more items)")
                    break
                sample.append(self._get_sample_data(item, max_depth - 1, max_items))
            return sample
        else:
            return data
    
    def parse_all_binaries(self):
        """Parse all identified binary files"""
        all_results = {
            "parse_info": {
                "parsed_at": datetime.now().isoformat(),
                "total_files_parsed": 0
            },
            "world_databases": {},
            "r2z_exports": {},
            "world_files": {},
            "texture_caches": {},
            "wackydatabase": {}
        }
        
        # Parse world database files
        worlds_dir = self.base_path / "Valheim_PlayerWorldData" / "worlds_local"
        if worlds_dir.exists():
            for db_file in worlds_dir.glob("*.db"):
                if not db_file.name.endswith('.old'):
                    result = self.parse_world_db(db_file)
                    all_results["world_databases"][db_file.name] = result
                    all_results["parse_info"]["total_files_parsed"] += 1
        
        # Parse R2Z export files
        exports_dir = self.base_path / "Valheim" / "exports"
        if exports_dir.exists():
            for r2z_file in exports_dir.glob("*.r2z"):
                result = self.parse_r2z_file(r2z_file)
                all_results["r2z_exports"][r2z_file.name] = result
                all_results["parse_info"]["total_files_parsed"] += 1
        
        # Parse world file headers
        if worlds_dir.exists():
            for fwl_file in worlds_dir.glob("*.fwl"):
                if not fwl_file.name.endswith('.old'):
                    result = self.parse_fwl_file(fwl_file)
                    all_results["world_files"][fwl_file.name] = result
                    all_results["parse_info"]["total_files_parsed"] += 1
        
        # Parse texture cache files
        if worlds_dir.exists():
            for cache_file in worlds_dir.glob("*TexCache"):
                result = self.parse_texture_cache(cache_file)
                all_results["texture_caches"][cache_file.name] = result
                all_results["parse_info"]["total_files_parsed"] += 1
        
        # Parse WackyDatabase files
        wdb_path = self.base_path / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config" / "wackysDatabase"
        if wdb_path.exists():
            result = self.parse_wackydatabase_files(wdb_path)
            all_results["wackydatabase"] = result
            all_results["parse_info"]["total_files_parsed"] += 1
        
        return all_results
    
    def save_results(self, results: Dict[str, Any]):
        """Save parsing results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save comprehensive analysis
        comprehensive_file = self.output_dir / f"comprehensive_binary_analysis_v2_{timestamp}.json"
        with open(comprehensive_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save summary
        summary_file = self.output_dir / f"binary_analysis_summary_v2_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=== Valheim Binary File Analysis v2 ===\n\n")
            f.write(f"Analysis Date: {results['parse_info']['parsed_at']}\n")
            f.write(f"Total Files Parsed: {results['parse_info']['total_files_parsed']}\n\n")
            
            f.write("=== File Categories ===\n")
            f.write(f"World Databases: {len(results['world_databases'])}\n")
            f.write(f"R2Z Exports: {len(results['r2z_exports'])}\n")
            f.write(f"World Files: {len(results['world_files'])}\n")
            f.write(f"Texture Caches: {len(results['texture_caches'])}\n")
            f.write(f"WackyDatabase: {'Yes' if results['wackydatabase'] else 'No'}\n\n")
            
            f.write("=== File Details ===\n")
            for category, files in results.items():
                if category != "parse_info" and category != "wackydatabase":
                    f.write(f"\n{category.upper()}:\n")
                    for filename, data in files.items():
                        if "file_info" in data:
                            size = data["file_info"].get("size_mb", "Unknown")
                            f.write(f"  - {filename}: {size} MB\n")
        
        print(f"Results saved to:")
        print(f"  - {comprehensive_file}")
        print(f"  - {summary_file}")
        
        return comprehensive_file, summary_file

def main():
    parser = ValheimBinaryParser(".")
    print("Starting comprehensive Valheim binary file analysis...")
    
    results = parser.parse_all_binaries()
    comprehensive_file, summary_file = parser.save_results(results)
    
    print(f"\nAnalysis complete! Parsed {results['parse_info']['total_files_parsed']} files.")
    print(f"Results saved to {comprehensive_file} and {summary_file}")

if __name__ == "__main__":
    main() 