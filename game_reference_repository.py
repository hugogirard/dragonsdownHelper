"""
Game Reference Repository - Handles loading and querying game reference data
"""
import json
import os
from typing import List, Dict, Optional


class GameReferenceRepository:
    """Repository for managing game reference data from JSON files"""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        self._lineages = None
        self._classes = None
        self._spells = None
        self._treasures = None
    
    def _load_json(self, filename: str) -> Dict:
        """Load JSON file from data directory"""
        filepath = os.path.join(self.data_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filename} not found at {filepath}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding {filename}: {e}")
            return {}
    
    # Lineages Methods
    def get_all_lineages(self) -> List[Dict]:
        """Get all lineages"""
        if self._lineages is None:
            data = self._load_json("lineages.json")
            self._lineages = data.get("lineages", [])
        return self._lineages
    
    def get_lineage_by_id(self, lineage_id: str) -> Optional[Dict]:
        """Get a specific lineage by ID"""
        lineages = self.get_all_lineages()
        return next((l for l in lineages if l["id"] == lineage_id), None)
    
    def search_lineages(self, query: str) -> List[Dict]:
        """Search lineages by name or description"""
        lineages = self.get_all_lineages()
        query_lower = query.lower()
        return [
            l for l in lineages 
            if query_lower in l["name"].lower() 
            or query_lower in l["description"].lower()
            or query_lower in l["advantage"].lower()
        ]
    
    # Classes Methods
    def get_all_classes(self) -> List[Dict]:
        """Get all classes"""
        if self._classes is None:
            data = self._load_json("classes.json")
            self._classes = data.get("classes", [])
        return self._classes
    
    def get_class_by_id(self, class_id: str) -> Optional[Dict]:
        """Get a specific class by ID"""
        classes = self.get_all_classes()
        return next((c for c in classes if c["id"] == class_id), None)
    
    def search_classes(self, query: str) -> List[Dict]:
        """Search classes by name or description"""
        classes = self.get_all_classes()
        query_lower = query.lower()
        return [
            c for c in classes 
            if query_lower in c["name"].lower() 
            or query_lower in c["description"].lower()
            or query_lower in c["advantage"].lower()
        ]
    
    # Spells Methods
    def get_all_spells(self) -> List[Dict]:
        """Get all spells"""
        if self._spells is None:
            data = self._load_json("spells.json")
            self._spells = data.get("spells", [])
        return self._spells
    
    def get_spell_by_id(self, spell_id: str) -> Optional[Dict]:
        """Get a specific spell by ID"""
        spells = self.get_all_spells()
        return next((s for s in spells if s["id"] == spell_id), None)
    
    def get_spells_by_color(self, color: str) -> List[Dict]:
        """Get all spells of a specific color"""
        spells = self.get_all_spells()
        return [s for s in spells if s["color"].lower() == color.lower()]
    
    def get_spell_colors(self) -> List[str]:
        """Get list of all unique spell colors"""
        spells = self.get_all_spells()
        colors = set(s["color"] for s in spells)
        # Return in specific order
        color_order = ["Universal", "Black", "Blue", "Gray", "Green", "Purple", "White", "Yellow"]
        return [c for c in color_order if c in colors]
    
    def search_spells(self, query: str, color: Optional[str] = None) -> List[Dict]:
        """Search spells by name or description, optionally filtered by color"""
        spells = self.get_all_spells()
        query_lower = query.lower()
        
        results = [
            s for s in spells 
            if query_lower in s["name"].lower() 
            or query_lower in s["description"].lower()
        ]
        
        if color:
            results = [s for s in results if s["color"].lower() == color.lower()]
        
        return results
    
    # Treasures Methods
    def get_all_treasures(self) -> List[Dict]:
        """Get all treasures"""
        if self._treasures is None:
            data = self._load_json("treasures.json")
            self._treasures = data.get("treasures", [])
        return self._treasures
    
    def get_treasure_by_id(self, treasure_id: str) -> Optional[Dict]:
        """Get a specific treasure by ID"""
        treasures = self.get_all_treasures()
        return next((t for t in treasures if t["id"] == treasure_id), None)
    
    def get_treasures_by_type(self, treasure_type: str) -> List[Dict]:
        """Get all treasures of a specific type"""
        treasures = self.get_all_treasures()
        return [t for t in treasures if t["type"].lower() == treasure_type.lower()]
    
    def get_treasures_by_rarity(self, rarity: str) -> List[Dict]:
        """Get all treasures of a specific rarity"""
        treasures = self.get_all_treasures()
        return [t for t in treasures if t["rarity"].lower() == rarity.lower()]
    
    def get_treasure_types(self) -> List[str]:
        """Get list of all unique treasure types"""
        treasures = self.get_all_treasures()
        return sorted(list(set(t["type"] for t in treasures)))
    
    def get_treasure_rarities(self) -> List[str]:
        """Get list of all unique treasure rarities"""
        treasures = self.get_all_treasures()
        rarities = set(t["rarity"] for t in treasures)
        # Return in specific order
        rarity_order = ["Legendary", "Epic", "Valuable", "Standard", "One-Time"]
        return [r for r in rarity_order if r in rarities]
    
    def search_treasures(self, query: str, treasure_type: Optional[str] = None, 
                        rarity: Optional[str] = None) -> List[Dict]:
        """Search treasures by name or description, with optional filters"""
        treasures = self.get_all_treasures()
        query_lower = query.lower()
        
        results = [
            t for t in treasures 
            if query_lower in t["name"].lower() 
            or query_lower in t["description"].lower()
        ]
        
        if treasure_type:
            results = [t for t in results if t["type"].lower() == treasure_type.lower()]
        
        if rarity:
            results = [t for t in results if t["rarity"].lower() == rarity.lower()]
        
        return results
    
    # Utility Methods
    def get_stats(self) -> Dict:
        """Get statistics about the game reference data"""
        return {
            "lineages": len(self.get_all_lineages()),
            "classes": len(self.get_all_classes()),
            "spells": len(self.get_all_spells()),
            "treasures": len(self.get_all_treasures()),
            "spell_colors": len(self.get_spell_colors()),
            "treasure_types": len(self.get_treasure_types())
        }
