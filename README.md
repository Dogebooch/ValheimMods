# Valheim Modlist Builder

A beautiful, user-friendly application for building and managing Valheim modlists with an earthy, forest-themed GUI.

## Features

### 🎮 Mod Management
- **Categorize mods** into different types:
  - **Boss & Combat Overhaul**: Harder and more numerous bosses, roaming encounters, boss affixes, difficulty scaling
  - **Loot Overhaul**: Randomized high-risk/high-reward loot, enhanced loot tables, rare materials, item customization
  - **Magic & Classes**: Magic spell systems, class/ability overhauls, magical gear and visuals
  - **Skills & Progression**: Runescape-style skills, professions system, attribute/level systems, build diversity
  - **Gear & Customization**: New armor/weapon sets, cosmetic items, tameable pets, appearance customization
  - **Co-op Stability**: Server optimization, multiplayer stability, anti-cheat measures
  - **Dependencies**: Core frameworks or libraries required by other mods
  - **Doesn't Fit**: Other mods
- **Add mod details** including name, author, and description
- **View mods by category** with a clean, organized display
- **Delete mods** from your list
- **Auto-categorization** based on intelligent content analysis
- **Sort and filter mods** by name, author, category, or gameplay change

### 📁 Mod Analysis
- **Upload zip files** containing Valheim mods
- **Automatic analysis** of mod contents including:
  - File structure detection
  - BepInEx compatibility check
  - Manifest file parsing
  - DLL file identification
  - Configuration file detection
- **Detailed summary** of what the mod does and how it's structured
- **Auto-add to modlist** with automatic categorization
- **AI-Enhanced Analysis** using local GPT4All:
  - Generate comprehensive mod summaries
  - Get AI category suggestions
  - **AI mod recommendations** (INCLUDE/EXCLUDE based on your 2-player co-op goals)
  - Enhanced mod understanding and recommendations
  - LocalDocs integration for reference-based analysis
  - **Thunderstore search** for mods by gameplay keyword

### 📤 Export Options
- **Multiple export formats**:
  - JSON (structured data)
  - TXT (readable text format)
  - CSV (spreadsheet compatible)
- **Live preview** of export format before saving
- **Custom file naming** and location selection

## Installation

1. **Requirements**: Python 3.6 or higher
2. **Dependencies**: Install required packages:
   ```bash
   pip install requests openai
   ```
3. **Run the application**:
   ```bash
   python app.py
   ```
   
   Or alternatively:
   ```bash
   python valheim_modlist_builder.py
   ```

## How to Use

### Adding Mods
1. Go to the "Mods Management" tab
2. Fill in the mod details:
   - **Name**: The mod's name
   - **Author**: Who created the mod
   - **Description**: What the mod does
   - **Category**: Select the appropriate category
3. Click "Add Mod" to save it to your list
4. Use the dropdown to view mods by category

### Auto-Adding Mods from Zip Files
1. Go to the "Mod Analysis" tab
2. Click "Browse" to select a mod zip file
3. Click "Analyze Mod" to get a detailed breakdown
4. Click "Auto-Add to Modlist" to automatically add the mod with categorization
5. The app will automatically categorize based on content analysis

### Analyzing Mod Files
1. Go to the "Mod Analysis" tab
2. Click "Browse" to select a mod zip file
3. Click "Analyze Mod" to get a detailed breakdown
4. The analysis will show:
   - All files in the mod
   - BepInEx compatibility
   - Manifest information (if available)
   - DLL files and configuration files
   - Summary statistics
   - Auto-categorization results

### AI-Enhanced Analysis
1. **Setup**: Ensure your local GPT4All server is running on `http://localhost:4891`
   - See `GPT4ALL_SETUP.md` for detailed setup instructions
2. **Status**: The app shows AI availability status (Available ✅ / Unavailable ❌)
3. After analyzing a mod, use the AI buttons:
   - **Generate AI Summary**: Get a comprehensive analysis with recommendations
   - **AI Category Suggestion**: Get AI-powered category recommendations
   - **AI Mod Recommendation**: Get INCLUDE/EXCLUDE recommendation based on your 2-player co-op goals
4. The AI analysis provides:
   - Detailed mod functionality explanation
   - Category suggestions with reasoning
   - **Modlist inclusion recommendations** (INCLUDE/EXCLUDE with reasoning)
   - Compatibility notes and requirements
   - Recommendations for your modlist
   - References from LocalDocs (if enabled)

**Note**: The app works perfectly without GPT4All - only AI features are disabled.

### Exporting Your Modlist
1. Go to the "Export Modlist" tab
2. Choose your preferred export format
3. Preview the output in the preview area
4. Click "Export Modlist" to save to a file

## File Structure

```
Valheim Modlist/
├── app.py                     # Main entry point
├── valheim_modlist_builder.py # Core application
├── requirements.txt           # Dependencies
├── README.md                 # This file
├── GPT4ALL_SETUP.md          # GPT4All setup guide
└── modlist_data.json        # Saved mod data (created automatically)
```

## Color Scheme

The application uses a beautiful earthy color palette:
- **Dark Forest Green** (#2F4F2F) - Main background
- **Beige** (#F5F5DC) - Text and entry fields
- **Saddle Brown** (#8B4513) - Accent color
- **Dark Olive Green** (#556B2F) - Secondary background
- **Sienna** (#A0522D) - Button colors

## Data Persistence

Your modlist data is automatically saved to `modlist_data.json` in the same directory as the application. This file is created automatically when you add your first mod and will persist between sessions.

## Tips for Mod Analysis

- **BepInEx mods** will be automatically detected if they contain BepInEx-related files
- **Manifest files** (manifest.json) will be parsed to extract mod information
- **DLL files** indicate code-based mods that modify game behavior
- **Configuration files** suggest the mod has customizable settings
- **Auto-categorization** analyzes mod names, descriptions, and file contents to intelligently categorize mods
- **Boss & Combat Overhaul**: Detects boss, encounter, roaming, affix, difficulty scaling, combat, CLLC keywords
- **Loot Overhaul**: Detects loot, drop, rarity, epic, legendary, chest, material, gem, weapon, enhanced keywords
- **Magic & Classes**: Detects magic, spell, class, ability, runic, skyheim, legend, power, magical keywords
- **Skills & Progression**: Detects skill, progression, level, profession, farming, attribute, runescape keywords
- **Gear & Customization**: Detects gear, armor, weapon, set, cosmetic, appearance, customization, pet keywords
- **Co-op Stability**: Detects server, multiplayer, coop, stability, dedicated, anti-cheat, performance keywords
- **Dependencies**: Detects frameworks, library packs, or required base mods

## Troubleshooting

- **Application won't start**: Make sure you have Python 3.6+ installed
- **Can't analyze zip files**: Ensure the file is a valid zip archive
- **Data not saving**: Check that the application has write permissions in its directory

## Future Enhancements

Potential features for future versions:
- Mod compatibility checking
- Automatic mod updates
- Integration with mod repositories
- Backup and restore functionality
- Mod load order management

---

**Enjoy building your perfect Valheim modlist!** 🏰⚔️ 