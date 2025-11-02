import streamlit as st
from datetime import datetime
from repository import CharacterRepository

# Set page configuration
st.set_page_config(
    page_title="Dragons Down Adventure Journal",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize repository
@st.cache_resource
def get_repository():
    """Get or create the character repository instance"""
    return CharacterRepository(storage_path="character_sheets")

# Initialize session state
if 'characters' not in st.session_state:
    repo = get_repository()
    st.session_state.characters = repo.get_all()

if 'current_character' not in st.session_state:
    st.session_state.current_character = None

if 'autosave' not in st.session_state:
    st.session_state.autosave = False

if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False


def save_character(char_id, char_data):
    """Save character data using repository"""
    repo = get_repository()
    if repo.save(char_id, char_data):
        st.session_state.characters[char_id] = char_data
        return True
    return False


def delete_character(char_id):
    """Delete character using repository"""
    repo = get_repository()
    if repo.delete(char_id):
        if char_id in st.session_state.characters:
            del st.session_state.characters[char_id]
        return True
    return False


def rename_character(old_char_id, new_char_id, char_data):
    """Rename character using repository"""
    repo = get_repository()
    if repo.rename(old_char_id, new_char_id):
        # Update session state
        if old_char_id in st.session_state.characters:
            del st.session_state.characters[old_char_id]
        st.session_state.characters[new_char_id] = char_data
        return True
    return False


def create_character_id(hero_name):
    """Create character ID from hero name and date"""
    name_prefix = hero_name[:4] if hero_name else "CHAR"
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name_prefix}_{date_str}"


def get_empty_character():
    """Return empty character template"""
    return {
        'hero_name': '',
        'lineage_and_class': '',
        'advantages': '',
        'scenario': '',
        'hero_story': '',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'hidden_paths': {
            'Ancient Hole': {'1-6_s1': False, '1-6_s2': False, '3-4_s2': False, '5-6_s2': False},
            'Black Caves': {'3-4_s1': False, '1-6_s2': False, '3-4_s2': False, '5-6_s2': False},
            'Dark Passes': {'1-4_s1': False, '3-6_s1': False, '1-4_s2': False, '2-3_s2': False, '3-6_s2': False},
            'Forlorn Tunnel': {'1-5_s1': False, '2-3_s1': False, '1-5_s2': False, '2-3_s2': False, '2-6_s2': False, '4-5_s2': False},
            'Secret Dens': {'5-6_s1': False, '2-3_s2': False},
            'Barriers': {'1-3_s1': False, '1-3_s2': False, '1-6_s2': False},
            'High Pass': {'1-5_s1': False, '1-5_s2': False, '3-4_s2': False},
            'Lonely Mountains': {'2-5_s1': False, '2-5_s2': False, '3-4_s2': False},
            'Narrow Ridges': {'5-6_s1': False, '3-4_s2': False, '5-6_s2': False},
            'Tri-Peaks': {'1-5_s1': False, '4-5_s1': False, '2-6_s2': False, '4-5_s2': False},
            'Deep Woods': {'1-3_s1': False, '1-6_s2': False},
            'Elder Woods': {'4-6_s1': False, '3-4_s2': False},
            'Mirky Woods': {'2-6_s1': False, '1-6_s2': False},
            'Oakwood': {'1-6_s1': False, '1-3_s2': False},
            'Timberlands': {'3-6_s1': False, '1-4_s2': False},
            'Flatlands': {'1-2_s1': False, '5-6_s2': False},
            'Grassy Plains': {'4-5_s1': False, '3-4_s2': False},
            'The Meadows': {'1-5_s1': False, '2-3_s2': False},
            'Twisted Steppe': {'1-6_s1': False, '4-6_s2': False},
            'Unbroken Lands': {'1-3_s1': False, '2-4_s2': False},
            'Decayed Swamp': {'5-6_s1': False, '4-5_s2': False},
            'Foul Swamp': {'5-6_s1': False, '1-3_s2': False},
            'Moorland': {'2-4_s1': False, '4-6_s2': False},
            'Putrid Waters': {'2-5_s1': False, '4-6_s2': False},
            'Quiet Bog': {'2-3_s1': False, '5-6_s2': False},
        },
        'discoveries': {
            'altar': False, 'crypt': False, 'hoard': False, 'secret_cache': False, 'wrecked_wagons': False,
            'catacombs': False, 'grotto': False, 'lost_battalion': False, 'shrine': False, 'deserted_ruins': False,
            'chamber': False, 'hideout': False, 'monolith': False, 'trove': False, 'forgotten_city': False,
        },
        'journal_entries': [''] * 30
    }


def render_character_form(char_data, char_id=None):
    """Render the character sheet form"""
    
    st.title("🐉 Dragons Down Adventure Journal")
    
    # Autosave toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        autosave = st.checkbox("Auto-save", value=st.session_state.autosave, key=f"autosave_{char_id}")
        st.session_state.autosave = autosave
    
    # Character Info Section
    st.header("Character Information")
    hero_name = st.text_input("Hero Name", value=char_data.get('hero_name', ''), key=f"hero_name_{char_id}")
    lineage_class = st.text_input("Lineage and Class", value=char_data.get('lineage_and_class', ''), key=f"lineage_{char_id}")
    advantages = st.text_area("Advantages", value=char_data.get('advantages', ''), height=100, key=f"advantages_{char_id}")
    
    st.header("Adventure Details")
    scenario = st.text_area("Scenario", value=char_data.get('scenario', ''), height=100, key=f"scenario_{char_id}")
    hero_story = st.text_area("Hero Story", value=char_data.get('hero_story', ''), height=150, key=f"story_{char_id}")
    
    # Journal Entries
    st.header("Adventure Journal")
    st.caption("Track your journey (Lines 1-30)")
    
    journal_entries = char_data.get('journal_entries', [''] * 30)
    
    # Display journal in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lines 1-15")
        for i in range(15):
            journal_entries[i] = st.text_input(
                f"Line {i+1}", 
                value=journal_entries[i], 
                key=f"journal_{i}_{char_id}",
                label_visibility="collapsed"
            )
    
    with col2:
        st.subheader("Lines 16-30")
        for i in range(15, 30):
            journal_entries[i] = st.text_input(
                f"Line {i+1}", 
                value=journal_entries[i], 
                key=f"journal_{i}_{char_id}",
                label_visibility="collapsed"
            )
    
    # Hidden Paths Section
    st.header("Hidden Paths Found")
    st.caption("Check the boxes for the tile connections you've discovered")
    
    hidden_paths = char_data.get('hidden_paths', get_empty_character()['hidden_paths'])
    
    # Define the hidden path configurations based on the image
    hidden_path_config = {
        'Caves': {
            'Ancient Hole': {'Tile Side 1': ['1-6'], 'Tile Side 2': ['1-6', '3-4', '5-6']},
            'Black Caves': {'Tile Side 1': ['3-4'], 'Tile Side 2': ['1-6', '3-4', '5-6']},
            'Dark Passes': {'Tile Side 1': ['1-4', '3-6'], 'Tile Side 2': ['1-4', '2-3', '3-6']},
            'Forlorn Tunnel': {'Tile Side 1': ['1-5', '2-3'], 'Tile Side 2': ['1-5', '2-3', '2-6', '4-5']},
            'Secret Dens': {'Tile Side 1': ['5-6'], 'Tile Side 2': ['2-3']},
        },
        'Mountains': {
            'Barriers': {'Tile Side 1': ['1-3'], 'Tile Side 2': ['1-3', '1-6']},
            'High Pass': {'Tile Side 1': ['1-5'], 'Tile Side 2': ['1-5', '3-4']},
            'Lonely Mountains': {'Tile Side 1': ['2-5'], 'Tile Side 2': ['2-5', '3-4']},
            'Narrow Ridges': {'Tile Side 1': ['5-6'], 'Tile Side 2': ['3-4', '5-6']},
            'Tri-Peaks': {'Tile Side 1': ['1-5', '4-5'], 'Tile Side 2': ['2-6', '4-5']},
        },
        'Woods': {
            'Deep Woods': {'Tile Side 1': ['1-3'], 'Tile Side 2': ['1-6']},
            'Elder Woods': {'Tile Side 1': ['4-6'], 'Tile Side 2': ['3-4']},
            'Mirky Woods': {'Tile Side 1': ['2-6'], 'Tile Side 2': ['1-6']},
            'Oakwood': {'Tile Side 1': ['1-6'], 'Tile Side 2': ['1-3']},
            'Timberlands': {'Tile Side 1': ['3-6'], 'Tile Side 2': ['1-4']},
        },
        'Plains': {
            'Flatlands': {'Tile Side 1': ['1-2'], 'Tile Side 2': ['5-6']},
            'Grassy Plains': {'Tile Side 1': ['4-5'], 'Tile Side 2': ['3-4']},
            'The Meadows': {'Tile Side 1': ['1-5'], 'Tile Side 2': ['2-3']},
            'Twisted Steppe': {'Tile Side 1': ['1-6'], 'Tile Side 2': ['4-6']},
            'Unbroken Lands': {'Tile Side 1': ['1-3'], 'Tile Side 2': ['2-4']},
        },
        'Swamps': {
            'Decayed Swamp': {'Tile Side 1': ['5-6'], 'Tile Side 2': ['4-5']},
            'Foul Swamp': {'Tile Side 1': ['5-6'], 'Tile Side 2': ['1-3']},
            'Moorland': {'Tile Side 1': ['2-4'], 'Tile Side 2': ['4-6']},
            'Putrid Waters': {'Tile Side 1': ['2-5'], 'Tile Side 2': ['4-6']},
            'Quiet Bog': {'Tile Side 1': ['2-3'], 'Tile Side 2': ['5-6']},
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Caves
        st.subheader("🏔️ Caves")
        for location, sides in hidden_path_config['Caves'].items():
            st.markdown(f"**{location}**")
            cols = st.columns(2)
            
            # Tile Side 1
            with cols[0]:
                st.caption("Tile Side 1")
                for path in sides['Tile Side 1']:
                    key = f"{path}_s1"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
            
            # Tile Side 2
            with cols[1]:
                st.caption("Tile Side 2")
                for path in sides['Tile Side 2']:
                    key = f"{path}_s2"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
        
        # Mountains
        st.subheader("⛰️ Mountains")
        for location, sides in hidden_path_config['Mountains'].items():
            st.markdown(f"**{location}**")
            cols = st.columns(2)
            
            # Tile Side 1
            with cols[0]:
                st.caption("Tile Side 1")
                for path in sides['Tile Side 1']:
                    key = f"{path}_s1"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
            
            # Tile Side 2
            with cols[1]:
                st.caption("Tile Side 2")
                for path in sides['Tile Side 2']:
                    key = f"{path}_s2"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
        
        # Woods
        st.subheader("🌲 Woods")
        for location, sides in hidden_path_config['Woods'].items():
            st.markdown(f"**{location}**")
            cols = st.columns(2)
            
            # Tile Side 1
            with cols[0]:
                st.caption("Tile Side 1")
                for path in sides['Tile Side 1']:
                    key = f"{path}_s1"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
            
            # Tile Side 2
            with cols[1]:
                st.caption("Tile Side 2")
                for path in sides['Tile Side 2']:
                    key = f"{path}_s2"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
    
    with col2:
        # Plains
        st.subheader("🌾 Plains")
        for location, sides in hidden_path_config['Plains'].items():
            st.markdown(f"**{location}**")
            cols = st.columns(2)
            
            # Tile Side 1
            with cols[0]:
                st.caption("Tile Side 1")
                for path in sides['Tile Side 1']:
                    key = f"{path}_s1"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
            
            # Tile Side 2
            with cols[1]:
                st.caption("Tile Side 2")
                for path in sides['Tile Side 2']:
                    key = f"{path}_s2"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
        
        # Swamps
        st.subheader("🌿 Swamps")
        for location, sides in hidden_path_config['Swamps'].items():
            st.markdown(f"**{location}**")
            cols = st.columns(2)
            
            # Tile Side 1
            with cols[0]:
                st.caption("Tile Side 1")
                for path in sides['Tile Side 1']:
                    key = f"{path}_s1"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )
            
            # Tile Side 2
            with cols[1]:
                st.caption("Tile Side 2")
                for path in sides['Tile Side 2']:
                    key = f"{path}_s2"
                    hidden_paths[location][key] = st.checkbox(
                        path,
                        value=hidden_paths.get(location, {}).get(key, False),
                        key=f"hp_{location}_{key}_{char_id}"
                    )


    
    # Discoveries Section
    st.header("Discoveries")
    discoveries = char_data.get('discoveries', get_empty_character()['discoveries'])
    
    cols = st.columns(5)
    discovery_items = list(discoveries.keys())
    
    for idx, discovery in enumerate(discovery_items):
        col_idx = idx % 5
        discoveries[discovery] = cols[col_idx].checkbox(
            discovery.replace('_', ' ').title(),
            value=discoveries.get(discovery, False),
            key=f"discovery_{discovery}_{char_id}"
        )
    
    # Update character data
    updated_char_data = {
        'hero_name': hero_name,
        'lineage_and_class': lineage_class,
        'advantages': advantages,
        'scenario': scenario,
        'hero_story': hero_story,
        'date': char_data.get('date', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'hidden_paths': hidden_paths,
        'discoveries': discoveries,
        'journal_entries': journal_entries
    }
    
    # Auto-save
    if autosave and char_id:
        if updated_char_data != char_data:
            save_character(char_id, updated_char_data)
            st.caption("✅ Auto-saved")
    
    # Save Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("💾 Save Character", type="primary", use_container_width=True):
            if char_id:
                # Check if hero name changed
                old_char_data = st.session_state.characters.get(char_id, {})
                if hero_name != old_char_data.get('hero_name', ''):
                    # Create new ID with updated name
                    new_char_id = create_character_id(hero_name)
                    
                    # Save with new ID and delete old
                    if save_character(new_char_id, updated_char_data):
                        delete_character(char_id)
                        st.session_state.current_character = new_char_id
                        st.success(f"✅ Character saved as: {new_char_id}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save character")
                else:
                    if save_character(char_id, updated_char_data):
                        st.success("✅ Character saved successfully!")
                    else:
                        st.error("❌ Failed to save character")
            else:
                # New character
                new_char_id = create_character_id(hero_name)
                if save_character(new_char_id, updated_char_data):
                    st.session_state.current_character = new_char_id
                    st.session_state.show_create_form = False
                    st.success(f"✅ Character created: {new_char_id}")
                    st.rerun()
                else:
                    st.error("❌ Failed to create character")
    
    with col2:
        if char_id and st.button("🗑️ Delete Character", use_container_width=True):
            if delete_character(char_id):
                st.session_state.current_character = None
                st.success("✅ Character deleted!")
                st.rerun()
            else:
                st.error("❌ Failed to delete character")


def main():
    # Sidebar
    with st.sidebar:
        st.title("📜 Character Sheets")
        
        # Create New Character Button
        if st.button("➕ Create New Character", type="primary", use_container_width=True):
            st.session_state.show_create_form = True
            st.session_state.current_character = None
            st.rerun()
        
        st.markdown("---")
        
        # List existing characters
        if st.session_state.characters:
            st.subheader("Your Characters")
            for char_id, char_data in st.session_state.characters.items():
                hero_name = char_data.get('hero_name', 'Unnamed')
                display_name = hero_name[:4] if hero_name else char_id[:4]
                
                # Extract date from char_id
                date_part = char_id.split('_', 1)[1] if '_' in char_id else ''
                label = f"{display_name}_{date_part}" if date_part else display_name
                
                if st.button(label, key=f"btn_{char_id}", use_container_width=True):
                    st.session_state.current_character = char_id
                    st.session_state.show_create_form = False
                    st.rerun()
        else:
            st.info("No characters yet. Create your first character!")
        
        st.markdown("---")
        st.caption("Dragons Down Adventure Journal v1.0")
    
    # Main content area
    if st.session_state.show_create_form:
        render_character_form(get_empty_character())
    elif st.session_state.current_character:
        char_id = st.session_state.current_character
        char_data = st.session_state.characters.get(char_id, get_empty_character())
        render_character_form(char_data, char_id)
    else:
        st.title("🐉 Welcome to Dragons Down Adventure Journal")
        st.markdown("""
        ### Getting Started
        
        Click **"Create New Character"** in the sidebar to begin your adventure!
        
        #### Features:
        - 📝 Create and manage multiple character sheets
        - 💾 Manual save or auto-save functionality
        - 🗺️ Track tiles visited across 5 terrain types
        - 🔍 Record hidden paths and discoveries
        - 📖 Keep a 30-line adventure journal
        - 🏷️ Characters automatically named with first 4 letters + timestamp
        
        Your adventure awaits!
        """)
        
        # Display example image if available
        st.image("https://via.placeholder.com/800x600?text=Dragons+Down+Adventure+Journal", 
                caption="Example Character Sheet")


if __name__ == "__main__":
    main()

