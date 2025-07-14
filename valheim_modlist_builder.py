import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import json
import zipfile
import os
import re
import requests
from pathlib import Path
from typing import Dict, List, Optional
import shutil
import time

class LMStudioIntegration:
    def __init__(self):
        self.base_url = "http://localhost:1234/v1"
        self.headers = {"Content-Type": "application/json"}
        # Model selection (updated for new optimal models)
        self.models = {
            'summary': 'google/gemma-3-12b',
            'recommendation': 'google/gemma-3-12b',
            'category': 'google/gemma-3-12b',
            'feature_search': 'google/gemma-3-12b',
            'config_suggestion': 'google/gemma-3-12b',
            'code_analysis': 'deepseek/deepseek-r1-0528-qwen3-8b',
            'code_generation': 'deepseek/deepseek-r1-0528-qwen3-8b',
            'picture': 'gemma-3-27b',
            'chat': 'google/gemma-3-12b',
            'fallback': 'google/gemma-3-12b',
        }
    
    def check_api_availability(self):
        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _call_model(self, model, system_prompt, user_prompt, max_tokens=1024, temperature=0.5):
        payload = {
            "model": model,
                    "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
                    ],
            "max_tokens": -1 if model == 'google/gemma-3-12b' else max_tokens,
            "temperature": 0.7 if model == 'google/gemma-3-12b' else temperature,
            "stream": False
        }
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_mod_summary(self, mod_name, mod_author, mod_description, file_analysis):
        model = self.models['summary']
        system_prompt = "You are a Valheim mod expert. Provide a concise, clear, and accurate summary in 1-3 sentences (max 50 words). Focus on the mod's main gameplay effect, unique features, and any major requirements."
        user_prompt = f"""
        Summarize this Valheim mod for a modlist builder. Be brief and to the point.
        Mod: {mod_name}
        Author: {mod_author}
        Description: {mod_description}
        [File Analysis]
        {file_analysis}
        """
        return self._call_model(model, system_prompt, user_prompt, max_tokens=120, temperature=0.45)

    def suggest_category(self, mod_name, mod_description, file_analysis):
        model = self.models['category']
        system_prompt = "You are a Valheim mod expert. Respond with only the category name."
        user_prompt = f"""
            Categorize this Valheim mod:
            Mod: {mod_name}
            Description: {mod_description}
        [File Analysis]
        {file_analysis}
            Categories:
            - Boss & Combat Overhaul: Bosses, combat, encounters
            - Loot Overhaul: Loot, items, drops
            - Magic & Classes: Magic, spells, classes
            - Skills & Progression: Skills, professions, leveling
            - Gear & Customization: Armor, weapons, cosmetics
            - Co-op Stability: Server, multiplayer, stability
        - Quality of Life: Inventory, UI, automation, building, navigation, and other improvements that reduce tedium.
        - Dependencies: Frameworks, libraries, or required base mods
            Respond with ONLY the category name.
            """
        return self._call_model(model, system_prompt, user_prompt, max_tokens=30, temperature=0.2).strip()
    
    def get_mod_recommendation(self, mod_name, mod_description, file_analysis):
        model = self.models['recommendation']
        system_prompt = "You are a Valheim modlist curator and compatibility expert. Provide actionable, concise, and accurate recommendations for modpack builders."
        user_prompt = f"""
        Evaluate this Valheim mod for inclusion in a 2-player co-op modlist. Focus on:
        - Should this mod be included or excluded? (Start with INCLUDE or EXCLUDE)
        - Key reasons for your recommendation (gameplay impact, balance, compatibility, uniqueness)
        - Any major conflicts, requirements, or dependencies
        - Unique features or value for a co-op experience
        - If EXCLUDE, suggest alternatives or explain why it doesn't fit
            Mod: {mod_name}
            Description: {mod_description}
        [File Analysis]
        {file_analysis}
        Respond with: INCLUDE or EXCLUDE + a brief, clear reason (max 100 words). Prioritize compatibility, gameplay value, and unique features.
        """
        return self._call_model(model, system_prompt, user_prompt, max_tokens=250, temperature=0.3).strip()

    def feature_search(self, feature, snippets, vision_prompt):
        model = self.models['feature_search']
        system_prompt = "You are a Valheim mod expert and feature search assistant."
        user_prompt = vision_prompt + f"\n\nFeature/Goal: {feature}\n\nRelevant config/instruction snippets from mods:\n" + "\n".join(snippets) + "\nIf you do not have enough information to make a recommendation, say so and request more information or tutorials."
        return self._call_model(model, system_prompt, user_prompt, max_tokens=400, temperature=0.5)

    def config_suggestion(self, mod_name, mod_version, config_snippets, vision_prompt):
        model = self.models['config_suggestion']
        system_prompt = "You are a Valheim mod configuration expert."
        user_prompt = vision_prompt + f"\n\nMod: {mod_name} v{mod_version}\nConfig/instruction snippets:\n" + "\n".join(config_snippets) + "\nRecommend configuration changes for this mod to best fit the vision. If you do not have enough information, say so and request more information or tutorials."
        return self._call_model(model, system_prompt, user_prompt, max_tokens=400, temperature=0.5)

    def code_analysis(self, code_snippet, task_description):
        model = self.models['code_analysis']
        system_prompt = "You are a code analysis expert for Valheim mods."
        user_prompt = f"Task: {task_description}\nCode:\n{code_snippet}"
        return self._call_model(model, system_prompt, user_prompt, max_tokens=400, temperature=0.5)

    def code_generation(self, task_description, context):
        model = self.models['code_generation']
        system_prompt = "You are a code generation assistant for Valheim mods."
        user_prompt = f"Task: {task_description}\nContext:\n{context}"
        return self._call_model(model, system_prompt, user_prompt, max_tokens=400, temperature=0.5)

    def chat(self, user_prompt, system_prompt_override=None):
        # Detect if the prompt contains code (triple backticks or common code keywords)
        import re
        code_detected = False
        code_snippet = None
        # Check for triple backticks
        code_blocks = re.findall(r'```[a-zA-Z]*\n([\s\S]*?)```', user_prompt)
        if code_blocks:
            code_detected = True
            code_snippet = '\n\n'.join(code_blocks)
        else:
            # Check for common code keywords
            code_keywords = [
                'def ', 'class ', 'public ', 'private ', 'using ', 'namespace ',
                'import ', 'void ', 'function ', 'return ', 'if(', 'for(',
                'while(', 'try:', 'except', 'catch(', 'System.', 'Console.'
            ]
            if any(kw in user_prompt for kw in code_keywords):
                code_detected = True
                code_snippet = user_prompt
        # If code detected, run through Deepseek first
        if code_detected and code_snippet:
            code_analysis = self.code_analysis(code_snippet, "Analyze this code for bugs, logic, and best practices. Summarize what it does and any issues.")
            user_prompt = f"[Code Analysis by Deepseek]:\n{code_analysis}\n\n[User Prompt]:\n{user_prompt}"
        model = self.models['chat']
        system_prompt = system_prompt_override or "You are a helpful, clear, and context-aware Valheim modding assistant. Provide practical advice, troubleshooting, and modlist building help."
        return self._call_model(model, system_prompt, user_prompt, max_tokens=-1, temperature=0.7)

class ValheimModlistBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Valheim Modlist Builder")
        self.root.geometry("1200x800")
        
        # Initialize LMStudio integration
        self.lmstudio = LMStudioIntegration()
        
        # Set modern olive green color scheme
        self.colors = {
            'bg': '#2F4F2F',  # Dark olive green background
            'fg': '#C9DAB4',  # Light olive green text
            'accent': '#8B4513',  # Saddle brown accent
            'light_bg': '#556B2F',  # Dark olive green
            'button_bg': '#A0522D',  # Sienna
            'button_fg': '#2F4F2F',  # Dark text on light olive buttons
            'entry_bg': '#C9DAB4',  # Light olive green entry background
            'entry_fg': '#2F4F2F',  # Dark olive text for light background
            'success': '#4CAF50',  # Green for success
            'warning': '#FF9800',  # Orange for warnings
            'error': '#F44336'  # Red for errors
        }
        
        self.root.configure(bg=self.colors['bg'])
        # Set global font for buttons to be larger
        self.root.option_add("*Button.Font", "Arial 12 bold")
        
        # Add notebook widget for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Data storage
        self.mods_data = {
            "boss_combat_overhaul": [],
            "loot_overhaul": [],
            "magic_classes": [],
            "skills_progression": [],
            "gear_customization": [],
            "coop_stability": [],
            "quality_of_life": [],
            "dependencies": [],
            "doesnt_fit": []
        }
        
        self.user_feedback = []
        self.feedback_file = "user_feedback.json"
        self.analyzed_mods_file = "analyzed_mods.json"
        self.analyzed_mods = []
        self.analyzed_mods_dir = "analyzed_mod_zips"
        if not os.path.exists(self.analyzed_mods_dir):
            os.makedirs(self.analyzed_mods_dir)
        self.load_feedback()
        self.load_analyzed_mods()
        self.setup_ui()
        self.load_data()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        self.create_add_mod_tab()
        self.create_mods_tab()
        self.create_export_tab()
        self.create_ai_config_tab()
        self.create_gameplay_changes_tab()
        self.create_conflicts_tab()

    def create_conflicts_tab(self):
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="Conflicts & Overlaps")
        tk.Label(tab, text="Detected Mod Conflicts & Overlaps (Master List Only)", bg=self.colors['bg'], fg=self.colors['error'], font=("Arial", 16, "bold")).pack(pady=(10, 5))
        self.conflicts_text = scrolledtext.ScrolledText(tab, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'], font=("Consolas", 10), wrap=tk.WORD)
        self.conflicts_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Button(tab, text="Rescan Conflicts", command=self.update_conflicts_report, bg=self.colors['accent'], fg=self.colors['button_fg'], relief=tk.FLAT, bd=0, padx=10, pady=5).pack(pady=5, fill=tk.X)
        self.update_conflicts_report()
        # Add Potential Conflicts button next to AI Recommendation tab
        self.add_potential_conflicts_button()

    def update_conflicts_report(self):
        # Only assess conflicts among mods in the master list
        master_mods = []
        for category, mods in self.mods_data.items():
            master_mods.extend(mods)
        asset_index = {}
        prefab_index = {}
        loc_index = {}
        config_index = {}
        patch_index = {}
        script_index = {}
        mod_name_map = {}
        for mod in master_mods:
            name = mod['name']
            mod_name_map[name] = mod
            # Assets/prefabs
            for f in mod.get('file_analysis', {}).get('prefab_files', []):
                asset_index.setdefault(f, []).append(name)
            # Localization
            for f in mod.get('file_analysis', {}).get('localization_files', []):
                loc_index.setdefault(f, []).append(name)
            # Configs
            for f in mod.get('file_analysis', {}).get('config_files', []):
                config_index.setdefault(f, []).append(name)
            # Patch/harmony
            for f in mod.get('file_analysis', {}).get('patch_files', []):
                patch_index.setdefault(f, []).append(name)
            # Scripts
            for f in mod.get('file_analysis', {}).get('script_files', []):
                script_index.setdefault(f, []).append(name)
        # Detect overlaps
        def find_conflicts(index, label):
            return [(k, v) for k, v in index.items() if len(v) > 1]
        asset_conflicts = find_conflicts(asset_index, "Asset/Prefab")
        loc_conflicts = find_conflicts(loc_index, "Localization")
        config_conflicts = find_conflicts(config_index, "Config")
        patch_conflicts = find_conflicts(patch_index, "Patch/Hook")
        script_conflicts = find_conflicts(script_index, "Script/Class")
        # Build report with improved formatting
        report = []
        def section(title, conflicts, suggestion=None):
            if conflicts:
                report.append(f"\n=== {title} Conflicts ===\n")
                for fname, mods in conflicts:
                    report.append(f"  - File: {fname}\n    Mods: {', '.join(mods)}\n")
                if suggestion:
                    report.append(f"    Suggestion: {suggestion}\n")
        section("Asset/Prefab", asset_conflicts, "Consider load order or disabling duplicate assets.")
        section("Localization", loc_conflicts, "Check for duplicate keys or merge localization files.")
        section("Config", config_conflicts, "Review config files for overlapping settings.")
        section("Patch/Hook", patch_conflicts, "Multiple mods patching the same method/class may cause instability. Review Harmony patches.")
        section("Script/Class", script_conflicts, "Multiple mods with the same script/class file may conflict.")
        if not report:
            report.append("No major conflicts or overlaps detected among master list mods!\n")
        self.conflicts_text.delete("1.0", tk.END)
        self.conflicts_text.insert(tk.END, "".join(report))
    
    def create_add_mod_tab(self):
        add_mod_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(add_mod_frame, text="Add Mod")
        
        # Title
        title_label = tk.Label(
            add_mod_frame,
            text="Add New Mod to Modlist",
            font=("Arial", 16, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title_label.pack(pady=(10, 20))
        
        # Main content frame
        content_frame = tk.Frame(add_mod_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Manual entry (smaller)
        left_panel = tk.Frame(content_frame, bg=self.colors['bg'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        left_panel.pack_propagate(False)  # Prevent the frame from shrinking
        
        # Manual entry section
        manual_frame = tk.LabelFrame(
            left_panel,
            text="Manual Entry",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        manual_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Mod name
        tk.Label(manual_frame, text="Mod Name:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.mod_name_entry = tk.Entry(manual_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        self.mod_name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Mod author
        tk.Label(manual_frame, text="Author:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.mod_author_entry = tk.Entry(manual_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        self.mod_author_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Mod description
        tk.Label(manual_frame, text="Description:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.mod_desc_text = scrolledtext.ScrolledText(
            manual_frame,
            height=4,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg']
        )
        self.mod_desc_text.pack(fill=tk.X, pady=(0, 10))
        
        # Category selection
        tk.Label(manual_frame, text="Category:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.category_var = tk.StringVar(value="boss_combat_overhaul")
        categories = [
            ("Boss & Combat Overhaul", "boss_combat_overhaul"),
            ("Loot Overhaul", "loot_overhaul"),
            ("Magic & Classes", "magic_classes"),
            ("Skills & Progression", "skills_progression"),
            ("Gear & Customization", "gear_customization"),
            ("Co-op Stability", "coop_stability"),
            ("Quality of Life", "quality_of_life"),
            ("Dependencies", "dependencies"),
            ("Doesn't Fit", "doesnt_fit")
        ]
        
        for text, value in categories:
            tk.Radiobutton(
                manual_frame,
                text=text,
                variable=self.category_var,
                value=value,
                bg=self.colors['bg'],
                fg=self.colors['fg'],
                selectcolor=self.colors['accent']
            ).pack(anchor=tk.W)
        
        # Add button
        add_button = tk.Button(
            manual_frame,
            text="Add Mod",
            command=self.add_mod,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=5
        )
        add_button.pack(pady=10, fill=tk.X)
        
        # Right panel - File upload and analysis (larger)
        right_panel = tk.Frame(content_frame, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # File upload section
        upload_frame = tk.LabelFrame(
            right_panel,
            text="Upload & Analyze",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        upload_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        file_frame = tk.Frame(upload_frame, bg=self.colors['bg'])
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(
            file_frame,
            textvariable=self.file_path_var,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            state='readonly'
        )
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = tk.Button(
            file_frame,
            text="Browse",
            command=self.browse_file,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=10
        )
        browse_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Analysis buttons frame
        buttons_frame = tk.Frame(upload_frame, bg=self.colors['bg'])
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Analyze button
        analyze_button = tk.Button(
            buttons_frame,
            text="Analyze Mod",
            command=self.analyze_mod,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5
        )
        analyze_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Auto-add button
        auto_add_button = tk.Button(
            buttons_frame,
            text="Auto-Add",
            command=self.auto_add_mod,
            bg=self.colors['success'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5
        )
        auto_add_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # AI Analysis buttons frame
        ai_buttons_frame = tk.Frame(upload_frame, bg=self.colors['bg'])
        ai_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # AI Status indicator
        self.ai_status_label = tk.Label(
            ai_buttons_frame,
            text="AI: Checking...",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 9)
        )
        self.ai_status_label.pack(side=tk.TOP, pady=(0, 5))
        
        # AI Summary button
        ai_summary_button = tk.Button(
            ai_buttons_frame,
            text="AI Summary",
            command=self.generate_ai_summary,
            bg=self.colors['accent'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3
        )
        ai_summary_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # AI Category button
        ai_category_button = tk.Button(
            ai_buttons_frame,
            text="AI Category",
            command=self.get_ai_category_suggestion,
            bg=self.colors['accent'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3
        )
        ai_category_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # AI Recommendation button
        ai_recommendation_button = tk.Button(
            ai_buttons_frame,
            text="AI Recommend",
            command=self.get_ai_mod_recommendation,
            bg=self.colors['accent'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3
        )
        ai_recommendation_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Analysis results
        results_frame = tk.LabelFrame(
            right_panel,
            text="Analysis Results",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.analysis_text = scrolledtext.ScrolledText(
            results_frame,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Check AI availability
        self.check_ai_status()
    
    def create_mods_tab(self):
        mods_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(mods_frame, text="Master Modlist")
        
        # Title
        title_label = tk.Label(
            mods_frame,
            text="Master Modlist",
            font=("Arial", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title_label.pack(pady=(10, 20))
        
        # Main content frame
        content_frame = tk.Frame(mods_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Filters and search
        left_panel = tk.Frame(content_frame, bg=self.colors['bg'], width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)  # Prevent the frame from shrinking
        
        # Filters frame
        filters_frame = tk.LabelFrame(
            left_panel,
            text="Filters & Search",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search by name
        tk.Label(filters_frame, text="Search by Name:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W, pady=(10, 5))
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            filters_frame,
            textvariable=self.search_var,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg']
        )
        search_entry.pack(fill=tk.X, padx=5, pady=(0, 10))
        search_entry.bind('<KeyRelease>', self.filter_mods)
        
        # Filter by category
        tk.Label(filters_frame, text="Filter by Category:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W, pady=(10, 5))
        self.filter_category_var = tk.StringVar(value="All Categories")
        categories = ["All Categories"] + [
            "Boss & Combat Overhaul",
            "Loot Overhaul",
            "Magic & Classes",
            "Skills & Progression",
            "Gear & Customization",
            "Co-op Stability",
            "Quality of Life",
            "Dependencies",
            "Doesn't Fit"
        ]
        
        filter_category_combo = ttk.Combobox(
            filters_frame,
            textvariable=self.filter_category_var,
            values=categories,
            state="readonly"
        )
        filter_category_combo.pack(fill=tk.X, padx=5, pady=(0, 10))
        filter_category_combo.bind('<<ComboboxSelected>>', self.filter_mods)
        
        # Filter by author
        tk.Label(filters_frame, text="Filter by Author:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W, pady=(10, 5))
        self.filter_author_var = tk.StringVar(value="All Authors")
        self.author_combo = ttk.Combobox(
            filters_frame,
            textvariable=self.filter_author_var,
            state="readonly"
        )
        self.author_combo.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.author_combo.bind('<<ComboboxSelected>>', self.filter_mods)
        
        # Sort options
        tk.Label(filters_frame, text="Sort by:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W, pady=(10, 5))
        self.sort_var = tk.StringVar(value="Name")
        sort_options = ["Name", "Author", "Category", "Gameplay Change", "Date Added"]
        
        for option in sort_options:
            tk.Radiobutton(
                filters_frame,
                text=option,
                variable=self.sort_var,
                value=option,
                bg=self.colors['bg'],
                fg=self.colors['fg'],
                selectcolor=self.colors['accent']
            ).pack(anchor=tk.W, padx=20)
        
        # Clear filters button
        clear_button = tk.Button(
            filters_frame,
            text="Clear Filters",
            command=self.clear_filters,
            bg=self.colors['warning'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5
        )
        clear_button.pack(pady=10, padx=5, fill=tk.X)
        
        # Stats frame
        stats_frame = tk.LabelFrame(
            left_panel,
            text="Statistics",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Total Mods: 0",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 10)
        )
        self.stats_label.pack(pady=10)
        
        # Center panel - Mods list
        center_panel = tk.Frame(content_frame, bg=self.colors['bg'])
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Mods list frame
        mods_list_frame = tk.LabelFrame(
            center_panel,
            text="Mods List",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        mods_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for mods
        columns = ('Name', 'Author', 'Category', 'Description')
        self.mods_tree = ttk.Treeview(mods_list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.mods_tree.heading('Name', text='Mod Name')
        self.mods_tree.heading('Author', text='Author')
        self.mods_tree.heading('Category', text='Category')
        self.mods_tree.heading('Description', text='Description')
        
        # Define column widths
        self.mods_tree.column('Name', width=200)
        self.mods_tree.column('Author', width=150)
        self.mods_tree.column('Category', width=150)
        self.mods_tree.column('Description', width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(mods_list_frame, orient=tk.VERTICAL, command=self.mods_tree.yview)
        self.mods_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.mods_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Actions
        right_panel = tk.Frame(content_frame, bg=self.colors['bg'], width=200)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)  # Prevent the frame from shrinking
        
        # Actions frame
        actions_frame = tk.LabelFrame(
            right_panel,
            text="Actions",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        actions_frame.pack(fill=tk.X)
        
        # Delete button
        delete_button = tk.Button(
            actions_frame,
            text="Delete Selected",
            command=self.delete_selected_mod,
            bg=self.colors['error'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8
        )
        delete_button.pack(pady=10, padx=10, fill=tk.X)
        
        # Edit button
        edit_button = tk.Button(
            actions_frame,
            text="Edit Mod",
            command=self.edit_selected_mod,
            bg=self.colors['accent'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8
        )
        edit_button.pack(pady=5, padx=10, fill=tk.X)
        
        # Export button
        export_button = tk.Button(
            actions_frame,
            text="Export Modlist",
            command=self.export_modlist,
            bg=self.colors['success'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8
        )
        export_button.pack(pady=5, padx=10, fill=tk.X)
        
        # Initialize the mods list
        self.update_master_modlist()
        
        # Add analyzed mods panel
        analyzed_panel = tk.Frame(content_frame, bg=self.colors['bg'], width=250)
        analyzed_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        analyzed_panel.pack_propagate(False)
        analyzed_label = tk.Label(analyzed_panel, text="Analyzed Mods (Not in Master List)", font=("Arial", 12, "bold"), bg=self.colors['bg'], fg="#888")
        analyzed_label.pack(pady=(10, 5))
        self.analyzed_listbox = tk.Listbox(analyzed_panel, bg="#333", fg="#888", selectbackground="#666", selectforeground="#C9DAB4", font=("Consolas", 10))
        self.analyzed_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.analyzed_listbox.bind('<Double-Button-1>', self.add_analyzed_mod_to_master)
        self.update_analyzed_mods_listbox()
    
    def filter_mods(self, event=None):
        """Filter mods based on search criteria"""
        self.update_master_modlist()
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_var.set("")
        self.filter_category_var.set("All Categories")
        self.filter_author_var.set("All Authors")
        self.sort_var.set("Name")
        self.update_master_modlist()
    
    def update_master_modlist(self):
        """Update the master modlist with current filters"""
        # Clear analyzed_mods list to only keep master mods relevant for conflict analysis
        self.analyzed_mods = []
        # Clear existing items
        for item in self.mods_tree.get_children():
            self.mods_tree.delete(item)
        
        # Get all mods
        all_mods = []
        for category, mods in self.mods_data.items():
            for mod in mods:
                category_name = category.replace('_', ' ').title()
                all_mods.append({
                    'name': mod['name'],
                    'author': mod['author'],
                    'category': category_name,
                    'description': mod['description'],
                    'category_key': category
                })
        
        # Apply filters
        filtered_mods = all_mods
        
        # Search filter
        search_term = self.search_var.get().lower()
        if search_term:
            filtered_mods = [mod for mod in filtered_mods if search_term in mod['name'].lower()]
        
        # Category filter
        category_filter = self.filter_category_var.get()
        if category_filter != "All Categories":
            filtered_mods = [mod for mod in filtered_mods if mod['category'] == category_filter]
        
        # Author filter
        author_filter = self.filter_author_var.get()
        if author_filter != "All Authors":
            filtered_mods = [mod for mod in filtered_mods if mod['author'] == author_filter]
        
        # Sort mods
        sort_by = self.sort_var.get()
        if sort_by == "Name":
            filtered_mods.sort(key=lambda x: x['name'])
        elif sort_by == "Author":
            filtered_mods.sort(key=lambda x: x['author'])
        elif sort_by == "Category":
            filtered_mods.sort(key=lambda x: x['category'])
        elif sort_by == "Gameplay Change":
            category_order = {
                "boss_combat_overhaul": 1,
                "loot_overhaul": 2,
                "magic_classes": 3,
                "skills_progression": 4,
                "gear_customization": 5,
                "coop_stability": 6,
                "quality_of_life": 7,
                "doesnt_fit": 8
            }
            filtered_mods.sort(key=lambda x: category_order.get(x['category_key'], 99))
        
        # Update author combo
        authors = list(set([mod['author'] for mod in all_mods]))
        authors.sort()
        self.author_combo['values'] = ["All Authors"] + authors
        
        # Add to treeview
        for mod in filtered_mods:
            self.mods_tree.insert('', 'end', values=(
                mod['name'],
                mod['author'],
                mod['category'],
                mod['description'][:100] + "..." if len(mod['description']) > 100 else mod['description']
            ))
        
        # Update stats
        total_mods = len(all_mods)
        filtered_count = len(filtered_mods)
        self.stats_label.config(text=f"Total Mods: {total_mods}\nFiltered: {filtered_count}")
    
    def edit_selected_mod(self):
        """Edit the selected mod"""
        selected_item = self.mods_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a mod to edit")
            return
        
        # Get selected mod info
        item = self.mods_tree.item(selected_item[0])
        mod_name = item['values'][0]
        mod_author = item['values'][1]
        mod_category = item['values'][2]
        
        # Find the mod in data
        for category, mods in self.mods_data.items():
            for mod in mods:
                if mod['name'] == mod_name and mod['author'] == mod_author:
                    # Create edit dialog
                    self.create_edit_dialog(mod, category)
                    return
        
        messagebox.showerror("Error", "Mod not found")
    
    def create_edit_dialog(self, mod, category):
        """Create dialog to edit mod"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Mod")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        tk.Label(dialog, text="Edit Mod", font=("Arial", 16, "bold"), 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(dialog, bg=self.colors['bg'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Name
        tk.Label(form_frame, text="Mod Name:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        name_entry = tk.Entry(form_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        name_entry.insert(0, mod['name'])
        name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Author
        tk.Label(form_frame, text="Author:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        author_entry = tk.Entry(form_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        author_entry.insert(0, mod['author'])
        author_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Description
        tk.Label(form_frame, text="Description:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        desc_text = scrolledtext.ScrolledText(form_frame, height=4, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        desc_text.insert("1.0", mod['description'])
        desc_text.pack(fill=tk.X, pady=(0, 10))
        
        # Category
        tk.Label(form_frame, text="Category:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        category_var = tk.StringVar(value=category.replace('_', ' ').title())
        categories = [
            ("Boss & Combat Overhaul", "boss_combat_overhaul"),
            ("Loot Overhaul", "loot_overhaul"),
            ("Magic & Classes", "magic_classes"),
            ("Skills & Progression", "skills_progression"),
            ("Gear & Customization", "gear_customization"),
            ("Co-op Stability", "coop_stability"),
            ("Quality of Life", "quality_of_life"),
            ("Dependencies", "dependencies"),
            ("Doesn't Fit", "doesnt_fit")
        ]
        
        for text, value in categories:
            tk.Radiobutton(form_frame, text=text, variable=category_var, value=value,
                          bg=self.colors['bg'], fg=self.colors['fg'], selectcolor=self.colors['accent']).pack(anchor=tk.W)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        def save_changes():
            # Remove from old category
            self.mods_data[category].remove(mod)
            
            # Add to new category
            new_category = category_var.get()
            new_mod = {
                'name': name_entry.get(),
                'author': author_entry.get(),
                'description': desc_text.get("1.0", tk.END).strip(),
                'category': new_category
            }
            self.mods_data[new_category].append(new_mod)
            
            self.save_data()
            self.update_master_modlist()
            dialog.destroy()
            messagebox.showinfo("Success", "Mod updated successfully")
        
        def cancel():
            dialog.destroy()
        
        tk.Button(button_frame, text="Save", command=save_changes,
                 bg=self.colors['success'], fg=self.colors['button_fg'],
                 relief=tk.FLAT, bd=0, padx=20, pady=5).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tk.Button(button_frame, text="Cancel", command=cancel,
                 bg=self.colors['error'], fg=self.colors['button_fg'],
                 relief=tk.FLAT, bd=0, padx=20, pady=5).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    # Removed create_upload_tab method - functionality moved to create_add_mod_tab
    
    def create_export_tab(self):
        export_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(export_frame, text="Export Modlist")
        
        # Title
        title_label = tk.Label(
            export_frame,
            text="Export Your Modlist",
            font=("Arial", 16, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title_label.pack(pady=(10, 20))
        
        # Main content frame
        content_frame = tk.Frame(export_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Export options
        left_panel = tk.Frame(content_frame, bg=self.colors['bg'])
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Export options
        options_frame = tk.LabelFrame(
            left_panel,
            text="Export Options",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        options_frame.pack(fill=tk.X)
        
        # Export format
        tk.Label(options_frame, text="Export Format:", bg=self.colors['bg'], fg=self.colors['fg'], font=("Arial", 11)).pack(anchor=tk.W, pady=(10, 5))
        self.export_format_var = tk.StringVar(value="json")
        formats = [("JSON", "json"), ("TXT", "txt"), ("CSV", "csv")]
        
        for text, value in formats:
            tk.Radiobutton(
                options_frame,
                text=text,
                variable=self.export_format_var,
                value=value,
                bg=self.colors['bg'],
                fg=self.colors['fg'],
                selectcolor=self.colors['accent']
            ).pack(anchor=tk.W, padx=20)
        
        # Export button
        export_button = tk.Button(
            options_frame,
            text="Export Modlist",
            command=self.export_modlist,
            bg=self.colors['success'],
            fg=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10
        )
        export_button.pack(pady=20, padx=10, fill=tk.X)
        
        # Right panel - Preview
        right_panel = tk.Frame(content_frame, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Preview
        preview_frame = tk.LabelFrame(
            right_panel,
            text="Export Preview",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Arial", 12, "bold")
        )
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            font=("Consolas", 10)
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.update_preview()
    
    def add_mod(self):
        name = self.mod_name_entry.get().strip()
        author = self.mod_author_entry.get().strip()
        description = self.mod_desc_text.get("1.0", tk.END).strip()
        category = self.category_var.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter a mod name")
            return
        
        mod_data = {
            "name": name,
            "author": author,
            "description": description,
            "category": category,
            "file_analysis": {
                "file_names": [],
                "manifest_json": {"name": name, "author": author, "description": description},
                "content_types": {}
            }
        }
        
        self.mods_data[category].append(mod_data)
        self.save_data()
        self.update_master_modlist()
        self.update_preview()
        
        # Clear form
        self.mod_name_entry.delete(0, tk.END)
        self.mod_author_entry.delete(0, tk.END)
        self.mod_desc_text.delete("1.0", tk.END)
        
        messagebox.showinfo("Success", f"Added {name} to {category.replace('_', ' ').title()}")
    

    
    def delete_selected_mod(self):
        """Delete the selected mod from the treeview"""
        selected_item = self.mods_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a mod to delete")
            return
        
        # Get selected mod info
        item = self.mods_tree.item(selected_item[0])
        mod_name = item['values'][0]
        mod_author = item['values'][1]
        mod_category = item['values'][2]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{mod_name}'?"):
            return
        
        # Find and remove the mod from data
        category_mapping = {
            "Boss & Combat Overhaul": "boss_combat_overhaul",
            "Loot Overhaul": "loot_overhaul",
            "Magic & Classes": "magic_classes",
            "Skills & Progression": "skills_progression",
            "Gear & Customization": "gear_customization",
            "Co-op Stability": "coop_stability",
            "Quality of Life": "quality_of_life",
            "Dependencies": "dependencies",
            "Doesn't Fit": "doesnt_fit"
        }
        
        category_key = category_mapping.get(mod_category, "doesnt_fit")
        
        # Find and remove the mod
        for mod in self.mods_data[category_key]:
            if mod['name'] == mod_name and mod['author'] == mod_author:
                self.mods_data[category_key].remove(mod)
                self.save_data()
                self.update_master_modlist()
                self.update_preview()
                messagebox.showinfo("Success", f"Deleted {mod_name}")
                return
        
        messagebox.showerror("Error", "Mod not found")
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Mod Zip File",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def analyze_mod(self):
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first")
            return
        
        try:
            analysis = self.analyze_zip_file(file_path)
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, analysis)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze file: {str(e)}")
    
    def auto_add_mod(self):
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first")
            return
        
        if not hasattr(self, 'current_analysis'):
            messagebox.showerror("Error", "Please analyze the mod first")
            return
        
        try:
            # Get mod information from analysis
            manifest_json = self.current_analysis.get('manifest_json', {})
            file_names = self.current_analysis.get('file_names', [])
            
            mod_name = manifest_json.get('name', os.path.basename(file_path).replace('.zip', ''))
            mod_author = manifest_json.get('author', 'Unknown')
            mod_description = manifest_json.get('description', 'No description available')
            
            # Generate detailed file analysis for AI
            file_analysis = self.generate_detailed_file_analysis(file_names)
            if hasattr(self, 'current_analysis') and 'file_path' in self.current_analysis:
                try:
                    with zipfile.ZipFile(self.current_analysis['file_path'], 'r') as zip_file:
                        content_info = self.extract_file_content_info(file_names, zip_file)
                        file_analysis += content_info
                except:
                    pass

            # Use AI to get category suggestion
            ai_category = self.lmstudio.suggest_category(mod_name, mod_description, file_analysis)

            # Map AI category string to internal key
            category_map = {
                "Boss & Combat Overhaul": "boss_combat_overhaul",
                "Loot Overhaul": "loot_overhaul",
                "Magic & Classes": "magic_classes",
                "Skills & Progression": "skills_progression",
                "Gear & Customization": "gear_customization",
                "Co-op Stability": "coop_stability",
                "Quality of Life": "quality_of_life",
                "Dependencies": "dependencies",
                "Doesn't Fit": "doesnt_fit",
                "Doesnt Fit": "doesnt_fit"
            }
            category = category_map.get(ai_category.strip(), "doesnt_fit")

            # Show the AI's category suggestion in the analysis box
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, f"AI Suggested Category: {ai_category}\n\n")
            self.analysis_text.insert(tk.END, f"Filing mod under: {category.replace('_', ' ').title()}\n\n")
            self.root.update()
            
            # Create mod data
            mod_data = {
                "name": mod_name,
                "author": mod_author,
                "description": mod_description,
                "category": category,
                "file_path": file_path,
                "file_analysis": self.current_analysis  # Store file analysis for overlap detection
            }
            
            # Add to appropriate category
            self.mods_data[category].append(mod_data)
            self.save_data()
            self.update_master_modlist()
            self.update_preview()
            
            messagebox.showinfo("Success", f"Added {mod_name} to {category.replace('_', ' ').title()}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to auto-add mod: {str(e)}")
    
    def auto_categorize_mod(self, file_names, mod_name, description):
        """
        Automatically categorize mods based on their content and description.
        """
        # Convert everything to lowercase for easier matching
        mod_name_lower = mod_name.lower()
        description_lower = description.lower()
        file_names_lower = [f.lower() for f in file_names]
        
        # Initialize category scores
        category_scores = {
            "boss_combat_overhaul": 0,
            "loot_overhaul": 0,
            "magic_classes": 0,
            "skills_progression": 0,
            "gear_customization": 0,
            "coop_stability": 0,
            "quality_of_life": 0,
            "dependencies": 0
        }
        
        # Boss & Combat Overhaul keywords
        boss_keywords = [
            'boss', 'encounter', 'roaming', 'repeatable', 'affix', 'affixes',
            'difficulty', 'scaling', 'monster', 'creature', 'enemy', 'spawn',
            'world', 'event', 'raid', 'invasion', 'attack', 'aggressive',
            'combat', 'battle', 'fight', 'harder', 'numerous', 'cllc'
        ]
        
        # Loot Overhaul keywords
        loot_keywords = [
            'loot', 'drop', 'rarity', 'rare', 'epic', 'legendary', 'chest',
            'material', 'item', 'customization', 'gem', 'weapon', 'enhanced',
            'table', 'random', 'randomized', 'reward', 'risk', 'epic loot',
            'drop chance', 'special effect', 'rarities'
        ]
        
        # Magic & Classes keywords
        magic_keywords = [
            'magic', 'spell', 'class', 'ability', 'runic', 'skyheim',
            'legend', 'power', 'magical', 'enchantment', 'sorcery',
            'wizard', 'mage', 'caster', 'spellbook', 'mana', 'magical gear',
            'visual', 'overhaul', 'unique power'
        ]
        
        # Skills & Progression keywords
        skills_keywords = [
            'skill', 'progression', 'level', 'experience', 'xp', 'profession',
            'farming', 'attribute', 'build', 'diversity', 'specialization',
            'runescape', 'non-combat', 'enrich', 'leveling', 'crafting',
            'gathering', 'mining', 'woodcutting', 'fishing', 'cooking'
        ]
        
        # Gear & Customization keywords
        gear_keywords = [
            'gear', 'armor', 'weapon', 'set', 'cosmetic', 'appearance',
            'customization', 'vanity', 'transmog', 'southsil', 'sage',
            'vault', 'pet', 'tameable', 'visual', 'appearance', 'outfit',
            'equipment', 'fashion', 'style', 'look'
        ]
        
        # Co-op Stability keywords
        coop_keywords = [
            'server', 'multiplayer', 'coop', 'co-op', 'stability', 'dedicated',
            'anti-cheat', 'anti-cheese', 'save', 'performance', 'sync',
            'network', 'connection', 'lag', 'desync', 'server-side'
        ]
        
        # Quality of Life keywords
        qol_keywords = [
            'inventory', 'management', 'stack', 'sort', 'organize', 'auto-sort',
            'quick-stack', 'crafting', 'station', 'workbench', 'forge', 'upgrade',
            'repair', 'durability', 'weight', 'capacity', 'storage', 'chest',
            'container', 'transfer', 'move', 'shift-click', 'drag', 'drop',
            'hotkey', 'shortcut', 'keybind', 'ui', 'interface', 'hud', 'minimap',
            'map', 'marker', 'waypoint', 'teleport', 'fast-travel', 'portal',
            'building', 'snap', 'grid', 'alignment', 'preview', 'blueprint',
            'copy', 'paste', 'undo', 'redo', 'rotation', 'mirror', 'flip',
            'health', 'stamina', 'food', 'buff', 'debuff', 'status', 'effect',
            'timer', 'cooldown', 'notification', 'alert', 'warning', 'info',
            'tooltip', 'help', 'guide', 'tutorial', 'wiki', 'reference',
            'quality', 'life', 'qol', 'convenience', 'ease', 'simplify',
            'automate', 'auto', 'smart', 'intelligent', 'helper', 'assistant'
        ]

        # Dependencies keywords
        dep_keywords = [
            'bepinex', 'framework', 'library', 'api', 'dependency', 'hook',
            'patcher', 'modding framework', 'core mod', 'required'
        ]
        
        # Check each category
        categories_to_check = [
            (boss_keywords, "boss_combat_overhaul"),
            (loot_keywords, "loot_overhaul"),
            (magic_keywords, "magic_classes"),
            (skills_keywords, "skills_progression"),
            (gear_keywords, "gear_customization"),
            (coop_keywords, "coop_stability"),
            (qol_keywords, "quality_of_life"),
            (dep_keywords, "dependencies")
        ]
        
        for keywords, category in categories_to_check:
            score = 0
            
            # Check mod name (higher weight)
            for keyword in keywords:
                if keyword in mod_name_lower:
                    score += 3
            
            # Check description
            for keyword in keywords:
                if keyword in description_lower:
                    score += 2
            
            # Check file names
            for file_name in file_names_lower:
                for keyword in keywords:
                    if keyword in file_name:
                        score += 1
            
            category_scores[category] = score
        
        # Find the category with the highest score
        best_category = max(category_scores.items(), key=lambda x: x[1])
        
        # Only categorize if we have a significant match (score >= 3)
        if best_category[1] >= 3:
            return best_category[0]
        else:
            return "doesnt_fit"
    
    def generate_detailed_file_analysis(self, file_names):
        """Generate detailed file analysis for AI consumption"""
        file_analysis = "=== DETAILED FILE ANALYSIS ===\n\n"
        
        # File structure analysis
        file_analysis += f"Total files: {len(file_names)}\n"
        
        # Categorize files by type
        dll_files = [f for f in file_names if f.endswith('.dll')]
        config_files = [f for f in file_names if any(ext in f.lower() for ext in ['.cfg', '.json', '.xml', 'config'])]
        texture_files = [f for f in file_names if any(ext in f.lower() for ext in ['.dds', '.png', '.jpg', '.jpeg'])]
        audio_files = [f for f in file_names if any(ext in f.lower() for ext in ['.ogg', '.wav', '.mp3'])]
        script_files = [f for f in file_names if any(ext in f.lower() for ext in ['.cs', '.dll', 'script'])]
        
        file_analysis += f"DLL files: {len(dll_files)}\n"
        file_analysis += f"Config files: {len(config_files)}\n"
        file_analysis += f"Texture files: {len(texture_files)}\n"
        file_analysis += f"Audio files: {len(audio_files)}\n"
        file_analysis += f"Script files: {len(script_files)}\n\n"
        
        # Check for BepInEx structure
        bepinex_files = [f for f in file_names if 'bepinex' in f.lower()]
        if bepinex_files:
            file_analysis += "BEPINEX MOD DETECTED\n"
            file_analysis += "This is a BepInEx plugin mod.\n\n"
        
        # Check for manifest files and read their content
        manifest_files = [f for f in file_names if 'manifest' in f.lower()]
        if manifest_files:
            file_analysis += "MANIFEST FILES FOUND:\n"
            for manifest in manifest_files:
                file_analysis += f"- {manifest}\n"
            file_analysis += "\n"
        
        # Key file analysis with more detail
        file_analysis += "KEY FILES:\n"
        for file_name in file_names[:20]:  # Show first 20 files
            file_analysis += f"- {file_name}\n"
        
        if len(file_names) > 20:
            file_analysis += f"... and {len(file_names) - 20} more files\n"
        
        # Content type analysis
        file_analysis += "\nCONTENT ANALYSIS:\n"
        if dll_files:
            file_analysis += "- Contains executable code (DLLs)\n"
        if config_files:
            file_analysis += "- Has configuration options\n"
        if texture_files:
            file_analysis += "- Includes visual assets\n"
        if audio_files:
            file_analysis += "- Contains audio content\n"
        if bepinex_files:
            file_analysis += "- BepInEx plugin structure\n"
        
        # Enhanced content pattern detection
        file_analysis += "\nDETAILED CONTENT PATTERNS:\n"
        
        # Combat and boss patterns
        combat_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['combat', 'boss', 'enemy', 'monster', 'creature', 'attack', 'weapon', 'damage'])]
        if combat_files:
            file_analysis += f"- Combat/Boss content: {len(combat_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(combat_files[:5]) + "\n"
        
        # Inventory and UI patterns
        inventory_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['inventory', 'ui', 'interface', 'hud', 'menu', 'slot', 'bag', 'container'])]
        if inventory_files:
            file_analysis += f"- Inventory/UI content: {len(inventory_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(inventory_files[:5]) + "\n"
        
        # Magic and spells patterns
        magic_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['magic', 'spell', 'runic', 'mana', 'enchant', 'sorcery', 'wizard'])]
        if magic_files:
            file_analysis += f"- Magic/Spell content: {len(magic_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(magic_files[:5]) + "\n"
        
        # Skills and progression patterns
        skill_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['skill', 'progression', 'level', 'experience', 'xp', 'profession', 'farming'])]
        if skill_files:
            file_analysis += f"- Skills/Progression content: {len(skill_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(skill_files[:5]) + "\n"
        
        # Building and construction patterns
        building_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['building', 'construction', 'hammer', 'workbench', 'forge', 'blueprint', 'snap'])]
        if building_files:
            file_analysis += f"- Building/Construction content: {len(building_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(building_files[:5]) + "\n"
        
        # Quality of Life patterns
        qol_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['auto', 'quick', 'stack', 'sort', 'organize', 'hotkey', 'shortcut', 'tooltip', 'minimap', 'clock', 'portal', 'teleport'])]
        if qol_files:
            file_analysis += f"- Quality of Life content: {len(qol_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(qol_files[:5]) + "\n"
        
        # Loot and items patterns
        loot_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['loot', 'item', 'drop', 'rarity', 'chest', 'treasure', 'reward', 'epic', 'legendary'])]
        if loot_files:
            file_analysis += f"- Loot/Items content: {len(loot_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(loot_files[:5]) + "\n"
        
        # Gear and customization patterns
        gear_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['gear', 'armor', 'weapon', 'set', 'cosmetic', 'appearance', 'customization', 'vanity'])]
        if gear_files:
            file_analysis += f"- Gear/Customization content: {len(gear_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(gear_files[:5]) + "\n"
        
        # Multiplayer and server patterns
        mp_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['server', 'multiplayer', 'coop', 'network', 'sync', 'anti-cheat', 'stability'])]
        if mp_files:
            file_analysis += f"- Multiplayer/Server content: {len(mp_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(mp_files[:5]) + "\n"
        
        # File size and complexity analysis
        file_analysis += "\nMOD COMPLEXITY ANALYSIS:\n"
        if len(dll_files) > 5:
            file_analysis += "- High complexity: Many DLL files suggest extensive code modifications\n"
        elif len(dll_files) > 2:
            file_analysis += "- Medium complexity: Several DLL files suggest moderate modifications\n"
        else:
            file_analysis += "- Low complexity: Few DLL files, likely configuration or asset mod\n"
        
        if len(config_files) > 3:
            file_analysis += "- Highly configurable: Many config files for customization\n"
        elif len(config_files) > 0:
            file_analysis += "- Configurable: Some config files for basic settings\n"
        else:
            file_analysis += "- No configuration: Likely a simple asset or behavior mod\n"
        
        if len(texture_files) > 10:
            file_analysis += "- Visual overhaul: Many texture files suggest significant visual changes\n"
        elif len(texture_files) > 3:
            file_analysis += "- Visual additions: Several texture files for specific content\n"
        else:
            file_analysis += "- Minimal visuals: Few texture files, likely code-focused mod\n"
        
        return file_analysis
    
    def generate_ai_summary(self):
        """
        Generate an AI-enhanced summary of the analyzed mod
        """
        if not hasattr(self, 'current_analysis'):
            messagebox.showerror("Error", "Please analyze a mod first")
            return
        # Check if LMStudio is available
        if not self.lmstudio.check_api_availability():
            messagebox.showwarning(
                "LM Studio Unavailable", 
                "LM Studio server is not running.\n\n"
                "To enable AI features:\n"
                "1. Open LM Studio application\n"
                "2. Go to Settings > API Server\n"
                "3. Enable 'Start API Server'\n"
                "4. Set port to 1234\n"
                "5. Click 'Start Server'\n\n"
                "The app will continue to work without AI features."
            )
            return
        try:
            manifest_json = self.current_analysis.get('manifest_json', {})
            file_names = self.current_analysis.get('file_names', [])
            mod_name = manifest_json.get('name', 'Unknown Mod')
            mod_author = manifest_json.get('author', 'Unknown')
            mod_description = manifest_json.get('description', 'No description available')
            file_analysis = self.generate_detailed_file_analysis(file_names)
            if hasattr(self, 'current_analysis') and 'file_path' in self.current_analysis:
                try:
                    with zipfile.ZipFile(self.current_analysis['file_path'], 'r') as zip_file:
                        content_info = self.extract_file_content_info(file_names, zip_file)
                        file_analysis += content_info
                except:
                    pass
            # Generate AI summary
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, "Generating AI summary... Please wait.\n\n")
            self.root.update()
            ai_summary = self.lmstudio.generate_mod_summary(
                mod_name, mod_author, mod_description, file_analysis
            )
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, ai_summary)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate AI summary: {str(e)}")
    
    def get_ai_category_suggestion(self):
        """
        Get AI suggestion for mod categorization
        """
        if not hasattr(self, 'current_analysis'):
            messagebox.showerror("Error", "Please analyze a mod first")
            return
        # Check if LMStudio is available
        if not self.lmstudio.check_api_availability():
            messagebox.showwarning(
                "LM Studio Unavailable", 
                "LM Studio server is not running.\n\n"
                "To enable AI features:\n"
                "1. Open LM Studio application\n"
                "2. Go to Settings > API Server\n"
                "3. Enable 'Start API Server'\n"
                "4. Set port to 1234\n"
                "5. Click 'Start Server'\n\n"
                "The app will continue to work without AI features."
            )
            return
        try:
            manifest_json = self.current_analysis.get('manifest_json', {})
            file_names = self.current_analysis.get('file_names', [])
            mod_name = manifest_json.get('name', 'Unknown Mod')
            mod_description = manifest_json.get('description', 'No description available')
            file_analysis = self.generate_detailed_file_analysis(file_names)
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, "Getting AI category suggestion... Please wait.\n")
            self.root.update()
            ai_suggestion = self.lmstudio.suggest_category(
                mod_name, mod_description, file_analysis
            )
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, f"AI Suggested Category: {ai_suggestion}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get AI category suggestion: {str(e)}")
    
    def get_ai_mod_recommendation(self):
        """
        Get AI recommendation for including/excluding the mod in the modlist
        """
        if not hasattr(self, 'current_analysis'):
            messagebox.showerror("Error", "Please analyze a mod first")
            return
        # Check if LMStudio is available
        if not self.lmstudio.check_api_availability():
            messagebox.showwarning(
                "LM Studio Unavailable", 
                "LM Studio server is not running.\n\n"
                "To enable AI features:\n"
                "1. Open LM Studio application\n"
                "2. Go to Settings > API Server\n"
                "3. Enable 'Start API Server'\n"
                "4. Set port to 1234\n"
                "5. Click 'Start Server'\n\n"
                "The app will continue to work without AI features."
            )
            return
        try:
            manifest_json = self.current_analysis.get('manifest_json', {})
            file_names = self.current_analysis.get('file_names', [])
            mod_name = manifest_json.get('name', 'Unknown Mod')
            mod_description = manifest_json.get('description', 'No description available')
            file_analysis = self.generate_detailed_file_analysis(file_names)
            feedback_prompt = self.get_feedback_prompt()
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, "Getting AI mod recommendation... Please wait.\n")
            self.root.update()
            ai_recommendation = self.lmstudio.get_mod_recommendation(
                mod_name, mod_description, file_analysis + feedback_prompt
            )
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, ai_recommendation)
            self.add_agree_disagree_buttons(ai_recommendation)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get AI mod recommendation: {str(e)}")

    def add_agree_disagree_buttons(self, ai_recommendation):
        # Remove any existing buttons
        if hasattr(self, 'agree_button') and self.agree_button:
            self.agree_button.destroy()
        if hasattr(self, 'disagree_button') and self.disagree_button:
            self.disagree_button.destroy()
        # Place buttons below the analysis_text widget
        parent = self.analysis_text.master
        self.agree_button = tk.Button(parent, text="Agree", bg=self.colors['success'], fg=self.colors['button_fg'], relief=tk.FLAT, bd=0, padx=15, pady=5, command=self.on_agree)
        self.agree_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.disagree_button = tk.Button(parent, text="Disagree", bg=self.colors['error'], fg=self.colors['button_fg'], relief=tk.FLAT, bd=0, padx=15, pady=5, command=lambda: self.on_disagree(ai_recommendation))
        self.disagree_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

    def on_agree(self):
        if hasattr(self, 'agree_button') and self.agree_button:
            self.agree_button.destroy()
        if hasattr(self, 'disagree_button') and self.disagree_button:
            self.disagree_button.destroy()
        messagebox.showinfo("Thank you", "Your agreement has been noted.")

    def on_disagree(self, ai_recommendation):
        if hasattr(self, 'agree_button') and self.agree_button:
            self.agree_button.destroy()
        if hasattr(self, 'disagree_button') and self.disagree_button:
            self.disagree_button.destroy()
        reason = simpledialog.askstring("Disagree with AI", "Please explain why you disagree with the AI's recommendation:")
        if reason:
            feedback_entry = f"Disagreed with: '{ai_recommendation}'. Reason: {reason}"
            self.user_feedback.append(feedback_entry)
            self.save_feedback()
            messagebox.showinfo("Feedback Saved", "Your feedback has been saved and will be used to improve future AI suggestions.")
        else:
            messagebox.showinfo("No Feedback", "No feedback was provided.")
    
    def check_ai_status(self):
        """
        Check if the local LMStudio API is available and update status
        """
        def check():
            if self.lmstudio.check_api_availability():
                self.ai_status_label.config(text="AI: Available ✅", fg="green")
            else:
                self.ai_status_label.config(text="AI: Unavailable ❌", fg="red")
        
        # Run the check in a separate thread to avoid blocking the UI
        import threading
        thread = threading.Thread(target=check)
        thread.daemon = True
        thread.start()
    
    def analyze_zip_file(self, file_path):
        analysis = []
        analysis.append("=== MOD ANALYSIS ===\n")
        dependencies = set()
        # New: Collect advanced file categories
        localization_files = []
        script_files = []
        prefab_files = []
        worldgen_files = []
        event_files = []
        ui_files = []
        audio_files = []
        doc_files = []
        loadorder_files = []
        patch_files = []
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                # List all files
                analysis.append("Files in mod:\n")
                for file_info in zip_file.filelist:
                    analysis.append(f"  {file_info.filename}\n")
                
                # Look for common mod files
                file_names = [f.filename for f in zip_file.filelist]
                
                # Advanced file categorization
                for fname in file_names:
                    lower = fname.lower()
                    if any(x in lower for x in ['localization', 'lang', 'translation']) or lower.endswith('.json') and 'local' in lower:
                        localization_files.append(fname)
                    if lower.endswith('.cs'):
                        script_files.append(fname)
                    if any(x in lower for x in ['prefab', 'asset', 'unity3d']) or lower.endswith(('.prefab', '.asset', '.unity3d', '.fbx', '.obj', '.3ds')):
                        prefab_files.append(fname)
                    if any(x in lower for x in ['biome', 'worldgen', 'map', 'seed']) or lower.endswith(('biomes.json', 'worldgen.cfg')):
                        worldgen_files.append(fname)
                    if any(x in lower for x in ['event', 'quest']) or lower.endswith(('events.json', 'quests.json')):
                        event_files.append(fname)
                    if any(x in lower for x in ['ui', 'hud', 'overlay', 'xaml', 'xml']) or lower.endswith(('.xml', '.xaml', '.atlas')):
                        ui_files.append(fname)
                    if lower.endswith(('.ogg', '.wav', '.mp3')):
                        audio_files.append(fname)
                    if any(x in lower for x in ['readme', 'changelog', 'install', 'doc']) or lower.endswith(('.md', '.txt')):
                        doc_files.append(fname)
                    if any(x in lower for x in ['loadorder', 'modlist']) or lower.endswith(('.txt', '.json')):
                        loadorder_files.append(fname)
                    if any(x in lower for x in ['patch', 'harmony', 'hook']) or lower.endswith(('patcher.cfg', 'harmony.json')):
                        patch_files.append(fname)
                
                # Check for BepInEx structure
                bepinex_files = [f for f in file_names if 'bepinex' in f.lower()]
                if bepinex_files:
                    analysis.append("\n=== BEPINEX MOD DETECTED ===\n")
                    analysis.append("This appears to be a BepInEx mod.\n")
                    dependencies.add("BepInEx")
                
                # Check for manifest files
                manifest_files = [f for f in file_names if 'manifest' in f.lower()]
                manifest_json = None
                if manifest_files:
                    analysis.append("\n=== MANIFEST FILES ===\n")
                    for manifest in manifest_files:
                        analysis.append(f"Found: {manifest}\n")
                
                # Try to read manifest.json if it exists
                for file_name in file_names:
                    if 'manifest.json' in file_name.lower():
                        try:
                            with zip_file.open(file_name) as f:
                                manifest_data = json.loads(f.read().decode('utf-8'))
                                manifest_json = manifest_data
                                # Check for dependencies in manifest
                                deps = manifest_data.get('dependencies')
                                if deps:
                                    if isinstance(deps, list):
                                        for dep in deps:
                                            dependencies.add(str(dep))
                                    elif isinstance(deps, dict):
                                        for dep in deps.keys():
                                            dependencies.add(str(dep))
                                    else:
                                        dependencies.add(str(deps))
                                break
                        except:
                            pass
                
                # Check for DLL files
                dll_files = [f for f in file_names if f.endswith('.dll')]
                if dll_files:
                    analysis.append("\n=== DLL FILES ===\n")
                    for dll in dll_files:
                        analysis.append(f"Found: {dll}\n")
                        # Heuristic: add common frameworks as dependencies
                        if 'bepinex' in dll.lower():
                            dependencies.add("BepInEx")
                        if 'jotunn' in dll.lower():
                            dependencies.add("Jotunn")
                        if 'valheimlib' in dll.lower():
                            dependencies.add("ValheimLib")
                        if 'hookgenpatcher' in dll.lower():
                            dependencies.add("HookGenPatcher")
                
                # Check for configuration files
                config_files = [f for f in file_names if 'config' in f.lower()]
                if config_files:
                    analysis.append("\n=== CONFIGURATION FILES ===\n")
                    for config in config_files:
                        analysis.append(f"Found: {config}\n")
                
                if manifest_json:
                    analysis.append("\n=== MANIFEST INFORMATION ===\n")
                    if 'name' in manifest_json:
                        analysis.append(f"Mod Name: {manifest_json['name']}\n")
                    if 'author' in manifest_json:
                        analysis.append(f"Author: {manifest_json['author']}\n")
                    if 'description' in manifest_json:
                        analysis.append(f"Description: {manifest_json['description']}\n")
                    if 'version' in manifest_json:
                        analysis.append(f"Version: {manifest_json['version']}\n")
                
                # Dependencies section
                analysis.append("\n=== DEPENDENCIES ===\n")
                if dependencies:
                    for dep in sorted(dependencies):
                        analysis.append(f"- {dep}\n")
                else:
                    analysis.append("(None detected)\n")
                
                # New: Summarize advanced file categories
                def summarize_list(title, files):
                    if files:
                        analysis.append(f"\n=== {title} ===\n")
                        for f in files[:10]:
                            analysis.append(f"- {f}\n")
                        if len(files) > 10:
                            analysis.append(f"...and {len(files)-10} more\n")
                summarize_list("LOCALIZATION FILES", localization_files)
                summarize_list("SCRIPT/SOURCE FILES", script_files)
                summarize_list("PREFAB/ASSET FILES", prefab_files)
                summarize_list("WORLDGEN/MAP FILES", worldgen_files)
                summarize_list("EVENT/QUEST FILES", event_files)
                summarize_list("UI/OVERLAY FILES", ui_files)
                summarize_list("AUDIO FILES", audio_files)
                summarize_list("DOCUMENTATION/CHANGELOGS", doc_files)
                summarize_list("LOAD ORDER/DEPENDENCY FILES", loadorder_files)
                summarize_list("PATCH/HOOK FILES", patch_files)
                
                # Summary
                analysis.append("\n=== SUMMARY ===\n")
                analysis.append(f"Total files: {len(file_names)}\n")
                analysis.append(f"BepInEx files: {len(bepinex_files)}\n")
                analysis.append(f"DLL files: {len(dll_files)}\n")
                analysis.append(f"Config files: {len(config_files)}\n")
                
                if manifest_json:
                    analysis.append("✅ Manifest file found and readable\n")
                else:
                    analysis.append("⚠️ No readable manifest file found\n")
                
                # Save a copy of the zip file automatically
                mod_base = manifest_json['name'] if manifest_json and 'name' in manifest_json else os.path.splitext(os.path.basename(file_path))[0]
                mod_version = manifest_json['version'] if manifest_json and 'version' in manifest_json else time.strftime('%Y%m%d%H%M%S')
                safe_mod_base = re.sub(r'[^a-zA-Z0-9_\-]', '_', mod_base)
                safe_mod_version = re.sub(r'[^a-zA-Z0-9_\-]', '_', str(mod_version))
                dest_filename = f"{safe_mod_base}_{safe_mod_version}.zip"
                dest_path = os.path.join(self.analyzed_mods_dir, dest_filename)
                # Prevent duplicate analyzed mods (by name+version or file)
                already = any((m['name'] == mod_base and m['version'] == mod_version) for m in self.analyzed_mods)
                file_exists = os.path.exists(dest_path)
                if not already and not file_exists:
                    shutil.copy2(file_path, dest_path)
                # Add to analyzed_mods list if not already present
                analyzed_entry = {
                    'name': mod_base,
                    'version': mod_version,
                    'author': manifest_json['author'] if manifest_json and 'author' in manifest_json else '',
                    'description': manifest_json['description'] if manifest_json and 'description' in manifest_json else '',
                    'zip_path': dest_path,
                    'dependencies': sorted(list(dependencies)),
                    'file_names': file_names,
                    'timestamp': int(time.time()),
                    'localization_files': localization_files,
                    'script_files': script_files,
                    'prefab_files': prefab_files,
                    'worldgen_files': worldgen_files,
                    'event_files': event_files,
                    'ui_files': ui_files,
                    'audio_files': audio_files,
                    'doc_files': doc_files,
                    'loadorder_files': loadorder_files,
                    'patch_files': patch_files
                }
                # Avoid duplicates by name+version
                if not already:
                    self.analyzed_mods.append(analyzed_entry)
                    self.save_analyzed_mods()
                
                # Store analysis data for auto-add functionality
                self.current_analysis = {
                    'file_names': file_names,
                    'manifest_json': manifest_json,
                    'bepinex_files': bepinex_files,
                    'dll_files': dll_files,
                    'config_files': config_files,
                    'dependencies': sorted(list(dependencies)),
                    'zip_path': dest_path,
                    'localization_files': localization_files,
                    'script_files': script_files,
                    'prefab_files': prefab_files,
                    'worldgen_files': worldgen_files,
                    'event_files': event_files,
                    'ui_files': ui_files,
                    'audio_files': audio_files,
                    'doc_files': doc_files,
                    'loadorder_files': loadorder_files,
                    'patch_files': patch_files
                }
                
                # Check for content overlap with existing mods
                overlap_report = self.check_content_overlap(file_names, manifest_json)
                
                # Add overlap report to analysis
                if overlap_report and overlap_report != "No existing mods to compare against.":
                    analysis.append("\n=== CONTENT OVERLAP ANALYSIS ===\n")
                    analysis.append(overlap_report)
                    analysis.append("\n")
                
                # Additional compatibility checks for duplicate DLLs/configs/assets
                duplicate_flags = []
                for category, mods in self.mods_data.items():
                    for mod in mods:
                        if 'file_analysis' in mod:
                            existing_files = set(mod['file_analysis'].get('file_names', []))
                            # DLL overlap
                            overlap_dlls = set(dll_files) & existing_files
                            if overlap_dlls:
                                duplicate_flags.append(f"⚠️ DLL file(s) potentially duplicated with '{mod['name']}': {', '.join(overlap_dlls)}")
                            # Config overlap
                            overlap_configs = set(config_files) & existing_files
                            if overlap_configs:
                                duplicate_flags.append(f"⚠️ Config file(s) potentially duplicated with '{mod['name']}': {', '.join(overlap_configs)}")
                            # Asset overlap (textures, models, etc.)
                            asset_exts = ['.png', '.jpg', '.jpeg', '.dds', '.obj', '.fbx', '.3ds']
                            asset_files = [f for f in file_names if any(f.lower().endswith(ext) for ext in asset_exts)]
                            existing_assets = [f for f in existing_files if any(f.lower().endswith(ext) for ext in asset_exts)]
                            overlap_assets = set(asset_files) & set(existing_assets)
                            if overlap_assets:
                                duplicate_flags.append(f"⚠️ Asset file(s) potentially duplicated with '{mod['name']}': {', '.join(overlap_assets)}")
                if duplicate_flags:
                    analysis.append("\n=== COMPATIBILITY WARNINGS ===\n")
                    for flag in duplicate_flags:
                        analysis.append(flag + "\n")
        
        except zipfile.BadZipFile:
            analysis.append("❌ Invalid zip file\n")
        except Exception as e:
            analysis.append(f"❌ Error reading file: {str(e)}\n")
        
        return "".join(analysis)
    
    def check_content_overlap(self, new_file_names, new_manifest):
        """Check for content overlap with existing mods"""
        if not hasattr(self, 'mods_data') or not self.mods_data:
            return "No existing mods to compare against."
        
        overlap_found = []
        new_mod_name = new_manifest.get('name', 'Unknown') if new_manifest else 'Unknown'
        
        # Create a library of common file patterns and content types
        content_library = {
            'textures': ['.dds', '.png', '.jpg', '.jpeg', 'texture', 'tex'],
            'models': ['.obj', '.fbx', '.3ds', 'model', 'mesh', 'asset'],
            'scripts': ['.cs', '.dll', 'script', 'assembly', 'plugin'],
            'configs': ['.cfg', '.json', '.xml', 'config', 'settings'],
            'audio': ['.ogg', '.wav', '.mp3', 'sound', 'audio', 'music'],
            'ui': ['ui', 'gui', 'interface', 'menu', 'hud'],
            'localization': ['localization', 'lang', 'translation', 'text'],
            'prefabs': ['prefab', 'prefabs', 'asset'],
            'spawns': ['spawn', 'spawns', 'entity', 'creature'],
            'items': ['item', 'items', 'weapon', 'armor', 'gear'],
            'biomes': ['biome', 'biomes', 'environment', 'world'],
            'effects': ['effect', 'effects', 'particle', 'vfx'],
            'animations': ['anim', 'animation', 'motion'],
            'shaders': ['shader', 'material', 'rendering']
        }
        
        # Analyze new mod's content types
        new_content_types = {}
        for file_name in new_file_names:
            file_lower = file_name.lower()
            for content_type, patterns in content_library.items():
                for pattern in patterns:
                    if pattern in file_lower:
                        if content_type not in new_content_types:
                            new_content_types[content_type] = []
                        new_content_types[content_type].append(file_name)
                        break
        
        # Check against existing mods
        for category, mods in self.mods_data.items():
            for existing_mod in mods:
                existing_mod_name = existing_mod['name']
                
                # Skip if this is the same mod (by name)
                if existing_mod_name.lower() == new_mod_name.lower():
                    continue
                
                # Check if existing mod has stored file analysis
                if 'file_analysis' in existing_mod:
                    existing_files = existing_mod['file_analysis'].get('file_names', [])
                    existing_content_types = existing_mod['file_analysis'].get('content_types', {})
                    
                    # Compare content types
                    overlap_score = 0
                    overlapping_content = []
                    
                    for content_type, new_files in new_content_types.items():
                        if content_type in existing_content_types:
                            # Calculate overlap percentage
                            new_count = len(new_files)
                            existing_count = len(existing_content_types[content_type])
                            overlap_score += min(new_count, existing_count)
                            overlapping_content.append(content_type)
                    
                    if overlap_score > 0:
                        overlap_found.append({
                            'mod_name': existing_mod_name,
                            'category': category.replace('_', ' ').title(),
                            'overlap_score': overlap_score,
                            'overlapping_content': overlapping_content
                        })
        
        # Generate overlap report
        if not overlap_found:
            return "✅ No significant content overlap detected with existing mods."
        
        report = f"⚠️  Potential content overlap detected:\n\n"
        
        # Sort by overlap score (highest first)
        overlap_found.sort(key=lambda x: x['overlap_score'], reverse=True)
        
        for overlap in overlap_found[:5]:  # Show top 5 overlaps
            report += f"📦 {overlap['mod_name']} ({overlap['category']})\n"
            report += f"   Overlap Score: {overlap['overlap_score']}\n"
            report += f"   Overlapping Content: {', '.join(overlap['overlapping_content'])}\n\n"
        
        if len(overlap_found) > 5:
            report += f"... and {len(overlap_found) - 5} more potential overlaps\n"
        
        report += "\n💡 Tip: High overlap scores may indicate:\n"
        report += "   • Compatible mods that work together\n"
        report += "   • Potential conflicts that need testing\n"
        report += "   • Redundant functionality\n"
        
        return report
    
    def update_preview(self):
        self.preview_text.delete("1.0", tk.END)
        
        format_type = self.export_format_var.get()
        
        if format_type == "json":
            preview = json.dumps(self.mods_data, indent=2)
        elif format_type == "txt":
            preview = self.format_as_text()
        elif format_type == "csv":
            preview = self.format_as_csv()
        
        self.preview_text.insert(tk.END, preview)
    
    def format_as_text(self):
        text = "VALHEIM MODLIST\n"
        text += "=" * 50 + "\n\n"
        
        for category, mods in self.mods_data.items():
            if mods:
                text += f"{category.replace('_', ' ').upper()}\n"
                text += "-" * 30 + "\n"
                for mod in mods:
                    text += f"Name: {mod['name']}\n"
                    text += f"Author: {mod['author']}\n"
                    text += f"Description: {mod['description']}\n"
                    text += "\n"
        
        return text
    
    def format_as_csv(self):
        csv = "Category,Name,Author,Description\n"
        
        for category, mods in self.mods_data.items():
            for mod in mods:
                csv += f"{category},{mod['name']},{mod['author']},{mod['description']}\n"
        
        return csv
    
    def export_modlist(self):
        format_type = self.export_format_var.get()
        
        filename = filedialog.asksaveasfilename(
            title="Export Modlist",
            defaultextension=f".{format_type}",
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    if format_type == "json":
                        json.dump(self.mods_data, f, indent=2)
                    elif format_type == "txt":
                        f.write(self.format_as_text())
                    elif format_type == "csv":
                        f.write(self.format_as_csv())
                
                messagebox.showinfo("Success", f"Modlist exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def save_data(self):
        try:
            with open('modlist_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.mods_data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def load_data(self):
        try:
            if os.path.exists('modlist_data.json'):
                with open('modlist_data.json', 'r', encoding='utf-8') as f:
                    self.mods_data = json.load(f)
            # Ensure all category keys exist after loading
            for key in [
                "boss_combat_overhaul",
                "loot_overhaul",
                "magic_classes",
                "skills_progression",
                "gear_customization",
                "coop_stability",
                "quality_of_life",
                "dependencies",
                "doesnt_fit",
            ]:
                self.mods_data.setdefault(key, [])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def extract_file_content_info(self, file_names, zip_file=None):
        """Extract additional information from config files and manifests"""
        content_info = ""
        
        if not zip_file:
            return content_info
        
        try:
            # Read manifest files for additional info
            manifest_files = [f for f in file_names if 'manifest' in f.lower()]
            for manifest_file in manifest_files:
                try:
                    with zip_file.open(manifest_file) as f:
                        manifest_data = json.loads(f.read().decode('utf-8'))
                        content_info += f"\nMANIFEST ANALYSIS ({manifest_file}):\n"
                        if 'name' in manifest_data:
                            content_info += f"- Mod Name: {manifest_data['name']}\n"
                        if 'author' in manifest_data:
                            content_info += f"- Author: {manifest_data['author']}\n"
                        if 'description' in manifest_data:
                            content_info += f"- Description: {manifest_data['description'][:200]}...\n"
                        if 'version' in manifest_data:
                            content_info += f"- Version: {manifest_data['version']}\n"
                        if 'dependencies' in manifest_data:
                            content_info += f"- Dependencies: {manifest_data['dependencies']}\n"
                        if 'website' in manifest_data:
                            content_info += f"- Website: {manifest_data['website']}\n"
                except:
                    pass
            
            # Read config files for settings info
            config_files = [f for f in file_names if any(ext in f.lower() for ext in ['.cfg', '.json', '.xml']) and 'config' in f.lower()]
            if config_files:
                content_info += "\nCONFIGURATION ANALYSIS:\n"
                for config_file in config_files[:3]:  # Limit to first 3 config files
                    try:
                        with zip_file.open(config_file) as f:
                            config_content = f.read().decode('utf-8')
                            # Extract key settings
                            lines = config_content.split('\n')
                            settings = []
                            for line in lines[:20]:  # First 20 lines
                                if '=' in line or ':' in line:
                                    settings.append(line.strip())
                            if settings:
                                content_info += f"- {config_file}: {len(settings)} settings found\n"
                                content_info += "  Sample settings: " + "; ".join(settings[:5]) + "\n"
                    except:
                        pass
            
            # Look for specific content in text files
            text_files = [f for f in file_names if f.endswith('.txt') or f.endswith('.md') or f.endswith('.readme')]
            if text_files:
                content_info += "\nTEXT CONTENT ANALYSIS:\n"
                for text_file in text_files[:2]:  # Limit to first 2 text files
                    try:
                        with zip_file.open(text_file) as f:
                            text_content = f.read().decode('utf-8')
                            # Look for key information
                            if 'feature' in text_content.lower():
                                content_info += f"- {text_file}: Contains feature descriptions\n"
                            if 'install' in text_content.lower():
                                content_info += f"- {text_file}: Contains installation instructions\n"
                            if 'compatibility' in text_content.lower():
                                content_info += f"- {text_file}: Contains compatibility information\n"
                    except:
                        pass
                        
        except Exception as e:
            content_info += f"\nNote: Could not extract additional file content: {str(e)}\n"
        
        return content_info
    
    def generate_detailed_file_analysis(self, file_names):
        """Generate detailed file analysis for AI consumption"""
        file_analysis = "=== DETAILED FILE ANALYSIS ===\n\n"
        
        # File structure analysis
        file_analysis += f"Total files: {len(file_names)}\n"
        
        # Categorize files by type
        dll_files = [f for f in file_names if f.endswith('.dll')]
        config_files = [f for f in file_names if any(ext in f.lower() for ext in ['.cfg', '.json', '.xml', 'config'])]
        texture_files = [f for f in file_names if any(ext in f.lower() for ext in ['.dds', '.png', '.jpg', '.jpeg'])]
        audio_files = [f for f in file_names if any(ext in f.lower() for ext in ['.ogg', '.wav', '.mp3'])]
        script_files = [f for f in file_names if any(ext in f.lower() for ext in ['.cs', '.dll', 'script'])]
        
        file_analysis += f"DLL files: {len(dll_files)}\n"
        file_analysis += f"Config files: {len(config_files)}\n"
        file_analysis += f"Texture files: {len(texture_files)}\n"
        file_analysis += f"Audio files: {len(audio_files)}\n"
        file_analysis += f"Script files: {len(script_files)}\n\n"
        
        # Check for BepInEx structure
        bepinex_files = [f for f in file_names if 'bepinex' in f.lower()]
        if bepinex_files:
            file_analysis += "BEPINEX MOD DETECTED\n"
            file_analysis += "This is a BepInEx plugin mod.\n\n"
        
        # Check for manifest files and read their content
        manifest_files = [f for f in file_names if 'manifest' in f.lower()]
        if manifest_files:
            file_analysis += "MANIFEST FILES FOUND:\n"
            for manifest in manifest_files:
                file_analysis += f"- {manifest}\n"
            file_analysis += "\n"
        
        # Key file analysis with more detail
        file_analysis += "KEY FILES:\n"
        for file_name in file_names[:20]:  # Show first 20 files
            file_analysis += f"- {file_name}\n"
        
        if len(file_names) > 20:
            file_analysis += f"... and {len(file_names) - 20} more files\n"
        
        # Content type analysis
        file_analysis += "\nCONTENT ANALYSIS:\n"
        if dll_files:
            file_analysis += "- Contains executable code (DLLs)\n"
        if config_files:
            file_analysis += "- Has configuration options\n"
        if texture_files:
            file_analysis += "- Includes visual assets\n"
        if audio_files:
            file_analysis += "- Contains audio content\n"
        if bepinex_files:
            file_analysis += "- BepInEx plugin structure\n"
        
        # Enhanced content pattern detection
        file_analysis += "\nDETAILED CONTENT PATTERNS:\n"
        
        # Combat and boss patterns
        combat_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['combat', 'boss', 'enemy', 'monster', 'creature', 'attack', 'weapon', 'damage'])]
        if combat_files:
            file_analysis += f"- Combat/Boss content: {len(combat_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(combat_files[:5]) + "\n"
        
        # Inventory and UI patterns
        inventory_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['inventory', 'ui', 'interface', 'hud', 'menu', 'slot', 'bag', 'container'])]
        if inventory_files:
            file_analysis += f"- Inventory/UI content: {len(inventory_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(inventory_files[:5]) + "\n"
        
        # Magic and spells patterns
        magic_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['magic', 'spell', 'runic', 'mana', 'enchant', 'sorcery', 'wizard'])]
        if magic_files:
            file_analysis += f"- Magic/Spell content: {len(magic_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(magic_files[:5]) + "\n"
        
        # Skills and progression patterns
        skill_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['skill', 'progression', 'level', 'experience', 'xp', 'profession', 'farming'])]
        if skill_files:
            file_analysis += f"- Skills/Progression content: {len(skill_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(skill_files[:5]) + "\n"
        
        # Building and construction patterns
        building_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['building', 'construction', 'hammer', 'workbench', 'forge', 'blueprint', 'snap'])]
        if building_files:
            file_analysis += f"- Building/Construction content: {len(building_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(building_files[:5]) + "\n"
        
        # Quality of Life patterns
        qol_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['auto', 'quick', 'stack', 'sort', 'organize', 'hotkey', 'shortcut', 'tooltip', 'minimap', 'clock', 'portal', 'teleport'])]
        if qol_files:
            file_analysis += f"- Quality of Life content: {len(qol_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(qol_files[:5]) + "\n"
        
        # Loot and items patterns
        loot_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['loot', 'item', 'drop', 'rarity', 'chest', 'treasure', 'reward', 'epic', 'legendary'])]
        if loot_files:
            file_analysis += f"- Loot/Items content: {len(loot_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(loot_files[:5]) + "\n"
        
        # Gear and customization patterns
        gear_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['gear', 'armor', 'weapon', 'set', 'cosmetic', 'appearance', 'customization', 'vanity'])]
        if gear_files:
            file_analysis += f"- Gear/Customization content: {len(gear_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(gear_files[:5]) + "\n"
        
        # Multiplayer and server patterns
        mp_files = [f for f in file_names if any(pattern in f.lower() for pattern in ['server', 'multiplayer', 'coop', 'network', 'sync', 'anti-cheat', 'stability'])]
        if mp_files:
            file_analysis += f"- Multiplayer/Server content: {len(mp_files)} files\n"
            file_analysis += "  Examples: " + ", ".join(mp_files[:5]) + "\n"
        
        # File size and complexity analysis
        file_analysis += "\nMOD COMPLEXITY ANALYSIS:\n"
        if len(dll_files) > 5:
            file_analysis += "- High complexity: Many DLL files suggest extensive code modifications\n"
        elif len(dll_files) > 2:
            file_analysis += "- Medium complexity: Several DLL files suggest moderate modifications\n"
        else:
            file_analysis += "- Low complexity: Few DLL files, likely configuration or asset mod\n"
        
        if len(config_files) > 3:
            file_analysis += "- Highly configurable: Many config files for customization\n"
        elif len(config_files) > 0:
            file_analysis += "- Configurable: Some config files for basic settings\n"
        else:
            file_analysis += "- No configuration: Likely a simple asset or behavior mod\n"
        
        if len(texture_files) > 10:
            file_analysis += "- Visual overhaul: Many texture files suggest significant visual changes\n"
        elif len(texture_files) > 3:
            file_analysis += "- Visual additions: Several texture files for specific content\n"
        else:
            file_analysis += "- Minimal visuals: Few texture files, likely code-focused mod\n"
        
        return file_analysis

    def load_feedback(self):
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    self.user_feedback = json.load(f)
            except Exception:
                self.user_feedback = []
        else:
            self.user_feedback = []

    def save_feedback(self):
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_feedback, f, indent=2)
        except Exception:
            pass

    def get_feedback_prompt(self):
        if not self.user_feedback:
            return ""
        feedback_text = "\n\nUSER FEEDBACK FOR PROMPT TUNING (incorporate these preferences):\n"
        for idx, fb in enumerate(self.user_feedback, 1):
            feedback_text += f"{idx}. {fb}\n"
        return feedback_text

    def load_analyzed_mods(self):
        if os.path.exists(self.analyzed_mods_file):
            try:
                with open(self.analyzed_mods_file, 'r', encoding='utf-8') as f:
                    self.analyzed_mods = json.load(f)
            except Exception:
                self.analyzed_mods = []
        else:
            self.analyzed_mods = []

    def save_analyzed_mods(self):
        try:
            with open(self.analyzed_mods_file, 'w', encoding='utf-8') as f:
                json.dump(self.analyzed_mods, f, indent=2)
        except Exception:
            pass

    def update_analyzed_mods_listbox(self):
        # Show only analyzed mods not in master mod list
        self.analyzed_listbox.delete(0, tk.END)
        used_mods = set()
        for category, mods in self.mods_data.items():
            for mod in mods:
                if 'name' in mod and 'file_analysis' in mod and 'manifest_json' in mod['file_analysis']:
                    used_mods.add((mod['name'], mod['file_analysis']['manifest_json'].get('version', '')))
        for mod in self.analyzed_mods:
            key = (mod['name'], mod['version'])
            if key not in used_mods:
                display = f"{mod['name']} v{mod['version']}"
                self.analyzed_listbox.insert(tk.END, display)

    def add_analyzed_mod_to_master(self, event):
        # Add selected analyzed mod to master mod list
        selection = self.analyzed_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        mod = [m for i, m in enumerate(self.analyzed_mods) if i == idx][0]
        # Add to 'doesnt_fit' by default, user can edit later
        mod_data = {
            "name": mod['name'],
            "author": mod.get('author', ''),
            "description": mod.get('description', ''),
            "category": "doesnt_fit",
            "file_path": mod['zip_path'],
            "file_analysis": {
                "file_names": mod.get('file_names', []),
                "manifest_json": {
                    "name": mod['name'],
                    "author": mod.get('author', ''),
                    "description": mod.get('description', ''),
                    "version": mod.get('version', '')
                },
                "dependencies": mod.get('dependencies', [])
            }
        }
        self.mods_data['doesnt_fit'].append(mod_data)
        self.save_data()
        self.update_master_modlist()
        self.update_analyzed_mods_listbox()
        messagebox.showinfo("Added", f"Added {mod['name']} v{mod['version']} to Master Modlist (Doesn't Fit)")

    def create_ai_config_tab(self):
        vision_prompt = (
            "I'm creating a custom Valheim modpack and modded server. My tool can interact with the server's API and config files, so I'm looking for structured guidance on gameplay transformation, mod compatibility, and installation order.\n"
            "\nMy Vision:\n"
            "I want to turn Valheim into a bossing- and loot-focused RPG, inspired by Solo Leveling, MMOs, and RuneScape. The experience should reward exploration, enable deep character builds, and create emergent excitement through:\n"
            "- Instanced or roaming bosses\n"
            "- RNG loot (with rare chances for endgame items early)\n"
            "- Magic and class systems\n"
            "- Highly customizable skills/builds\n"
            "- Visual and clothing customization\n"
            "- Exploration incentives (rare loot, random events)\n"
            "\nCore Gameplay Systems to Overhaul:\n"
            "- Character Progression & Leveling\n"
            "- Loot & Equipment (Diablo-style RNG)\n"
            "- Class & Skill Systems (e.g. magic, professions, talent trees)\n"
            "- Enemy Scaling & Elite Affixes\n"
            "- Questing & World Events\n"
            "- Magic & Special Abilities (Skyheim-style spells or custom classes)\n"
            "- UI & Feedback Improvements\n"
            "Other Enhancements:\n"
            "- Quality of Life (craft-from-container, inventory sort, etc.)\n"
            "- Expanded Building & Automation\n"
            "- Immersion/Visual Upgrades (map, seasons, weather, etc.)\n"
            "- World Gen Improvements (larger worlds, more dungeons)\n"
            "- Floating loot items, backpacks, player appearance customization\n"
        )
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="AI Config & Feature Assistant")

        # Top: Feature/goal entry
        feature_frame = tk.Frame(tab, bg=self.colors['bg'])
        feature_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(feature_frame, text="Describe a feature or gameplay goal:", bg=self.colors['bg'], fg=self.colors['fg'], font=("Arial", 12, "bold")).pack(anchor=tk.W)
        self.feature_entry = tk.Entry(feature_frame, font=("Arial", 11), bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        self.feature_entry.pack(fill=tk.X, pady=5)
        tk.Button(feature_frame, text="Find Feature in Mods", command=self.find_feature_in_mods, bg=self.colors['accent'], fg=self.colors['button_fg'], relief=tk.FLAT, bd=0, padx=10, pady=5).pack(anchor=tk.E, pady=5, fill=tk.X)

        # Middle: List of all analyzed mods
        mid_frame = tk.Frame(tab, bg=self.colors['bg'])
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tk.Label(mid_frame, text="Select a mod for config recommendations:", bg=self.colors['bg'], fg=self.colors['fg'], font=("Arial", 11, "bold")).pack(anchor=tk.W)
        self.config_mods_listbox = tk.Listbox(mid_frame, bg="#333", fg="#C9DAB4", selectbackground="#666", selectforeground="#C9DAB4", font=("Consolas", 10), height=8)
        self.config_mods_listbox.pack(fill=tk.X, pady=5)
        self.config_mods_listbox.bind('<<ListboxSelect>>', self.get_mod_config_recommendation)
        self.update_config_mods_listbox()

        # Bottom: AI recommendations/results
        result_frame = tk.Frame(tab, bg=self.colors['bg'])
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tk.Label(result_frame, text="AI Recommendations & Relevant Configs:", bg=self.colors['bg'], fg=self.colors['fg'], font=("Arial", 11, "bold")).pack(anchor=tk.W)
        self.ai_config_result = scrolledtext.ScrolledText(result_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'], font=("Consolas", 10), wrap=tk.WORD)
        self.ai_config_result.pack(fill=tk.BOTH, expand=True, pady=5)
        self.vision_prompt = vision_prompt

    def create_gameplay_changes_tab(self):
        """Tab for searching Thunderstore for gameplay change mods"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="Gameplay Changes")

        tk.Label(tab, text="Search Thunderstore for mods:",
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=10, pady=(10,5))

        search_frame = tk.Frame(tab, bg=self.colors['bg'])
        search_frame.pack(fill=tk.X, padx=10)
        self.thunder_query_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.thunder_query_var,
                 bg=self.colors['entry_bg'], fg=self.colors['entry_fg']).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(search_frame, text="Search", command=self.search_thunderstore_mods,
                  bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                  font=("Arial", 10, "bold"), relief=tk.FLAT, bd=0,
                  padx=10, pady=5).pack(side=tk.RIGHT, padx=(5,0))

        self.thunder_results = scrolledtext.ScrolledText(tab, bg=self.colors['entry_bg'],
                fg=self.colors['entry_fg'], font=("Consolas", 10), wrap=tk.WORD)
        self.thunder_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def search_thunderstore_mods(self):
        """Query Thunderstore for mods matching the user's gameplay goal"""
        query = self.thunder_query_var.get().strip()
        self.thunder_results.delete("1.0", tk.END)
        if not query:
            self.thunder_results.insert(tk.END, "Please enter a search term.")
            return
        self.thunder_results.insert(tk.END, "Searching Thunderstore...\n")
        self.root.update()
        try:
            encoded = requests.utils.quote(query)
            url = f"https://thunderstore.io/api/experimental/package/?query={encoded}&page=1&community=valheim"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            packages = data.get('packages') if isinstance(data, dict) else data
            if not packages:
                self.thunder_results.insert(tk.END, "No mods found.")
                return
            for pkg in packages[:10]:
                name = pkg.get('name') or pkg.get('package_name', 'Unknown')
                author = pkg.get('owner', 'Unknown')
                desc = pkg.get('description', '')
                self.thunder_results.insert(tk.END, f"{name} by {author}\n{desc}\n\n")
        except Exception as e:
            self.thunder_results.insert(tk.END, f"Error fetching data from Thunderstore: {e}")

    def update_config_mods_listbox(self):
        if not hasattr(self, 'config_mods_listbox'):
            return
        self.config_mods_listbox.delete(0, tk.END)
        for mod in self.analyzed_mods:
            display = f"{mod['name']} v{mod['version']}"
            self.config_mods_listbox.insert(tk.END, display)

    def find_feature_in_mods(self):
        feature = self.feature_entry.get().strip()
        if not feature:
            self.ai_config_result.delete("1.0", tk.END)
            self.ai_config_result.insert(tk.END, "Please enter a feature or gameplay goal.")
            return
        # Search all analyzed mods' configs/instructions for relevant snippets
        relevant_snippets = []
        for mod in self.analyzed_mods:
            for fname in mod.get('file_names', []):
                if any(ext in fname.lower() for ext in ['.cfg', '.json', '.xml', '.txt', '.md', 'readme', 'config']):
                    try:
                        zip_path = mod['zip_path']
                        with zipfile.ZipFile(zip_path, 'r') as zf:
                            if fname in zf.namelist():
                                with zf.open(fname) as f:
                                    content = f.read().decode(errors='ignore')
                                    if feature.lower() in content.lower():
                                        snippet = content[:1000]  # Limit snippet size
                                        relevant_snippets.append((mod['name'], fname, snippet))
                    except Exception:
                        continue
        # Prepare AI prompt
        prompt = self.vision_prompt + "\n\nFeature/Goal: " + feature + "\n\n" + (
            "Relevant config/instruction snippets from mods:\n" + "\n".join([f"[{mod}] {fname}:\n{snippet[:500]}..." for mod, fname, snippet in relevant_snippets]) if relevant_snippets else "No relevant config/instruction snippets found.")
        prompt += "\n\nIf you do not have enough information to make a recommendation, say so and request more information or tutorials."
        # Call AI
        self.ai_config_result.delete("1.0", tk.END)
        self.ai_config_result.insert(tk.END, "AI analyzing feature across mods... Please wait.\n\n")
        self.root.update()
        ai_response = self.lmstudio.feature_search(feature, [f"{mod}: {snippet[:500]}..." for mod, fname, snippet in relevant_snippets], prompt)
        self.ai_config_result.delete("1.0", tk.END)
        self.ai_config_result.insert(tk.END, ai_response)

    def get_mod_config_recommendation(self, event):
        selection = self.config_mods_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        mod = self.analyzed_mods[idx]
        # Extract all config/instruction files
        config_snippets = []
        for fname in mod.get('file_names', []):
            if any(ext in fname.lower() for ext in ['.cfg', '.json', '.xml', '.txt', '.md', 'readme', 'config']):
                try:
                    zip_path = mod['zip_path']
                    with zipfile.ZipFile(zip_path, 'r') as zf:
                        if fname in zf.namelist():
                            with zf.open(fname) as f:
                                content = f.read().decode(errors='ignore')
                                snippet = content[:1000]
                                config_snippets.append((fname, snippet))
                except Exception:
                    continue
        # Prepare AI prompt
        prompt = self.vision_prompt + f"\n\nMod: {mod['name']} v{mod['version']}\n" + (
            "\nConfig/instruction snippets:\n" + "\n".join([f"{fname}:\n{snippet[:500]}..." for fname, snippet in config_snippets]) if config_snippets else "No config/instruction files found.")
        prompt += "\n\nRecommend configuration changes for this mod to best fit the vision. If you do not have enough information, say so and request more information or tutorials."
        # Call AI
        self.ai_config_result.delete("1.0", tk.END)
        self.ai_config_result.insert(tk.END, f"AI analyzing {mod['name']} config... Please wait.\n\n")
        self.root.update()
        ai_response = self.lmstudio.config_suggestion(mod['name'], mod.get('version', ''), [f"{fname}:\n{snippet[:500]}..." for fname, snippet in config_snippets], prompt)
        self.ai_config_result.delete("1.0", tk.END)
        self.ai_config_result.insert(tk.END, ai_response)

    def add_potential_conflicts_button(self):
        # Find the AI Recommendation tab and add a button next to it
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == "Add Mod":
                # Place the button in the same parent as the notebook
                parent = self.notebook.master
                btn = tk.Button(parent, text="Potential Conflicts", command=self.show_potential_conflicts, bg=self.colors['warning'], fg=self.colors['button_fg'], relief=tk.FLAT, bd=0, padx=10, pady=5)
                btn.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=5, fill=tk.X)
                break

    def show_potential_conflicts(self):
        # Analyze potential conflicts for mods in analyzed_mods not in master list
        master_mod_names = set()
        for category, mods in self.mods_data.items():
            for mod in mods:
                master_mod_names.add(mod['name'])
        potential_conflicts = []
        for mod in self.analyzed_mods:
            if mod['name'] in master_mod_names:
                continue
            # Check for overlap with master mods
            overlaps = []
            for category, mods in self.mods_data.items():
                for master_mod in mods:
                    # Compare file names
                    master_files = set(master_mod.get('file_analysis', {}).get('file_names', []))
                    mod_files = set(mod.get('file_names', []))
                    overlap = master_files & mod_files
                    if overlap:
                        overlaps.append((master_mod['name'], list(overlap)))
            if overlaps:
                potential_conflicts.append((mod['name'], overlaps))
        # Show in a popup
        popup = tk.Toplevel(self.root)
        popup.title("Potential Conflicts (Analyzed Mods vs. Master List)")
        popup.geometry("700x500")
        popup.configure(bg=self.colors['bg'])
        tk.Label(popup, text="Potential Conflicts (Analyzed Mods not in Master List)", bg=self.colors['bg'], fg=self.colors['error'], font=("Arial", 14, "bold")).pack(pady=10)
        text = scrolledtext.ScrolledText(popup, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'], font=("Consolas", 10), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        if not potential_conflicts:
            text.insert(tk.END, "No potential conflicts detected between analyzed mods and the master list.")
        else:
            for mod_name, overlaps in potential_conflicts:
                text.insert(tk.END, f"\n=== {mod_name} ===\n")
                for master_mod, files in overlaps:
                    text.insert(tk.END, f"  Conflicts with: {master_mod}\n    Overlapping files: {', '.join(files)}\n")
        tk.Button(popup, text="Close", command=popup.destroy, bg=self.colors['accent'], fg=self.colors['button_fg'], relief=tk.FLAT, bd=0, padx=10, pady=5).pack(pady=10, fill=tk.X)

    def on_close(self):
        """Handle application close event by persisting data"""
        try:
            self.save_data()
            self.save_analyzed_mods()
            self.save_feedback()
        finally:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = ValheimModlistBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main() 