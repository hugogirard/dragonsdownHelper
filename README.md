# 🐉 Dragons Down Adventure Journal

A Streamlit web application for creating and managing character sheets for the Dragons Down Adventure tabletop game.

## Features

- **Character Management**: Create, save, and manage multiple character sheets
- **Repository Pattern**: Clean separation of data persistence logic (easy to migrate to MongoDB or other databases)
- **Auto-save**: Toggle auto-save functionality on/off
- **Character Naming**: Characters are automatically named with the first 4 letters + timestamp format
- **Comprehensive Tracking**:
  - Hero information (name, lineage, class, advantages)
  - Scenario and hero story
  - 30-line adventure journal
  - Hidden paths found with predefined tile connections
  - Discoveries (15 different types)

## Architecture

### Repository Pattern

The application uses a repository pattern for data persistence, making it easy to switch between different storage backends:

- **Current Implementation**: JSON file storage (`CharacterRepository`)
- **Future Ready**: MongoDB implementation stub included (`MongoCharacterRepository`)

```python
from repository import CharacterRepository

# Initialize repository
repo = CharacterRepository(storage_path="character_sheets")

# Save a character
repo.save(character_id, character_data)

# Get a character
character = repo.get(character_id)

# Delete a character
repo.delete(character_id)
```

### Project Structure

```
.
├── main.py                      # Main Streamlit application
├── repository/                  # Data persistence layer
│   ├── __init__.py
│   └── character_repository.py  # Repository implementation
├── character_sheets/            # JSON storage directory
├── test_repository.py          # Repository tests
├── pyproject.toml              # Project configuration
├── README.md                   # This file
└── run.sh                      # Quick start script
```

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
   - Check off hidden paths for each location and tile side
   - Mark discoveries
   - Write journal entries (lines 1-30)
4. Click **"Save Character"** to save your sheet

### Hidden Paths System

Each location has predefined hidden path connections across two tile sides:

**Example - Ancient Hole (Caves):**
- Tile Side 1: ☐ 1-6
- Tile Side 2: ☐ 1-6, ☐ 3-4, ☐ 5-6

Simply check the boxes for the paths you've discovered during your adventure.

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

Character data is stored as JSON files with the following structure:

- Hero information (name, lineage, class, advantages)
- Adventure details (scenario, story)
- Hidden paths (specific tile connections per location)
- Discoveries (boolean flags for each discovery type)
- Journal entries (array of 30 strings)
- Timestamps (created and last modified)

## Future Database Migration

The repository pattern makes it easy to migrate to a NoSQL database like MongoDB:

1. **Implement MongoDB Repository**: Complete the `MongoCharacterRepository` class in `repository/character_repository.py`
2. **Update Initialization**: Change the repository initialization in `main.py`:
   ```python
   # From:
   repo = CharacterRepository(storage_path="character_sheets")
   
   # To:
   repo = MongoCharacterRepository(
       connection_string="mongodb://localhost:27017",
       database_name="dragonsdown"
   )
   ```
3. **No Other Changes Needed**: The rest of the application code remains the same!

### Benefits of Repository Pattern:
- ✅ Separation of concerns
- ✅ Easy to test
- ✅ Easy to swap implementations
- ✅ No business logic changes when switching databases

## Testing the Repository

Run the repository tests:
```bash
python test_repository.py
```

This will test all repository operations (save, get, update, delete, rename, etc.)

## Tips

- Use the journal section to track your adventure chronologically
- Check off tiles as you explore different locations
- Record important discoveries to remember what you've found
- The character sheet automatically updates the sidebar name when you change the hero name and save

## Version

Version 1.0 - November 2025
