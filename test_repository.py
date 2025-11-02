"""
Test file for Character Repository
Demonstrates the repository pattern usage
"""
from repository import CharacterRepository
from datetime import datetime


def test_character_repository():
    """Test the character repository functionality"""
    
    # Initialize repository
    repo = CharacterRepository(storage_path="test_character_sheets")
    
    # Create a test character
    test_character = {
        'hero_name': 'TestHero',
        'lineage_and_class': 'Elf Warrior',
        'advantages': 'Strong and brave',
        'scenario': 'Test scenario',
        'hero_story': 'A brave hero',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'hidden_paths': {},
        'discoveries': {},
        'journal_entries': [''] * 30
    }
    
    # Test save
    print("Testing save...")
    char_id = "Test_20251102_120000"
    assert repo.save(char_id, test_character), "Save failed"
    print("✓ Save successful")
    
    # Test get
    print("\nTesting get...")
    loaded_char = repo.get(char_id)
    assert loaded_char is not None, "Get failed"
    assert loaded_char['hero_name'] == 'TestHero', "Character data mismatch"
    print("✓ Get successful")
    
    # Test exists
    print("\nTesting exists...")
    assert repo.exists(char_id), "Exists check failed"
    print("✓ Exists check successful")
    
    # Test get_all
    print("\nTesting get_all...")
    all_chars = repo.get_all()
    assert char_id in all_chars, "Get all failed"
    print(f"✓ Get all successful - found {len(all_chars)} character(s)")
    
    # Test list_character_ids
    print("\nTesting list_character_ids...")
    char_ids = repo.list_character_ids()
    assert char_id in char_ids, "List IDs failed"
    print(f"✓ List IDs successful - found {len(char_ids)} ID(s)")
    
    # Test update
    print("\nTesting update...")
    test_character['hero_name'] = 'UpdatedHero'
    assert repo.update(char_id, test_character), "Update failed"
    updated_char = repo.get(char_id)
    assert updated_char['hero_name'] == 'UpdatedHero', "Update data mismatch"
    print("✓ Update successful")
    
    # Test rename
    print("\nTesting rename...")
    new_char_id = "Upda_20251102_120001"
    assert repo.rename(char_id, new_char_id), "Rename failed"
    assert repo.exists(new_char_id), "New character ID not found after rename"
    assert not repo.exists(char_id), "Old character ID still exists after rename"
    print("✓ Rename successful")
    
    # Test delete
    print("\nTesting delete...")
    assert repo.delete(new_char_id), "Delete failed"
    assert not repo.exists(new_char_id), "Character still exists after delete"
    print("✓ Delete successful")
    
    print("\n✅ All tests passed!")
    
    # Clean up test directory
    import shutil
    shutil.rmtree("test_character_sheets", ignore_errors=True)
    print("✓ Test cleanup complete")


if __name__ == "__main__":
    test_character_repository()
