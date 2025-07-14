#!/usr/bin/env python3
"""
Valheim Modlist Builder - Main Entry Point
==========================================

A comprehensive application for building and managing Valheim modlists
with AI-enhanced analysis and automatic categorization.

Features:
- Mod categorization and management
- Zip file analysis and auto-categorization
- AI-enhanced summaries using local GPT4All
- Export functionality in multiple formats
- Beautiful earthy GUI theme

Author: Valheim Modlist Builder
Version: 1.0.0
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Add the current directory to Python path to import the main module
sys.path.insert(0, str(Path(__file__).parent))

try:
    from valheim_modlist_builder import ValheimModlistBuilder
except ImportError as e:
    print(f"Error importing ValheimModlistBuilder: {e}")
    print("Make sure valheim_modlist_builder.py is in the same directory.")
    sys.exit(1)

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['requests', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall them with:")
        print(f"  pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_gpt4all_availability():
    """Check if local GPT4All server is available."""
    try:
        import requests
        response = requests.get("http://localhost:4891/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ Local GPT4All server is available")
            return True
        else:
            print("⚠️  Local GPT4All server is not responding")
            print("   Status code:", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  Local GPT4All server is not running")
        print("   To start the server:")
        print("   1. Open GPT4All application")
        print("   2. Go to Settings > API Server")
        print("   3. Enable 'Start API Server'")
        print("   4. Set port to 4891")
        print("   5. Click 'Start Server'")
        return False
    except Exception as e:
        print("⚠️  Local GPT4All server is not available")
        print(f"   Error: {e}")
        print("   Make sure your GPT4All server is running on http://localhost:4891")
        return False

def main():
    """Main entry point for the Valheim Modlist Builder."""
    print("=" * 60)
    print("Valheim Modlist Builder")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        sys.exit(1)
    print("✅ All dependencies are installed")
    print()
    
    # Check GPT4All availability
    print("Checking GPT4All server...")
    gpt4all_available = check_gpt4all_availability()
    print()
    
    # Create and run the application
    try:
        print("Starting Valheim Modlist Builder...")
        print("(Press Ctrl+C to exit)")
        print()
        
        # Create the main window
        root = tk.Tk()
        
        # Set application icon if available
        icon_path = Path(__file__).parent / "icon.ico"
        if icon_path.exists():
            try:
                root.iconbitmap(str(icon_path))
            except:
                pass  # Icon loading failed, continue without it
        
        # Create and run the application
        app = ValheimModlistBuilder(root)
        
        # Center the window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        print("✅ Application started successfully!")
        print(f"   GPT4All AI: {'Available' if gpt4all_available else 'Unavailable'}")
        print()
        
        # Start the main event loop
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("Please check the error message above and try again.")
        sys.exit(1)
    finally:
        print("\nValheim Modlist Builder closed.")

if __name__ == "__main__":
    main() 