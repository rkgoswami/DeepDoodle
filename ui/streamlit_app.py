import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import sys
import streamlit as st
from PIL import Image
import shutil # Added shutil import

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configs import STORY_EXPANSION_WORD_THRESHOLD, PROMPT
from main import run_comic_generation_workflow #type: ignore
from configs import (
    DEFAULT_LAYOUT_STYLE, SUPPORTED_LAYOUT_STYLES, 
    DEFAULT_STYLE_PRESET, SUPPORTED_STYLE_PRESETS, 
    DEFAULT_GENRE_PRESET, SUPPORTED_GENRE_PRESETS,
    OUTPUT_DIR, COMIC_PAGES_DIR, RAW_PANELS_DIR # Added missing imports
) #type: ignore
from models.comic_generation_state import ComicGenerationState # Import from models

# --- Page Configuration ---
# Constants for layout options
LAYOUT_2X2_GRID = "2x2 Grid (4 Panels)"
LAYOUT_FEATURED_PANEL = "Featured Panel (3 Panels)"
LAYOUT_MIXED_GRID = "Mixed Grid (4 Panels)"
LAYOUT_HORIZONTAL_STRIP = "Horizontal Strip (2 Panels)"
LAYOUT_VERTICAL_STRIP = "Vertical Strip (2 Panels)"

st.set_page_config(page_title="DeepDoodle: AI Comic Generator", layout="wide", initial_sidebar_state="expanded")

# --- CSS Styling ---
st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        # background-color: #f0f2f6;
    }
    
    /* Center the title */
    h1 {
        text-align: center;
    }

    /* Improve button look */
    .stButton>button {
        border-radius: 10px;
        border: 2px solid #4A90E2;
        color: #4A90E2;
        font-weight: bold;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        border-color: #357ABD;
        background-color: #4A90E2;
        color: white;
    }
    .stButton>button:active {
        background-color: #357ABD;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title and Subtitle ---
st.title("✒️ DeepDoodle: AI Comic Generator")
st.markdown("<h4 style='text-align: center; color: #555;'>Turn your stories into visual comic strips with the power of AI Agents</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Directory Setup ---
def setup_directories():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(COMIC_PAGES_DIR, exist_ok=True)
    os.makedirs(RAW_PANELS_DIR, exist_ok=True)

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("⚙️ Model Configuration")
    text_engine_options = {
        "OpenAI (gpt-4o) - Recommended": "openai_gpt4o",
        "Mistral AI (Mixtral-8x7B-Instruct)": "mistral_mixtral_8x7b_instruct",
        "Google (Gemini 1.5 Flash)": "gemini_1.5_flash",
    }
    selected_text_engine_name = st.selectbox("Select Text Engine", list(text_engine_options.keys()))
    text_engine = text_engine_options[selected_text_engine_name]

    image_engine_options = {
        "Black Forest Labs (FLUX.1-schnell) - Recommended": "flux.1-schnell",
        "Stability AI (stable-diffusion-2-1)": "sd21",
    }
    selected_image_engine_name = st.selectbox("Select Image Engine", list(image_engine_options.keys()))
    image_engine = image_engine_options[selected_image_engine_name]

    st.header("🎨 Story & Style")
    story_input = st.text_area("Write or paste your story here:", height=250, 
                               placeholder="A curious fox enters a haunted library...")
    
    # Updated style_options to match keys from STYLE_CONFIGS
    # Assuming 'auto' is still desired as an option for future development or default handling
    style_options = ["Ghibli Animation", "Simple Line Art Comic", "Black and White Manga", "Modern Anime", "Classic Western Comic"]
    style = st.selectbox("Select Visual Style", style_options, index=0)

    mood_options = ["Sci-Fi", "Fantasy", "Horror", "Comedy", "Romance", "Mythology", "Drama", "Mystery", "Adventure", "Whimsical", "Noir", "Cyberpunk", "Steampunk"]
    mood = st.selectbox("Select Mood", mood_options, index=0)
    
    # --- Add Sarvam language dropdown here ---
    sarvam_languages = [
        "English", "Hindi", "Tamil", "Telugu"
    ]
    selected_sarvam_language = st.selectbox("Select Sarvam Output Language", sarvam_languages, index=0)
    # -----------------------------------------

    st.header("📄 Page Layout")
    layout_options = {
        LAYOUT_MIXED_GRID: ("mixed_2x2", 4),
        LAYOUT_FEATURED_PANEL: ("feature_left", 3),
        LAYOUT_2X2_GRID: ("grid_2x2", 4), 
        LAYOUT_HORIZONTAL_STRIP: ("horizontal_strip", 2),
        LAYOUT_VERTICAL_STRIP: ("vertical_strip", 2)
    }
    selected_layout_name = st.selectbox("Select Panel Layout", list(layout_options.keys()))
    layout, panel_count = layout_options[selected_layout_name]
    
    st.markdown("---")
    generate_button = st.button("✨ Generate Comic", use_container_width=True)

# --- Main Panel for Output ---
if 'result' not in st.session_state:
    st.session_state.result = None

if generate_button:
    is_valid = True
    if not story_input.strip():
        st.error("Please provide a story first!")
        is_valid = False

    if is_valid:
        with st.spinner("🧙‍♂️ The AI agents are doodling... Please wait."):
            setup_directories()
            from graph.workflow import create_workflow # Lazy import
            inputs = {
                "story_text": story_input,
                "panel_count": panel_count,
                "style_preset": style,
                "genre_preset": mood,
                "layout_style": layout,
                "text_engine": text_engine,
                "image_engine": image_engine,
                "prompt": PROMPT,
                "target_language": selected_sarvam_language,
            }
            # Initialize the workflow with the provided inputs
            app = create_workflow()
            st.session_state.result = app.invoke(inputs, {"recursion_limit": 100})
    else:
        st.session_state.result = None

if st.session_state.result:
    result = st.session_state.result
    if result and result.get("final_page_images"):
        st.success("Comic generated successfully!")
        
        # Create two columns to constrain the width of the comic page display
        col1, col2, col3 = st.columns([1, 6, 1]) 

        with col2: 
            # Display each page in a styled card
            for i, page_img in enumerate(result["final_page_images"]):
                with st.container(border=True): # Use border=True for a card effect
                    st.image(page_img, use_container_width=True)
                    st.markdown(f"<p style='text-align: center; color: #888;'>Page {i + 1}</p>", unsafe_allow_html=True)
        
        # Display individual panels in an expander with a grid layout
        with st.expander("Show Individual Panels"):
            cols = st.columns(4)
            for idx, panel_path in enumerate(result["panel_image_paths"]):
                with cols[idx % 4]:
                    st.image(panel_path, caption=f"Panel {idx + 1}", use_container_width=True)

    else:
        st.error("An error occurred. The agents failed to generate the comic.")
else:
    st.info("Fill in the details on the left and click 'Generate Comic' to see the magic!")