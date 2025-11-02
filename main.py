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
    st.session_state.autosave = True  # Auto-save enabled by default

if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False

if 'show_realm_builder' not in st.session_state:
    st.session_state.show_realm_builder = False

if 'last_save_time' not in st.session_state:
    st.session_state.last_save_time = None

if 'pending_save' not in st.session_state:
    st.session_state.pending_save = False


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


def get_all_tiles_by_land_pack():
    """Return all tiles organized by land pack"""
    return {
        'Caves': [
            'Ancient Hole',
            'Black Caves',
            'Dark Passes',
            'Forlorn Tunnel',
            'Secret Dens'
        ],
        'Mountains': [
            'Barriers',
            'High Pass',
            'Lonely Mountains',
            'Narrow Ridges',
            'Tri-Peaks'
        ],
        'Woods': [
            'Deep Woods',
            'Elder Woods',
            'Mirky Woods',
            'Oakwood',
            'Timberlands'
        ],
        'Plains': [
            'Flatlands',
            'Grassy Plains',
            'The Meadows',
            'Twisted Steppe',
            'Unbroken Lands'
        ],
        'Swamps': [
            'Decayed Swamp',
            'Foul Swamp',
            'Moorland',
            'Putrid Waters',
            'Quiet Bog'
        ]
    }


def generate_realm_tiles(selected_land_packs):
    """
    Generate a randomized list of tiles from selected land packs
    
    Args:
        selected_land_packs: List of land pack names
        
    Returns:
        List of randomized tile names
    """
    import random
    
    all_tiles = get_all_tiles_by_land_pack()
    realm_tiles = []
    
    # Collect all tiles from selected land packs
    for land_pack in selected_land_packs:
        if land_pack in all_tiles:
            realm_tiles.extend(all_tiles[land_pack])
    
    # Randomize the order
    random.shuffle(realm_tiles)
    
    return realm_tiles


def render_realm_builder():
    """Render the realm builder interface"""
    st.title("🏰 Create New Realm")
    
    st.markdown("""
    ### Build Your Adventure Realm
    
    Select between 2 and 5 land packs to create your realm. 
    The tiles will be randomly ordered to create a unique adventure experience!
    """)
    
    st.markdown("---")
    
    # Land pack selection
    st.subheader("Select Land Packs (2-5)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        caves = st.checkbox("🏔️ Caves (5 tiles)", key="realm_caves")
        mountains = st.checkbox("⛰️ Mountains (5 tiles)", key="realm_mountains")
    
    with col2:
        woods = st.checkbox("🌲 Woods (5 tiles)", key="realm_woods")
        plains = st.checkbox("🌾 Plains (5 tiles)", key="realm_plains")
    
    with col3:
        swamps = st.checkbox("🌿 Swamps (5 tiles)", key="realm_swamps")
    
    # Collect selected land packs
    selected_packs = []
    if caves:
        selected_packs.append('Caves')
    if mountains:
        selected_packs.append('Mountains')
    if woods:
        selected_packs.append('Woods')
    if plains:
        selected_packs.append('Plains')
    if swamps:
        selected_packs.append('Swamps')
    
    # Validation
    num_selected = len(selected_packs)
    
    st.markdown("---")
    
    if num_selected < 2:
        st.warning(f"⚠️ Please select at least 2 land packs. Currently selected: {num_selected}")
    elif num_selected > 5:
        st.error(f"❌ Please select maximum 5 land packs. Currently selected: {num_selected}")
    else:
        st.success(f"✅ {num_selected} land pack(s) selected - Total of {num_selected * 5} tiles")
        
        # Generate realm button
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🎲 Generate Realm", type="primary", use_container_width=True):
                realm_tiles = generate_realm_tiles(selected_packs)
                st.session_state.generated_realm = {
                    'land_packs': selected_packs,
                    'tiles': realm_tiles
                }
        
        with col2:
            if st.button("🔙 Back to Home", use_container_width=True):
                st.session_state.show_realm_builder = False
                if 'generated_realm' in st.session_state:
                    del st.session_state.generated_realm
                st.rerun()
    
    # Display generated realm
    if 'generated_realm' in st.session_state:
        st.markdown("---")
        realm = st.session_state.generated_realm
        
        st.header("🗺️ Your Realm")
        
        # Display selected land packs
        st.subheader("Selected Land Packs:")
        cols = st.columns(len(realm['land_packs']))
        icons = {'Caves': '🏔️', 'Mountains': '⛰️', 'Woods': '🌲', 'Plains': '🌾', 'Swamps': '🌿'}
        
        for idx, pack in enumerate(realm['land_packs']):
            with cols[idx]:
                st.info(f"{icons.get(pack, '📍')} **{pack}**")
        
        st.markdown("---")
        
        # Display tiles in order
        st.subheader(f"Realm Tiles (Total: {len(realm['tiles'])})")
        st.caption("Tiles are listed in the order they should be discovered/explored")
        
        # Display tiles in a numbered list with columns
        num_cols = 2
        tile_cols = st.columns(num_cols)
        
        for idx, tile in enumerate(realm['tiles'], 1):
            col_idx = (idx - 1) % num_cols
            with tile_cols[col_idx]:
                # Determine which land pack this tile belongs to
                all_tiles = get_all_tiles_by_land_pack()
                tile_pack = None
                for pack, tiles in all_tiles.items():
                    if tile in tiles:
                        tile_pack = pack
                        break
                
                icon = icons.get(tile_pack, '📍')
                st.markdown(f"**{idx}.** {icon} {tile} *({tile_pack})*")
        
        # Regenerate button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔄 Regenerate Realm", use_container_width=True):
                realm_tiles = generate_realm_tiles(realm['land_packs'])
                st.session_state.generated_realm['tiles'] = realm_tiles
                st.rerun()
        
        with col2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                tile_list = "\n".join([f"{i}. {tile}" for i, tile in enumerate(realm['tiles'], 1)])
                st.code(tile_list, language=None)
                st.success("✅ Tile list displayed above - you can copy it!")


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
    
    # If no char_id provided (new character), use a temporary unique ID for widget keys
    if char_id is None:
        char_id = "new_character"
    
    st.title("🐉 Dragons Down Adventure Journal")
    
    # Top controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        autosave = st.checkbox("Auto-save (2s delay)", value=st.session_state.autosave, key=f"autosave_{char_id}")
        st.session_state.autosave = autosave
    
    with col3:
        # Collapse/Expand All button
        if 'sections_expanded' not in st.session_state:
            st.session_state.sections_expanded = True
        
        if st.button("➖ Collapse All" if st.session_state.sections_expanded else "➕ Expand All", use_container_width=True):
            st.session_state.sections_expanded = not st.session_state.sections_expanded
            st.rerun()
    
    st.markdown("---")
    
    # Character Info Section
    with st.expander("📋 Character Information", expanded=st.session_state.sections_expanded):
        hero_name = st.text_input("Hero Name", value=char_data.get('hero_name', ''), key=f"hero_name_{char_id}")
        lineage_class = st.text_input("Lineage and Class", value=char_data.get('lineage_and_class', ''), key=f"lineage_{char_id}")
        advantages = st.text_area("Advantages", value=char_data.get('advantages', ''), height=100, key=f"advantages_{char_id}")
    
    # Adventure Details Section
    with st.expander("📖 Adventure Details", expanded=st.session_state.sections_expanded):
        scenario = st.text_area("Scenario", value=char_data.get('scenario', ''), height=100, key=f"scenario_{char_id}")
        hero_story = st.text_area("Hero Story", value=char_data.get('hero_story', ''), height=150, key=f"story_{char_id}")
    
    # Journal Entries Section
    with st.expander("📝 Adventure Journal (Lines 1-30)", expanded=st.session_state.sections_expanded):
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
    with st.expander("🗺️ Hidden Paths Found", expanded=st.session_state.sections_expanded):
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
        
        # Render each region as a collapsible expander
        with st.expander("🏔️ Caves", expanded=st.session_state.sections_expanded):
            for location, sides in hidden_path_config['Caves'].items():
                st.markdown(f"**{location}**")
                cols = st.columns(2)
                
                # Tile Side 1
                with cols[0]:
                    st.caption("Tile Side 1")
                    for path in sides['Tile Side 1']:
                        key = f"{path}_s1"
                        # Initialize if not exists
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
                
                # Tile Side 2
                with cols[1]:
                    st.caption("Tile Side 2")
                    for path in sides['Tile Side 2']:
                        key = f"{path}_s2"
                        # Initialize if not exists
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
        
        with st.expander("⛰️ Mountains", expanded=st.session_state.sections_expanded):
            for location, sides in hidden_path_config['Mountains'].items():
                st.markdown(f"**{location}**")
                cols = st.columns(2)
                
                # Tile Side 1
                with cols[0]:
                    st.caption("Tile Side 1")
                    for path in sides['Tile Side 1']:
                        key = f"{path}_s1"
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
                
                # Tile Side 2
                with cols[1]:
                    st.caption("Tile Side 2")
                    for path in sides['Tile Side 2']:
                        key = f"{path}_s2"
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
        
        with st.expander("🌲 Woods", expanded=st.session_state.sections_expanded):
            for location, sides in hidden_path_config['Woods'].items():
                st.markdown(f"**{location}**")
                cols = st.columns(2)
                
                # Tile Side 1
                with cols[0]:
                    st.caption("Tile Side 1")
                    for path in sides['Tile Side 1']:
                        key = f"{path}_s1"
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
                
                # Tile Side 2
                with cols[1]:
                    st.caption("Tile Side 2")
                    for path in sides['Tile Side 2']:
                        key = f"{path}_s2"
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
        
        with st.expander("🌾 Plains", expanded=st.session_state.sections_expanded):
            for location, sides in hidden_path_config['Plains'].items():
                st.markdown(f"**{location}**")
                cols = st.columns(2)
                
                # Tile Side 1
                with cols[0]:
                    st.caption("Tile Side 1")
                    for path in sides['Tile Side 1']:
                        key = f"{path}_s1"
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
                
                # Tile Side 2
                with cols[1]:
                    st.caption("Tile Side 2")
                    for path in sides['Tile Side 2']:
                        key = f"{path}_s2"
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
        
        with st.expander("🌿 Swamps", expanded=st.session_state.sections_expanded):
            for location, sides in hidden_path_config['Swamps'].items():
                st.markdown(f"**{location}**")
                cols = st.columns(2)
                
                # Tile Side 1
                with cols[0]:
                    st.caption("Tile Side 1")
                    for path in sides['Tile Side 1']:
                        key = f"{path}_s1"
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
                            key=f"hp_{location}_{key}_{char_id}"
                        )
                
                # Tile Side 2
                with cols[1]:
                    st.caption("Tile Side 2")
                    for path in sides['Tile Side 2']:
                        key = f"{path}_s2"
                        if location not in hidden_paths:
                            hidden_paths[location] = {}
                        if key not in hidden_paths[location]:
                            hidden_paths[location][key] = False
                            
                        hidden_paths[location][key] = st.checkbox(
                            path,
                            value=hidden_paths[location].get(key, False),
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
    if autosave and char_id and char_id != "new_character":
        if updated_char_data != char_data:
            save_character(char_id, updated_char_data)
            st.caption("✅ Auto-saved")
    elif autosave and char_id == "new_character" and hero_name:
        # Auto-save for new character - create it when hero name is entered
        new_char_id = create_character_id(hero_name)
        if save_character(new_char_id, updated_char_data):
            st.session_state.current_character = new_char_id
            st.session_state.show_create_form = False
            st.caption(f"✅ Auto-saved as: {new_char_id}")
            st.rerun()
    
    # Save Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("💾 Save Character", type="primary", use_container_width=True):
            if char_id and char_id != "new_character":
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
        if char_id and char_id != "new_character" and st.button("🗑️ Delete Character", use_container_width=True):
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
            st.session_state.show_realm_builder = False
            st.session_state.current_character = None
            st.rerun()
        
        # Create New Realm Button
        if st.button("🏰 Create New Realm", type="secondary", use_container_width=True):
            st.session_state.show_realm_builder = True
            st.session_state.show_create_form = False
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
                    st.session_state.show_realm_builder = False
                    st.rerun()
        else:
            st.info("No characters yet. Create your first character!")
        
        st.markdown("---")
        st.caption("Dragons Down Adventure Journal v1.0")
    
    # Main content area
    if st.session_state.show_realm_builder:
        render_realm_builder()
    elif st.session_state.show_create_form:
        render_character_form(get_empty_character())
    elif st.session_state.current_character:
        char_id = st.session_state.current_character
        char_data = st.session_state.characters.get(char_id, get_empty_character())
        render_character_form(char_data, char_id)
    else:
        st.title("🐉 Welcome to Dragons Down Adventure Journal")
        st.markdown("""
        ### Getting Started
        
        - Click **"Create New Character"** to begin tracking a character's adventure
        - Click **"Create New Realm"** to generate a randomized realm for your game
        
        #### Features:
        - 📝 Create and manage multiple character sheets
        - 🏰 Generate randomized realms from 2-5 land packs
        - � Manual save or auto-save functionality
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

