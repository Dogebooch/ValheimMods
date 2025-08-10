#!/usr/bin/env python3
"""
Launcher for the Centralized Mod Manager
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to the path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

try:
    from centralized_mod_manager import main
    main()
except ImportError as e:
    print(f"Error importing centralized_mod_manager: {e}")
    print("Make sure all required dependencies are installed:")
    print("pip install pyyaml pillow")
    sys.exit(1)
except Exception as e:
    print(f"Error running centralized mod manager: {e}")
    sys.exit(1)
