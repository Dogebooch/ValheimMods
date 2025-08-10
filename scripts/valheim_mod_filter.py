import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import re

class ValheimModFilter:
    def __init__(self, root):
        self.root = root
        self.root.title("Valheim Mod Filter")
        self.root.geometry("1200x800")
        
        # Mod data - extracted from the summary document
        self.mods = [
            {
                "name": "Therzie-Wizardry",
                "tags": ["magic", "armor", "weapons", "monsters", "food", "building"],
                "description": "Comprehensive magic system with staffs, robes, magic enemies, and crafting stations.",
                "prefab_count": 150,
                "content_types": 6,
                "category": "Magic & Combat"
            },
            {
                "name": "Fantu-Sages_Vault",
                "tags": ["armor", "weapons", "magic"],
                "description": "High-tier armor and weapons with magical properties.",
                "prefab_count": 45,
                "content_types": 3,
                "category": "Armor & Equipment"
            },
            {
                "name": "Therzie-Armory",
                "tags": ["armor", "weapons"],
                "description": "Comprehensive armor and weapon sets.",
                "prefab_count": 80,
                "content_types": 2,
                "category": "Armor & Equipment"
            },
            {
                "name": "HugotheDwarf-Hugos_Armory",
                "tags": ["armor", "weapons"],
                "description": "Diverse armor and weapon collection.",
                "prefab_count": 60,
                "content_types": 2,
                "category": "Armor & Equipment"
            },
            {
                "name": "Shawesome-Shawesomes_Divine_Armaments",
                "tags": ["armor"],
                "description": "Divine-themed armor sets.",
                "prefab_count": 25,
                "content_types": 1,
                "category": "Armor & Equipment"
            },
            {
                "name": "Southsil-SouthsilArmor",
                "tags": ["armor"],
                "description": "Unique armor designs and sets.",
                "prefab_count": 30,
                "content_types": 1,
                "category": "Armor & Equipment"
            },
            {
                "name": "Therzie-Warfare",
                "tags": ["weapons"],
                "description": "Comprehensive weapon collection.",
                "prefab_count": 50,
                "content_types": 1,
                "category": "Combat"
            },
            {
                "name": "Therzie-WarfareFireAndIce",
                "tags": ["weapons"],
                "description": "Fire and ice themed weapons.",
                "prefab_count": 20,
                "content_types": 1,
                "category": "Combat"
            },
            {
                "name": "blacks7ar-MagicRevamp",
                "tags": ["magic", "monsters"],
                "description": "Magic system overhaul with magical creatures.",
                "prefab_count": 75,
                "content_types": 2,
                "category": "Magic & Combat"
            },
            {
                "name": "Soloredis-RtDMagic",
                "tags": ["magic"],
                "description": "Ritual-based magic system.",
                "prefab_count": 40,
                "content_types": 1,
                "category": "Magic & Combat"
            },
            {
                "name": "Therzie-Monstrum",
                "tags": ["monsters", "food", "building"],
                "description": "Monster variety with related food and building content.",
                "prefab_count": 90,
                "content_types": 3,
                "category": "Monsters & Creatures"
            },
            {
                "name": "Therzie-MonstrumDeepNorth",
                "tags": ["monsters"],
                "description": "Deep North themed monsters.",
                "prefab_count": 35,
                "content_types": 1,
                "category": "Monsters & Creatures"
            },
            {
                "name": "Horem-MushroomMonsters",
                "tags": ["monsters"],
                "description": "Mushroom-themed monster variants.",
                "prefab_count": 15,
                "content_types": 1,
                "category": "Monsters & Creatures"
            },
            {
                "name": "TaegukGaming-Biome_Lords_Quest",
                "tags": ["monsters"],
                "description": "Biome lords and quest content.",
                "prefab_count": 25,
                "content_types": 1,
                "category": "Monsters & Creatures"
            },
            {
                "name": "blacks7ar-CookingAdditions",
                "tags": ["food"],
                "description": "Enhanced cooking and food system.",
                "prefab_count": 45,
                "content_types": 1,
                "category": "Food & Farming"
            },
            {
                "name": "OdinPlus-PotionPlus",
                "tags": ["food"],
                "description": "Potion crafting and alchemy system.",
                "prefab_count": 30,
                "content_types": 1,
                "category": "Food & Farming"
            },
            {
                "name": "Smoothbrain-Cooking",
                "tags": ["food"],
                "description": "Expanded cooking recipes and mechanics.",
                "prefab_count": 35,
                "content_types": 1,
                "category": "Food & Farming"
            },
            {
                "name": "warpalicious Series",
                "tags": ["building", "monsters"],
                "description": "Building pieces with monster integration.",
                "prefab_count": 120,
                "content_types": 2,
                "category": "Building & Construction"
            },
            {
                "name": "OdinPlus-OdinArchitect",
                "tags": ["building"],
                "description": "Advanced building and architecture tools.",
                "prefab_count": 85,
                "content_types": 1,
                "category": "Building & Construction"
            },
            {
                "name": "blacks7ar-FineWoodBuildPieces",
                "tags": ["building"],
                "description": "Fine wood building pieces and structures.",
                "prefab_count": 55,
                "content_types": 1,
                "category": "Building & Construction"
            },
            {
                "name": "blacks7ar-FineWoodFurnitures",
                "tags": ["building"],
                "description": "Fine wood furniture and decorative items.",
                "prefab_count": 40,
                "content_types": 1,
                "category": "Building & Construction"
            },
            {
                "name": "JewelHeim-RelicHeim",
                "tags": ["loot", "monsters", "systems"],
                "description": "Relic system with monster encounters and progression.",
                "prefab_count": 65,
                "content_types": 3,
                "category": "Loot & Progression"
            }
        ]
        
        self.active_filters = set()
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔍 Valheim Mod Filter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Search frame
        search_frame = ttk.LabelFrame(main_frame, text="Search & Filter", padding="10")
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(0, weight=1)
        
        # Search box
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 10))
        search_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        search_entry.insert(0, "Search mods by name...")
        search_entry.bind('<FocusIn>', self.on_search_focus_in)
        search_entry.bind('<FocusOut>', self.on_search_focus_out)
        
        # Clear search button
        clear_search_btn = ttk.Button(search_frame, text="Clear Search", command=self.clear_search)
        clear_search_btn.grid(row=0, column=1)
        
        # Filter buttons frame
        filter_frame = ttk.Frame(search_frame)
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Filter buttons
        self.filter_buttons = {}
        filter_tags = [
            ("armor", "🛡️ ARMOR"),
            ("weapons", "⚔️ WEAPONS"),
            ("magic", "🧙‍♂️ MAGIC"),
            ("monsters", "🐉 MONSTERS"),
            ("food", "🍖 FOOD"),
            ("building", "🏰 BUILDING"),
            ("loot", "🎒 LOOT"),
            ("systems", "🎮 SYSTEMS")
        ]
        
        for i, (tag, label) in enumerate(filter_tags):
            btn = ttk.Button(filter_frame, text=label, command=lambda t=tag: self.toggle_filter(t))
            btn.grid(row=i//4, column=i%4, padx=5, pady=2, sticky=(tk.W, tk.E))
            self.filter_buttons[tag] = btn
        
        # Clear filters button
        clear_filters_btn = ttk.Button(filter_frame, text="❌ CLEAR ALL FILTERS", 
                                     command=self.clear_filters, style="Accent.TButton")
        clear_filters_btn.grid(row=len(filter_tags)//4 + 1, column=0, columnspan=4, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Mod Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=("Consolas", 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Initial display
        self.update_display()
        
    def on_search_focus_in(self, event):
        if self.search_var.get() == "Search mods by name...":
            self.search_var.set("")
            
    def on_search_focus_out(self, event):
        if self.search_var.get() == "":
            self.search_var.set("Search mods by name...")
            
    def on_search_change(self, *args):
        self.update_display()
        
    def clear_search(self):
        self.search_var.set("Search mods by name...")
        self.update_display()
        
    def toggle_filter(self, tag):
        if tag in self.active_filters:
            self.active_filters.remove(tag)
            self.filter_buttons[tag].state(['!pressed'])
        else:
            self.active_filters.add(tag)
            self.filter_buttons[tag].state(['pressed'])
        self.update_display()
        
    def clear_filters(self):
        self.active_filters.clear()
        for btn in self.filter_buttons.values():
            btn.state(['!pressed'])
        self.update_display()
        
    def get_tag_emoji(self, tag):
        emoji_map = {
            "armor": "🛡️",
            "weapons": "⚔️",
            "magic": "🧙‍♂️",
            "monsters": "🐉",
            "food": "🍖",
            "building": "🏰",
            "loot": "🎒",
            "systems": "🎮"
        }
        return emoji_map.get(tag, "📦")
        
    def filter_mods(self):
        filtered_mods = []
        search_term = self.search_var.get().lower()
        
        for mod in self.mods:
            # Check search term
            if search_term and search_term != "search mods by name...":
                if search_term not in mod["name"].lower() and search_term not in mod["description"].lower():
                    continue
                    
            # Check active filters
            if self.active_filters:
                if not any(tag in mod["tags"] for tag in self.active_filters):
                    continue
                    
            filtered_mods.append(mod)
            
        return filtered_mods
        
    def update_display(self):
        filtered_mods = self.filter_mods()
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        if not filtered_mods:
            self.results_text.insert(tk.END, "No mods found matching your criteria.\n\n")
            self.results_text.insert(tk.END, "Try:\n")
            self.results_text.insert(tk.END, "• Clearing some filters\n")
            self.results_text.insert(tk.END, "• Using different search terms\n")
            self.results_text.insert(tk.END, "• Checking the spelling of mod names\n")
            self.status_var.set("No results found")
            return
            
        # Display mods
        for i, mod in enumerate(filtered_mods, 1):
            # Mod header
            self.results_text.insert(tk.END, f"{i}. {mod['name']}\n", "mod_name")
            self.results_text.insert(tk.END, f"   Category: {mod['category']}\n")
            
            # Tags
            tag_text = "   Content: "
            for tag in mod["tags"]:
                emoji = self.get_tag_emoji(tag)
                tag_text += f"{emoji} {tag.upper()} "
            self.results_text.insert(tk.END, tag_text + "\n")
            
            # Stats
            self.results_text.insert(tk.END, f"   Prefabs: {mod['prefab_count']} | Content Types: {mod['content_types']}\n")
            
            # Description
            self.results_text.insert(tk.END, f"   Description: {mod['description']}\n")
            
            # Separator
            if i < len(filtered_mods):
                self.results_text.insert(tk.END, "\n" + "="*80 + "\n\n")
                
        # Update status
        self.status_var.set(f"Showing {len(filtered_mods)} of {len(self.mods)} mods")
        
        # Configure tags for styling
        self.results_text.tag_configure("mod_name", font=("Consolas", 10, "bold"))

def main():
    root = tk.Tk()
    app = ValheimModFilter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
