import streamlit as st
import random
from datetime import datetime
from repository import CharacterRepository
from reference_tabs import render_game_reference
from game_reference_repository import GameReferenceRepository

# Set page configuration
st.set_page_config(
    page_title="Dragons Down Adventure Journal",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for fantasy theme
st.markdown("""
<style>
    /* Import medieval-looking font */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Crimson+Text:ital,wght@0,400;0,700;1,400&display=swap');
    
    /* Main theme colors - dark fantasy */
    :root {
        --primary-color: #d4af37;
        --background-color: #0d0907;
        --secondary-background-color: #1a120d;
        --text-color: #f5e6d3;
        --accent-color: #ff6b35;
    }
    
    /* Main background - deep dark with subtle texture */
    .stApp {
        background: 
            radial-gradient(ellipse at top, #1a0f0a 0%, #0d0907 50%, #000000 100%),
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(139, 69, 19, 0.02) 10px,
                rgba(139, 69, 19, 0.02) 20px
            );
        background-attachment: fixed;
    }
    
    /* Sidebar - rich leather book style */
    [data-testid="stSidebar"] {
        background: 
            linear-gradient(180deg, #2d1810 0%, #1a0f0a 50%, #0d0604 100%);
        border-right: 4px solid #d4af37;
        box-shadow: 
            inset -20px 0 30px rgba(0,0,0,0.5),
            5px 0 20px rgba(212, 175, 55, 0.2);
        position: relative;
    }
    
    /* Sidebar decorative border */
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        right: 4px;
        width: 2px;
        height: 100%;
        background: linear-gradient(
            to bottom,
            transparent,
            rgba(255, 107, 53, 0.5) 10%,
            rgba(255, 107, 53, 0.5) 90%,
            transparent
        );
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        color: #d4af37 !important;
        font-family: 'Cinzel', serif !important;
        text-shadow: 
            2px 2px 4px #000000,
            0 0 20px rgba(212, 175, 55, 0.6),
            0 0 40px rgba(212, 175, 55, 0.3);
        font-size: 1.8rem !important;
        letter-spacing: 2px;
        border-bottom: 3px double #d4af37;
        padding-bottom: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Sidebar caption */
    [data-testid="stSidebar"] .stCaption {
        color: #d4af37 !important;
        text-align: center;
        font-style: italic;
        margin-top: 20px;
        border-top: 1px solid #8B4513;
        padding-top: 10px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #d4af37 !important;
        font-family: 'Cinzel', serif !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        letter-spacing: 2px;
    }
    
    /* Main title */
    .main h1 {
        font-size: 3rem !important;
        text-align: center;
        background: linear-gradient(135deg, #ffd700 0%, #d4af37 50%, #ff6b35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.8));
        margin-bottom: 30px;
        padding: 20px 0;
        border-bottom: 3px solid #d4af37;
        border-top: 3px solid #d4af37;
    }
    
    /* Section headers */
    .main h2 {
        color: #ff6b35 !important;
        border-left: 5px solid #d4af37;
        padding-left: 15px;
        margin-top: 30px;
    }
    
    /* Expander styling - ancient book pages */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2d1810 0%, #1a0f0a 100%) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 10px !important;
        color: #f5e6d3 !important;
        font-weight: bold;
        font-family: 'Cinzel', serif !important;
        box-shadow: 
            0 4px 10px rgba(0,0,0,0.7),
            inset 0 1px 0 rgba(212, 175, 55, 0.3);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #3d2820 0%, #2d1810 100%) !important;
        border-color: #ffd700 !important;
        box-shadow: 
            0 6px 15px rgba(0,0,0,0.8),
            0 0 20px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(180deg, #1a120d 0%, #0d0907 100%) !important;
        border: 2px solid #8B4513 !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        box-shadow: inset 0 4px 8px rgba(0,0,0,0.5);
        padding: 20px !important;
    }
    
    /* Buttons - ornate medieval */
    .stButton button {
        background: linear-gradient(135deg, #8B4513 0%, #654321 100%) !important;
        color: #f5e6d3 !important;
        border: 3px solid #d4af37 !important;
        border-radius: 8px !important;
        font-weight: bold;
        font-family: 'Cinzel', serif !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
        box-shadow: 
            0 4px 8px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(212, 175, 55, 0.3);
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #a0522d 0%, #8B4513 100%) !important;
        border-color: #ffd700 !important;
        box-shadow: 
            0 6px 12px rgba(0,0,0,0.8),
            0 0 25px rgba(212, 175, 55, 0.5);
        transform: translateY(-3px);
    }
    
    /* Primary button - golden treasure */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #ffd700 0%, #d4af37 50%, #ff6b35 100%) !important;
        color: #0d0907 !important;
        border: 3px solid #ffd700 !important;
        font-weight: 900;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
    }
    
    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #ffed4e 0%, #ffd700 50%, #ff8c52 100%) !important;
        box-shadow: 
            0 8px 16px rgba(0,0,0,0.9),
            0 0 40px rgba(255, 215, 0, 0.8),
            inset 0 0 20px rgba(255,255,255,0.3);
        transform: translateY(-3px) scale(1.02);
    }
    
    /* Input fields - parchment style */
    .stTextInput input, .stTextArea textarea {
        background-color: #2d1f15 !important;
        border: 2px solid #8B4513 !important;
        border-radius: 8px !important;
        color: #f5e6d3 !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 1.1rem !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #d4af37 !important;
        box-shadow: 
            inset 0 2px 4px rgba(0,0,0,0.5),
            0 0 15px rgba(212, 175, 55, 0.4) !important;
        background-color: #3d2f25 !important;
    }
    
    /* Checkboxes */
    .stCheckbox {
        color: #f5e6d3 !important;
        font-family: 'Crimson Text', serif !important;
    }
    
    /* Labels and captions */
    .stCaption {
        color: #d4af37 !important;
        font-weight: bold;
        font-family: 'Cinzel', serif !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #f5e6d3 !important;
        font-family: 'Crimson Text', serif !important;
        line-height: 1.8;
    }
    
    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, #1a3d1a 0%, #0f2a0f 100%) !important;
        border: 2px solid #4a7c4a !important;
        border-radius: 8px;
        color: #90ee90 !important;
    }
    
    /* Error messages */
    .stError {
        background: linear-gradient(135deg, #3d1a1a 0%, #2a0f0f 100%) !important;
        border: 2px solid #8B0000 !important;
        color: #ff6b6b !important;
    }
    
    /* Horizontal rules - ornate divider */
    hr {
        border: none !important;
        height: 3px !important;
        background: linear-gradient(
            to right,
            transparent,
            #d4af37 20%,
            #d4af37 80%,
            transparent
        ) !important;
        margin: 30px 0 !important;
    }
    
    /* Column styling */
    [data-testid="column"] {
        background-color: rgba(29, 18, 13, 0.5);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(139, 69, 19, 0.3);
    }
</style>
""", unsafe_allow_html=True)

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

if 'show_combat_tracker' not in st.session_state:
    st.session_state.show_combat_tracker = False

if 'show_game_reference' not in st.session_state:
    st.session_state.show_game_reference = False

if 'last_save_time' not in st.session_state:
    st.session_state.last_save_time = None

if 'pending_save' not in st.session_state:
    st.session_state.pending_save = False

if 'combat_tracker' not in st.session_state:
    st.session_state.combat_tracker = {
        'in_combat': False,
        'current_round': 1,
        'rounds_without_damage': 0,
        'player_hidden': False,
        'enemy_flipped': False,
        'combat_log': []
    }


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


def render_combat_tracker():
    """Render the combat tracker interface with step-by-step guidance"""
    st.title("⚔️ Combat Tracker")
    
    st.markdown("""
    ### Step-by-Step Combat Guide
    
    Follow the combat flow based on Dragons Down rules.
    """)
    
    # Back button at top
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.button("🔙 Back to Home", use_container_width=True):
            st.session_state.show_combat_tracker = False
            st.rerun()
    
    st.markdown("---")
    
    # Get combat tracker from session state
    combat_tracker = st.session_state.combat_tracker
    
    # Initialize combat step if not exists
    if 'combat_step' not in combat_tracker:
        combat_tracker['combat_step'] = 'start'
    
    # Combat status bar
    if combat_tracker.get('in_combat', False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Current Round", combat_tracker.get('current_round', 1))
        with col2:
            st.metric("💔 Rounds No Damage", combat_tracker.get('rounds_without_damage', 0))
        with col3:
            if st.button("🏁 End Combat", type="secondary", use_container_width=True):
                # Log combat end
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': f"Combat ended after {combat_tracker['current_round']} rounds"
                })
                combat_tracker['combat_log'] = combat_log
                # Reset combat
                combat_tracker['in_combat'] = False
                combat_tracker['current_round'] = 1
                combat_tracker['rounds_without_damage'] = 0
                combat_tracker['player_hidden'] = False
                combat_tracker['enemy_flipped'] = False
                combat_tracker['combat_step'] = 'start'
                st.success("✅ Combat ended!")
                st.rerun()
        
        st.markdown("---")
    
    # Get current step
    current_step = combat_tracker.get('combat_step', 'start')
    
    # START COMBAT
    if current_step == 'start':
        st.header("🎬 Start Combat")
        st.markdown("""
        ### Ready to begin combat?
        Click below to start a new combat encounter.
        """)
        
        if st.button("⚔️ Start New Combat", type="primary", use_container_width=True, key="start_combat"):
            combat_tracker['in_combat'] = True
            combat_tracker['current_round'] = 1
            combat_tracker['rounds_without_damage'] = 0
            combat_tracker['player_hidden'] = False
            combat_tracker['enemy_flipped'] = False
            combat_tracker['combat_step'] = 'hidden_check'
            # Log combat start
            combat_log = combat_tracker.get('combat_log', [])
            combat_log.append({
                'round': 1,
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'event': "Combat started"
            })
            combat_tracker['combat_log'] = combat_log
            st.rerun()
        
        # Show last combat log if exists
        combat_log = combat_tracker.get('combat_log', [])
        if combat_log:
            st.markdown("---")
            st.subheader("📜 Previous Combat Log")
            with st.expander("View Last Combat", expanded=False):
                for entry in reversed(combat_log[-10:]):
                    st.caption(f"**Round {entry['round']}** ({entry['timestamp']}): {entry['event']}")
    
    # HIDDEN CHECK
    elif current_step == 'hidden_check':
        st.header(f"🌑 Round {combat_tracker.get('current_round', 1)} - Are You Hidden?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ YES - I am hidden", type="primary", use_container_width=True, key="hidden_yes"):
                combat_tracker['player_hidden'] = True
                combat_tracker['combat_step'] = 'hidden_ambush'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': "Player is hidden"
                })
                combat_tracker['combat_log'] = combat_log
                st.rerun()
        
        with col2:
            if st.button("❌ NO - Not hidden", use_container_width=True, key="hidden_no"):
                combat_tracker['player_hidden'] = False
                combat_tracker['combat_step'] = 'normal_combat'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': "Player is not hidden - normal combat"
                })
                combat_tracker['combat_log'] = combat_log
                st.rerun()
    
    # HIDDEN - AMBUSH DECISION
    elif current_step == 'hidden_ambush':
        st.header(f"🎯 Round {combat_tracker.get('current_round', 1)} - Hidden: Do You Want to Ambush?")
        st.info("💡 You can only ambush with a spell or ranged weapon")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⚔️ YES - Ambush Attack", type="primary", use_container_width=True, key="ambush_yes"):
                combat_tracker['combat_step'] = 'ambush_action'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': "Player chose to ambush"
                })
                combat_tracker['combat_log'] = combat_log
                st.rerun()
        
        with col2:
            if st.button("👁️ NO - Stay Hidden (Recon)", use_container_width=True, key="ambush_no"):
                combat_tracker['combat_step'] = 'recon_round'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': "Player stays hidden for reconnaissance"
                })
                combat_tracker['combat_log'] = combat_log
                st.rerun()
    
    # RECONNAISSANCE ROUND
    elif current_step == 'recon_round':
        st.header(f"👁️ Round {combat_tracker.get('current_round', 1)} - Reconnaissance")
        st.markdown("""
        ### You are staying hidden to observe the enemy
        
        - Watch if the enemy flips
        - You can attack in the next round
        - **Remember:** Monster will still use skills dice in Round 2 if you attack
        """)
        
        st.warning("⚠️ Monster uses skills dice for Round 2 if you attack next round")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Continue Observing (Next Round)", use_container_width=True, key="recon_continue"):
                # Advance to next round
                combat_tracker['current_round'] += 1
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'] - 1,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': f"Reconnaissance complete - moving to Round {combat_tracker['current_round']}"
                })
                combat_tracker['combat_log'] = combat_log
                combat_tracker['combat_step'] = 'hidden_ambush'
                st.rerun()
        
        with col2:
            if st.button("⚔️ Attack Now (Monster uses skills dice)", type="primary", use_container_width=True, key="recon_attack"):
                combat_tracker['combat_step'] = 'ambush_monster_skills'
                st.rerun()
    
    # AMBUSH - MONSTER SKILLS DICE (Round 2 after recon)
    elif current_step == 'ambush_monster_skills':
        st.header(f"🎲 Round {combat_tracker.get('current_round', 1)} - Monster Rolls Skills Dice")
        st.warning("⚠️ This is Round 2 after reconnaissance - Monster rolls skills dice!")
        
        st.markdown("""
        ### Roll skills dice for the monster
        - Check if they flip
        - Then proceed to your ambush attack
        """)
        
        if st.button("✅ Skills Dice Rolled - Proceed to Ambush", type="primary", use_container_width=True, key="skills_rolled"):
            combat_tracker['combat_step'] = 'ambush_action'
            st.rerun()
    
    # AMBUSH ACTION
    elif current_step == 'ambush_action':
        st.header(f"🎯 Round {combat_tracker.get('current_round', 1)} - Ambush Attack")
        
        st.markdown("""
        ### Execute Your Ambush
        1. 🎯 Target monster
        2. 🎲 Monster rolls skills dice to see if they flip
        3. 💥 Process damage
        """)
        
        weapon_type = st.radio("Weapon Type:", ["Spell", "Ranged Weapon", "Other"], key="weapon_type", horizontal=True)
        
        if weapon_type == "Ranged Weapon":
            st.warning("🏹 Ranged Weapon: Roll ranged dice and keep the WORST result!")
        
        st.markdown("---")
        
        st.markdown("### Did enemy flip?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Enemy Flipped", use_container_width=True):
                combat_tracker['enemy_flipped'] = True
        with col2:
            if st.button("❌ Enemy Did NOT Flip", use_container_width=True):
                combat_tracker['enemy_flipped'] = False
        
        st.markdown("---")
        
        if st.button("💥 Damage Processed - Roll Sneak Dice", type="primary", use_container_width=True, key="ambush_damage"):
            combat_tracker['combat_step'] = 'sneak_roll'
            combat_tracker['rounds_without_damage'] = 0  # Reset no damage counter
            combat_log = combat_tracker.get('combat_log', [])
            combat_log.append({
                'round': combat_tracker['current_round'],
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'event': f"Ambush attack executed with {weapon_type}"
            })
            combat_tracker['combat_log'] = combat_log
            st.rerun()
    
    # SNEAK ROLL AFTER AMBUSH
    elif current_step == 'sneak_roll':
        st.header(f"🎲 Round {combat_tracker.get('current_round', 1)} - Roll Sneak Dice")
        
        st.markdown("""
        ### After ambush, roll your sneak dice
        
        **To stay hidden:**
        - 🎯 You need to roll **TWO BLANKS**
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Rolled 2 Blanks - Still Hidden!", type="primary", use_container_width=True, key="sneak_success"):
                combat_tracker['player_hidden'] = True
                combat_tracker['current_round'] += 1
                combat_tracker['combat_step'] = 'hidden_ambush'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'] - 1,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': f"Sneak successful - still hidden, moving to Round {combat_tracker['current_round']}"
                })
                combat_tracker['combat_log'] = combat_log
                st.success("🌑 You remain hidden! Can ambush again next round.")
                st.rerun()
        
        with col2:
            if st.button("❌ Did NOT Roll 2 Blanks - Revealed!", use_container_width=True, key="sneak_fail"):
                combat_tracker['player_hidden'] = False
                combat_tracker['combat_step'] = 'round_end'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': "Sneak failed - player revealed"
                })
                combat_tracker['combat_log'] = combat_log
                st.warning("⚠️ You are revealed! Continue with normal combat.")
                st.rerun()
    
    # NORMAL COMBAT
    elif current_step == 'normal_combat':
        st.header(f"⚔️ Round {combat_tracker.get('current_round', 1)} - Normal Combat")
        
        st.markdown("""
        ### Normal Combat Sequence
        1. **Assign Tactics** - Allocate cubes to weapon, spells, speed, maneuver
        2. **Select Target**
        3. **Roll Dice** to see if enemy flips
        4. **Execute Combat** in speed order
        """)
        
        with st.expander("📋 Step 1: Assign Tactics", expanded=True):
            st.markdown("Allocate your cubes to:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("- 🗡️ Weapon")
                st.markdown("- ✨ Spells")
            with col2:
                st.markdown("- 🏃 Speed")
                st.markdown("- 🛡️ Maneuver")
        
        with st.expander("🎯 Step 2: Select Target"):
            st.markdown("Choose which enemy to attack")
        
        with st.expander("🎲 Step 3: Roll Dice"):
            st.markdown("Roll dice to see if enemy flips")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Enemy Flipped", use_container_width=True, key="normal_flip_yes"):
                    combat_tracker['enemy_flipped'] = True
                    st.success("Enemy flipped!")
            with col2:
                if st.button("❌ Enemy Did NOT Flip", use_container_width=True, key="normal_flip_no"):
                    combat_tracker['enemy_flipped'] = False
                    st.info("Enemy did not flip")
        
        st.markdown("---")
        
        with st.expander("⚔️ Step 4: Execute Combat in Speed Order", expanded=True):
            st.markdown("### Damage Processing")
            
            weapon_type = st.radio("Using ranged weapon?", ["No", "Yes - Ranged Weapon"], key="normal_weapon", horizontal=True)
            
            if weapon_type == "Yes - Ranged Weapon":
                st.warning("🏹 **Ranged Weapon Rule:** Roll ranged dice and keep the WORST result!")
            
            st.markdown("---")
            st.markdown("#### Automatic Hit Check")
            st.info("💡 If your Speed > Enemy Maneuver = Automatic Hit!")
            
            auto_hit = st.checkbox("🎯 Automatic Hit? (Speed > Maneuver)", key="auto_hit")
            
            if auto_hit:
                st.success("✅ Automatic Hit!")
                instant_kill = st.checkbox("💀 Total Damage ≥ Enemy Health? (Instant Kill)", key="instant_kill")
                if instant_kill:
                    st.error("💀 INSTANT KILL!")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💔 Damage Dealt This Round", type="primary", use_container_width=True, key="normal_damage"):
                combat_tracker['rounds_without_damage'] = 0
                combat_tracker['combat_step'] = 'round_end'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': "Damage dealt in normal combat"
                })
                combat_tracker['combat_log'] = combat_log
                st.rerun()
        
        with col2:
            if st.button("⏩ No Damage This Round", use_container_width=True, key="normal_no_damage"):
                combat_tracker['rounds_without_damage'] = combat_tracker.get('rounds_without_damage', 0) + 1
                combat_tracker['combat_step'] = 'round_end'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': "No damage dealt"
                })
                combat_tracker['combat_log'] = combat_log
                st.rerun()
    
    # ROUND END
    elif current_step == 'round_end':
        st.header(f"🔄 End of Round {combat_tracker.get('current_round', 1)}")
        
        rounds_no_dmg = combat_tracker.get('rounds_without_damage', 0)
        
        if rounds_no_dmg >= 2:
            st.error("🛑 **Combat Should End!** - No damage for 2 consecutive rounds")
            st.markdown("According to the rules, combat ends after 2 rounds without damage.")
            
            if st.button("🏁 End Combat Now", type="primary", use_container_width=True, key="force_end"):
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': "Combat ended - 2 rounds without damage"
                })
                combat_tracker['combat_log'] = combat_log
                combat_tracker['in_combat'] = False
                combat_tracker['current_round'] = 1
                combat_tracker['rounds_without_damage'] = 0
                combat_tracker['player_hidden'] = False
                combat_tracker['enemy_flipped'] = False
                combat_tracker['combat_step'] = 'start'
                st.rerun()
        else:
            st.success(f"✅ Round {combat_tracker.get('current_round', 1)} Complete!")
            
            if rounds_no_dmg > 0:
                st.warning(f"⚠️ {rounds_no_dmg} round(s) without damage. Combat ends after 2.")
            
            st.markdown("---")
            
            if st.button("➡️ Continue to Next Round", type="primary", use_container_width=True, key="next_round"):
                combat_tracker['current_round'] += 1
                combat_tracker['combat_step'] = 'hidden_check'
                combat_log = combat_tracker.get('combat_log', [])
                combat_log.append({
                    'round': combat_tracker['current_round'],
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'event': f"Round {combat_tracker['current_round']} started"
                })
                combat_tracker['combat_log'] = combat_log
                st.rerun()
    
    # Combat Log at bottom
    st.markdown("---")
    st.subheader("📜 Combat Log")
    combat_log = combat_tracker.get('combat_log', [])
    
    if combat_log:
        with st.expander("View Combat Log", expanded=False):
            for entry in reversed(combat_log[-20:]):
                st.caption(f"**Round {entry['round']}** ({entry['timestamp']}): {entry['event']}")
            
            if st.button("🗑️ Clear Log", key="clear_log_bottom"):
                combat_tracker['combat_log'] = []
                st.rerun()
    else:
        st.info("No combat events logged yet")


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
        
        # Lineage and Class with Random Generator
        col_lc1, col_lc2 = st.columns([3, 1])
        with col_lc1:
            lineage_class = st.text_input("Lineage and Class", value=char_data.get('lineage_and_class', ''), key=f"lineage_{char_id}")
        with col_lc2:
            if st.button("🎲 Random", key=f"random_lc_{char_id}", use_container_width=True, help="Generate random race and class"):
                repo = GameReferenceRepository()
                lineages = repo.get_all_lineages()
                classes = repo.get_all_classes()
                
                if lineages and classes:
                    random_lineage = random.choice(lineages)
                    random_class = random.choice(classes)
                    random_text = f"{random_lineage['name']} {random_class['name']}"
                    random_advantages = f"**{random_lineage['name']} - {random_lineage['advantage']}:** {random_lineage['description']}\n\n**{random_class['name']} - {random_class['advantage']}:** {random_class['description']}"
                    
                    # Update session state to trigger UI update
                    if f"lineage_{char_id}" in st.session_state:
                        st.session_state[f"lineage_{char_id}"] = random_text
                    if f"advantages_{char_id}" in st.session_state:
                        st.session_state[f"advantages_{char_id}"] = random_advantages
                    st.rerun()
        
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
            st.session_state.show_combat_tracker = False
            st.session_state.show_game_reference = False
            st.session_state.current_character = None
            st.rerun()
        
        # Create New Realm Button
        if st.button("🏰 Create New Realm", type="secondary", use_container_width=True):
            st.session_state.show_realm_builder = True
            st.session_state.show_create_form = False
            st.session_state.show_combat_tracker = False
            st.session_state.show_game_reference = False
            st.session_state.current_character = None
            st.rerun()
        
        # Combat Tracker Button
        if st.button("⚔️ Combat Tracker", type="secondary", use_container_width=True):
            st.session_state.show_combat_tracker = True
            st.session_state.show_realm_builder = False
            st.session_state.show_create_form = False
            st.session_state.show_game_reference = False
            st.session_state.current_character = None
            st.rerun()
        
        # Game Reference Button
        if st.button("📚 Game Reference", type="secondary", use_container_width=True):
            st.session_state.show_game_reference = True
            st.session_state.show_realm_builder = False
            st.session_state.show_create_form = False
            st.session_state.show_combat_tracker = False
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
                    st.session_state.show_combat_tracker = False
                    st.session_state.show_game_reference = False
                    st.rerun()
        else:
            st.info("No characters yet. Create your first character!")
        
        st.markdown("---")
        st.caption("Dragons Down Adventure Journal v1.0")
    
    # Main content area
    if st.session_state.show_realm_builder:
        render_realm_builder()
    elif st.session_state.show_combat_tracker:
        render_combat_tracker()
    elif st.session_state.show_game_reference:
        render_game_reference()
    elif st.session_state.show_create_form:
        render_character_form(get_empty_character())
    elif st.session_state.current_character:
        char_id = st.session_state.current_character
        char_data = st.session_state.characters.get(char_id, get_empty_character())
        render_character_form(char_data, char_id)
    else:
        st.title("🐉 Dragons Down Adventure Journal")
        
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
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(139, 69, 19, 0.2) 0%, rgba(61, 42, 31, 0.3) 100%); 
                    padding: 30px; border-radius: 15px; border: 3px solid #8B4513; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.6); margin: 20px 0;'>
            <h2 style='color: #d4af37; text-align: center; font-family: Georgia, serif; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.8); margin-bottom: 20px;'>
                ⚔️ The Age of Rebuilding ⚔️
            </h2>
            <p style='color: #e8dcc4; font-size: 1.1em; text-align: center; font-style: italic; 
                     line-height: 1.8; font-family: Georgia, serif;'>
                Two centuries have passed since the dragons' wrath consumed the world. 
                From the ashes of destruction, brave civilizations rise again. 
                Elves, humans, and dwarves forge new alliances, venturing into forgotten ruins 
                and facing ancient evils. Orcs, goblins, and darker creatures lurk in the shadows, 
                challenging those who dare to explore the scarred lands.
            </p>
            <p style='color: #d4af37; font-size: 1.2em; text-align: center; font-weight: bold; 
                     margin-top: 20px; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);'>
                Will you be the hero this broken world needs?
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

