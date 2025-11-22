"""
Dragons Down Game Reference - Streamlit Tab Component
"""
import streamlit as st
from game_reference_repository import GameReferenceRepository

# Initialize repository
@st.cache_resource
def get_repository():
    return GameReferenceRepository()

def render_game_reference():
    """Render the game reference tabs"""
    
    st.title("📚 Dragons Down Game Reference")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏺 Treasures", "✨ Spells", "👥 Lineages", "⚔️ Classes"])
    
    with tab1:
        render_treasures()
    
    with tab2:
        render_spells()
    
    with tab3:
        render_lineages()
    
    with tab4:
        render_classes()


def render_treasures():
    """Render treasures reference"""
    st.header("🏺 Treasure Manifest")
    repo = get_repository()
    
    # Search box
    search = st.text_input("🔍 Search treasures", placeholder="Type treasure name...", key="treasure_search")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        types = ["All"] + repo.get_treasure_types()
        treasure_type = st.selectbox("Type", types)
    with col2:
        rarities = ["All"] + repo.get_treasure_rarities()
        rarity = st.selectbox("Rarity", rarities)
    
    # Get treasures
    if search:
        treasures = repo.search_treasures(
            search, 
            treasure_type=None if treasure_type == "All" else treasure_type,
            rarity=None if rarity == "All" else rarity
        )
    else:
        treasures = repo.get_all_treasures()
        if treasure_type != "All":
            treasures = [t for t in treasures if t["type"] == treasure_type]
        if rarity != "All":
            treasures = [t for t in treasures if t["rarity"] == rarity]
    
    # Display count
    st.caption(f"Showing {len(treasures)} treasures")
    
    # Display results
    if treasures:
        for treasure in sorted(treasures, key=lambda x: x["name"]):
            icon = "👑" if treasure["rarity"] == "Legendary" else "⭐" if treasure["rarity"] == "Epic" else "💎" if treasure["rarity"] == "Valuable" else "⚔️"
            
            with st.expander(f"{icon} {treasure['name']}"):
                st.markdown(f"**Type:** {treasure['type']}")
                st.markdown(f"**Rarity:** {treasure['rarity']}")
                if treasure.get('subtype'):
                    st.markdown(f"**Subtype:** {treasure['subtype']}")
                st.markdown(treasure['description'])
    else:
        st.info("No treasures found matching your search.")


def render_spells():
    """Render spells reference"""
    st.header("✨ Spell Manifest")
    repo = get_repository()
    
    # Search box
    search = st.text_input("🔍 Search spells", placeholder="Type spell name...", key="spell_search")
    
    # Spell color filter
    colors = ["All"] + repo.get_spell_colors()
    spell_color = st.selectbox("Magic Color", colors)
    
    # Get spells
    if search:
        spells = repo.search_spells(search, color=None if spell_color == "All" else spell_color)
    else:
        spells = repo.get_all_spells() if spell_color == "All" else repo.get_spells_by_color(spell_color)
    
    # Display count
    st.caption(f"Showing {len(spells)} spells")
    
    # Display results
    if spells:
        color_icons = {
            "Universal": "🌟", "Black": "💀", "Blue": "💧", 
            "Gray": "🌫️", "Green": "🌿", "Purple": "⚡", 
            "White": "✨", "Yellow": "🔮"
        }
        
        for spell in sorted(spells, key=lambda x: x["name"]):
            icon = color_icons.get(spell['color'], '✨')
            
            with st.expander(f"{icon} {spell['name']} - {spell['color']} Magic"):
                st.markdown(f"**Type:** {spell['type']}")
                st.markdown(f"**Timing:** {spell['timing']}")
                st.markdown(f"**Magic Color:** {spell['color']}")
                st.markdown(spell['description'])
    else:
        st.info("No spells found matching your search.")


def render_lineages():
    """Render lineages/races reference"""
    st.header("👥 Lineage Advantages")
    repo = get_repository()
    
    # Search box
    search = st.text_input("🔍 Search lineages", placeholder="Type lineage name...", key="lineage_search")
    
    # Get lineages
    lineages = repo.search_lineages(search) if search else repo.get_all_lineages()
    
    # Display count
    st.caption(f"Showing {len(lineages)} lineages")
    
    # Display
    if lineages:
        for lineage in sorted(lineages, key=lambda x: x["name"]):
            with st.expander(f"👤 {lineage['name']} ({lineage['advantage']})"):
                st.markdown(lineage['description'])
    else:
        st.info("No lineages found matching your search.")


def render_classes():
    """Render classes reference"""
    st.header("⚔️ Class Advantages")
    repo = get_repository()
    
    # Search box
    search = st.text_input("🔍 Search classes", placeholder="Type class name...", key="class_search")
    
    # Get classes
    classes = repo.search_classes(search) if search else repo.get_all_classes()
    
    # Display count
    st.caption(f"Showing {len(classes)} classes")
    
    # Display
    if classes:
        for cls in sorted(classes, key=lambda x: x["name"]):
            with st.expander(f"🎭 {cls['name']} ({cls['advantage']})"):
                st.markdown(cls['description'])
    else:
        st.info("No classes found matching your search.")
