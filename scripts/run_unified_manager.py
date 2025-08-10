#!/usr/bin/env python3
"""
Launcher for Valheim Unified Mod Manager
"""

import os
import sys

# Add scripts directory to path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)

try:
    from valheim_unified_manager import main
    main()
except ImportError as e:
    print(f"Error importing unified manager: {e}")
    print("Make sure all required dependencies are installed:")
    print("pip install pillow pyyaml")
except Exception as e:
    print(f"Error running unified manager: {e}")
