#!/usr/bin/env python3
"""
Simple test script to verify GUI components work correctly.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

def test_basic_gui():
    """Test basic tkinter functionality."""
    print("Testing basic tkinter functionality...")
    
    root = tk.Tk()
    root.title("GUI Test")
    root.geometry("400x300")
    
    # Test basic widgets
    label = tk.Label(root, text="If you can see this, tkinter is working!")
    label.pack(pady=20)
    
    button = tk.Button(root, text="Click me!", command=lambda: messagebox.showinfo("Test", "Button works!"))
    button.pack(pady=10)
    
    # Test ttk widgets
    ttk_button = ttk.Button(root, text="TTK Button", command=lambda: messagebox.showinfo("Test", "TTK button works!"))
    ttk_button.pack(pady=10)
    
    # Test combobox
    combo = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
    combo.pack(pady=10)
    combo.set("Option 1")
    
    # Test treeview
    tree = ttk.Treeview(root, columns=("col1", "col2"), show="headings")
    tree.heading("col1", text="Column 1")
    tree.heading("col2", text="Column 2")
    tree.insert("", "end", values=("Test 1", "Test 2"))
    tree.pack(pady=10, fill=tk.BOTH, expand=True)
    
    # Close button
    close_btn = tk.Button(root, text="Close", command=root.quit)
    close_btn.pack(pady=10)
    
    print("GUI test window should now be visible.")
    print("If you can see the window and interact with it, tkinter is working correctly.")
    
    root.mainloop()
    print("GUI test completed.")

def test_config_path():
    """Test config path detection."""
    print("Testing config path detection...")
    
    workspace = Path(__file__).resolve().parents[1]
    config_path = workspace / "config"
    
    print(f"Workspace: {workspace}")
    print(f"Config path: {config_path}")
    print(f"Config exists: {config_path.exists()}")
    
    if config_path.exists():
        print("Config directory found!")
        # List a few files
        files = list(config_path.glob("*.cfg"))[:5]
        print(f"Sample config files: {[f.name for f in files]}")
    else:
        print("Config directory not found!")

if __name__ == "__main__":
    print("Starting GUI test...")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    
    test_config_path()
    print()
    test_basic_gui()
