# configs/text_style_config.py

from .paths_config import BUNDLED_FONT_PATH, HINDI_FONT_PATH, TAMIL_FONT_PATH, TELUGU_FONT_PATH

# --- Text & Caption Styling ---
# Caption styling
CAPTION_BACKGROUND_COLOR = (255, 255, 255, 100)  # RGBA: White with some transparency
CAPTION_TEXT_COLOR = "black"
CAPTION_PADDING = 8                    # Pixels inside the caption box
CAPTION_MARGIN = 5                      # Pixels outside the caption box (spacing between captions)
MAX_CAPTION_HEIGHT_RATIO = 0.25         # Max height of the entire caption block relative to panel height
LINE_SPACING = 2                        # Pixels between lines of text within a single caption
CAPTION_CORNER_RADIUS = 10              # Pixels for rounded corners of dialogue bubbles
NARRATOR_BACKGROUND_COLOR = (255, 250, 220, 180) # RGBA: Light yellowish tint with some transparency
MAX_FONT_SIZE = 14 # Maximum font size for captions
DEFAULT_FONT_SIZE = 12 # Default font size if not otherwise determined
MIN_FONT_SIZE = 10 # Absolute minimum font size to attempt for captions

# Font paths for different languages
FONT_PATHS = {
    "English": BUNDLED_FONT_PATH,
    "Hindi": HINDI_FONT_PATH,
    "Tamil": TAMIL_FONT_PATH,
    "Telugu": TELUGU_FONT_PATH,
}

# SFX (Sound Effects) styling
SFX_TEXT_COLOR = "red"
SFX_FONT_PATH = None # Path to a dedicated SFX font (e.g., from paths_config.BUNDLED_FONT_PATH if needed)
