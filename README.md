# 🐉 Dragons Down Adventure Journal

A Streamlit web application for creating and managing character sheets for the Dragons Down Adventure tabletop game.

## Features

- **Character Management**: Create, save, and manage multiple character sheets
- **Auto-save**: Toggle auto-save functionality on/off
- **Character Naming**: Characters are automatically named with the first 4 letters + timestamp format
- **Comprehensive Tracking**:
  - Hero information (name, lineage, class, advantages)
  - Scenario and hero story
  - 30-line adventure journal
  - Tiles visited across 5 terrain types (Caves, Mountains, Woods, Plains, Swamps)
  - Hidden paths found
  - Discoveries (15 different types)

## Installation

1. Install dependencies:
```bash
pip install streamlit pandas
```

Or using the project file:
```bash
pip install -e .
```

## Running the Application

Run the Streamlit app with:
```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage

### Creating a New Character

1. Click the **"Create New Character"** button in the left sidebar
2. Fill in your character information:
   - Hero Name
   - Lineage and Class
   - Advantages
   - Scenario
   - Hero Story
3. Track your adventure:
   - Check off tiles visited in different terrains
   - Record hidden paths found
   - Mark discoveries
   - Write journal entries (lines 1-30)
4. Click **"Save Character"** to save your sheet

### Auto-save Feature

- Toggle the **"Auto-save"** checkbox at the top of the form
- When enabled, changes are automatically saved as you type
- When disabled, you must manually click the save button

### Character Naming

- Characters are saved with format: `[FIRST_4_LETTERS_OF_NAME]_[DATE_TIMESTAMP]`
- Example: If hero name is "Aragorn", saved as `Arag_20251102_143022`
- In the sidebar, only the first 4 characters and date are shown

### Managing Characters

- All saved characters appear in the left sidebar
- Click on any character name to load and edit that sheet
- Use the **"Delete Character"** button to remove a character
- Character files are stored in the `character_sheets/` directory as JSON files

## Data Structure

Character data is stored as JSON files in the `character_sheets/` directory with the following structure:

- Hero information (name, lineage, class, advantages)
- Adventure details (scenario, story)
- Tiles visited (organized by terrain type and location)
- Hidden paths (by terrain type)
- Discoveries (boolean flags)
- Journal entries (array of 30 strings)
- Timestamps (created and last modified)

## File Structure

```
.
├── main.py                 # Main Streamlit application
├── pyproject.toml         # Project configuration and dependencies
├── README.md              # This file
└── character_sheets/      # Directory for saved character JSON files
```

## Tips

- Use the journal section to track your adventure chronologically
- Check off tiles as you explore different locations
- Record important discoveries to remember what you've found
- The character sheet automatically updates the sidebar name when you change the hero name and save

## Version

Version 1.0 - November 2025
