"""
Character Repository
Handles persistence of character data using JSON files.
This implementation can be easily replaced with a NoSQL database (MongoDB, etc.) later.
"""
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime


class CharacterRepository:
    """Repository for managing character data persistence"""
    
    def __init__(self, storage_path: str = "character_sheets"):
        """
        Initialize the character repository
        
        Args:
            storage_path: Directory path where character JSON files will be stored
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
    
    def save(self, character_id: str, character_data: Dict) -> bool:
        """
        Save a character to storage
        
        Args:
            character_id: Unique identifier for the character
            character_data: Dictionary containing all character information
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            filepath = self.storage_path / f"{character_id}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(character_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving character {character_id}: {e}")
            return False
    
    def get(self, character_id: str) -> Optional[Dict]:
        """
        Retrieve a character by ID
        
        Args:
            character_id: Unique identifier for the character
            
        Returns:
            Dict: Character data if found, None otherwise
        """
        try:
            filepath = self.storage_path / f"{character_id}.json"
            if not filepath.exists():
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading character {character_id}: {e}")
            return None
    
    def get_all(self) -> Dict[str, Dict]:
        """
        Retrieve all characters from storage
        
        Returns:
            Dict: Dictionary mapping character IDs to character data
        """
        characters = {}
        try:
            for filepath in self.storage_path.glob("*.json"):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        char_data = json.load(f)
                        characters[filepath.stem] = char_data
                except Exception as e:
                    print(f"Error loading character from {filepath}: {e}")
                    continue
        except Exception as e:
            print(f"Error scanning character directory: {e}")
        
        return characters
    
    def delete(self, character_id: str) -> bool:
        """
        Delete a character from storage
        
        Args:
            character_id: Unique identifier for the character
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            filepath = self.storage_path / f"{character_id}.json"
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting character {character_id}: {e}")
            return False
    
    def exists(self, character_id: str) -> bool:
        """
        Check if a character exists in storage
        
        Args:
            character_id: Unique identifier for the character
            
        Returns:
            bool: True if character exists, False otherwise
        """
        filepath = self.storage_path / f"{character_id}.json"
        return filepath.exists()
    
    def list_character_ids(self) -> List[str]:
        """
        Get a list of all character IDs
        
        Returns:
            List[str]: List of character IDs
        """
        try:
            return [f.stem for f in self.storage_path.glob("*.json")]
        except Exception as e:
            print(f"Error listing character IDs: {e}")
            return []
    
    def update(self, character_id: str, character_data: Dict) -> bool:
        """
        Update an existing character (alias for save)
        
        Args:
            character_id: Unique identifier for the character
            character_data: Dictionary containing updated character information
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        return self.save(character_id, character_data)
    
    def rename(self, old_character_id: str, new_character_id: str) -> bool:
        """
        Rename a character (useful when hero name changes)
        
        Args:
            old_character_id: Current character ID
            new_character_id: New character ID
            
        Returns:
            bool: True if rename was successful, False otherwise
        """
        try:
            old_filepath = self.storage_path / f"{old_character_id}.json"
            new_filepath = self.storage_path / f"{new_character_id}.json"
            
            if not old_filepath.exists():
                return False
            
            if new_filepath.exists():
                print(f"Character {new_character_id} already exists")
                return False
            
            # Read the old file
            with open(old_filepath, 'r', encoding='utf-8') as f:
                char_data = json.load(f)
            
            # Save to new location
            with open(new_filepath, 'w', encoding='utf-8') as f:
                json.dump(char_data, f, indent=2, ensure_ascii=False)
            
            # Delete old file
            old_filepath.unlink()
            return True
        except Exception as e:
            print(f"Error renaming character from {old_character_id} to {new_character_id}: {e}")
            return False
    
    def get_storage_path(self) -> Path:
        """
        Get the storage path for character files
        
        Returns:
            Path: Path object for the storage directory
        """
        return self.storage_path


# Future implementation stub for MongoDB
class MongoCharacterRepository:
    """
    Future implementation for MongoDB storage
    This will implement the same interface as CharacterRepository
    """
    
    def __init__(self, connection_string: str, database_name: str = "dragonsdown"):
        """
        Initialize MongoDB repository
        
        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        raise NotImplementedError("MongoDB repository not yet implemented")
        # Future implementation:
        # self.client = MongoClient(connection_string)
        # self.db = self.client[database_name]
        # self.collection = self.db.characters
    
    def save(self, character_id: str, character_data: Dict) -> bool:
        raise NotImplementedError("MongoDB repository not yet implemented")
    
    def get(self, character_id: str) -> Optional[Dict]:
        raise NotImplementedError("MongoDB repository not yet implemented")
    
    def get_all(self) -> Dict[str, Dict]:
        raise NotImplementedError("MongoDB repository not yet implemented")
    
    def delete(self, character_id: str) -> bool:
        raise NotImplementedError("MongoDB repository not yet implemented")
    
    def exists(self, character_id: str) -> bool:
        raise NotImplementedError("MongoDB repository not yet implemented")
    
    def list_character_ids(self) -> List[str]:
        raise NotImplementedError("MongoDB repository not yet implemented")
    
    def update(self, character_id: str, character_data: Dict) -> bool:
        raise NotImplementedError("MongoDB repository not yet implemented")
    
    def rename(self, old_character_id: str, new_character_id: str) -> bool:
        raise NotImplementedError("MongoDB repository not yet implemented")
