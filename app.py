import streamlit as st
from translator import EmojiTranslator
import json
import os
import logging
from datetime import datetime
from typing import Optional, List, Dict
from dotenv import load_dotenv
import pyperclip

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Constants
MAX_CHARS = 200
HISTORY_FILE = "storage.json"
MAX_HISTORY_ITEMS = 50

def load_history() -> List[Dict]:
    """Load translation history from JSON file."""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.info("No history file found, creating new one")
        return []
    except json.JSONDecodeError:
        logger.error("Invalid JSON in history file, resetting")
        return []

def save_history(history: List[Dict]) -> None:
    """Save translation history to JSON file."""
    try:
        # Keep only the most recent items
        if len(history) > MAX_HISTORY_ITEMS:
            history = history[-MAX_HISTORY_ITEMS:]
        
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save history: {e}")
        st.error("Failed to save translation history")

def get_emoji_codes(text: str) -> List[str]:
    """Extract Unicode codes for emojis in the text."""
    return [f"U+{ord(c):04X}" for c in text if ord(c) > 127]  # Only non-ASCII characters

def copy_to_clipboard_safe(text: str, message: str) -> None:
    """Safely copy text to clipboard with error handling."""
    try:
        pyperclip.copy(text)
        st.success(f"✅ {message}")
    except Exception as e:
        logger.error(f"Failed to copy to clipboard: {e}")
        st.error("Failed to copy to clipboard. Please copy manually.")

# Page config
st.set_page_config(
    page_title="Emoji Mood Translator",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Add FontAwesome to the head
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# Theme customization
st.markdown("""
    <style>
        .main {
            background-color: #1E1E1E;  /* Light Blue background */
        }
        .title {
            font-size: 40px;
            text-align: center;
            color: #FFD700;  /* Primary Yellow */
            margin-bottom: 30px;
            font-family: sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .subtitle {
            font-size: 28px;
            color: #FFD700;  /* Secondary Text */
            font-family: sans-serif;
        }
        .translation-box {
            background-color: #34495E;  /* Primary Yellow */
            padding: 25px;
            border-radius: 10px;
            font-size: 33px;
            text-align: center;
            border: 2px solid #FFA500;  /* Secondary Orange */
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            color: #fff; 
        }
        .emoji-result {
            margin-bottom: 15px;
        }
        .emoji-codes {
            font-family: monospace;
            font-size: 16px;
            color: #fff;  /* Secondary Text */
            margin-top: 10px;
            background-color: rgba(255,255,255,0.2);
            padding: 8px;
            border-radius: 5px;
        }
        .code-label {
            color: rgba(255,255,255,0.7);
        }
        .history-box {
            background-color: #1E1E1E;  /* Secondary Orange */
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            color: #fff;  /* Primary Text */
            border: 1px solid #FFD700;  /* Primary Yellow */
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .stTextArea textarea {
            font-size: 24px !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border: 2px solid #FFA500 !important;  /* Secondary Orange */
            min-height: 120px !important;
            width: 100% !important;
            font-family: sans-serif !important;
            background-color: 1E1E1E !important;
            color: #fff !important; 
        }
        .stButton button {
            background-color: #FFD700 !important;  /* Primary Yellow */
            color: #333333 !important;  /* Primary Text */
            font-family: sans-serif !important;
            display: block !important;
            margin: 20px auto !important;
            padding: 10px 30px !important;
            font-size: 20px !important;
            border: 2px solid #FFA500 !important;  /* Secondary Orange */
            transition: all 0.3s ease !important;
        }
        .stButton button:hover {
            background-color: #FFA500 !important;  /* Secondary Orange */
            color: white !important;
        }
        .copy-icon {
            color: #FFA500 !important;  /* Primary Text */
            cursor: pointer !important;
            padding: 5px 8px !important;
            border-radius: 5px !important;
            display: inline-flex !important;
            align-items: center !important;
            transition: all 0.3s ease !important;
            margin-left: 10px !important;
            font-size: 16px !important;
        }
        .tooltip:hover::after {
            background-color: #FFA500;  /* Secondary Orange */
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        /* Placeholder and disabled text */
        ::placeholder {
            color: #BBBBBB !important;  /* Tertiary Text */
        }
        .disabled {
            color: #BBBBBB !important;  /* Tertiary Text */
        }
    </style>
""", unsafe_allow_html=True)

# Add copy functions
def copy_to_clipboard(text, message):
    pyperclip.copy(text)
    st.toast(f"✅ {message}", icon="🔄")

# Create a session state for translation result
if 'translation_result' not in st.session_state:
    st.session_state.translation_result = ""
    st.session_state.emoji_codes = ""

if 'translation_style' not in st.session_state:
    st.session_state.translation_style = "Standard"

if 'reverse_translation' not in st.session_state:
    st.session_state.reverse_translation = ""

# Move input components to sidebar
with st.sidebar:
    st.markdown('<div class="title">Input</div>', unsafe_allow_html=True)
    
    # Move text input to sidebar
    MAX_CHARS = 100
    user_input = st.text_area("💬 Enter your mood or thought:", height=120, max_chars=MAX_CHARS)
    chars_left = MAX_CHARS - len(user_input)
    
    # Display character counter in sidebar
    counter_style = (
        "danger" if chars_left < 20 else 
        "warning" if chars_left < 40 else 
        ""
    )
    
    # Move translation style selector to sidebar
    st.session_state.translation_style = st.selectbox(
        "Select Translation Style:",
        ["Standard", "Minimal", "Expressive"],
        help="Standard: Basic translation\nMinimal: 1-2 emojis\nExpressive: More detailed emotions"
    )
    
    # Move translate button to sidebar
    if st.button("🔁 Translate to Emoji", use_container_width=True, disabled=not user_input.strip()):
        if user_input.strip():
            with st.spinner("🤖 Translating your mood..."):
                try:
                    translator = EmojiTranslator()
                    emoji_result = translator.translate(user_input.strip())
                    
                    if emoji_result and not emoji_result.startswith("❌"):
                        # Get emoji codes
                        emoji_codes = get_emoji_codes(emoji_result)
                        emoji_codes_str = ", ".join(emoji_codes)

                        # Update session state
                        st.session_state.translation_result = emoji_result
                        st.session_state.emoji_codes = emoji_codes_str

                        # Save to history
                        history = load_history()
                        history.append({
                            "input": user_input.strip(),
                            "translation": emoji_result,
                            "emoji_codes": emoji_codes,
                            "timestamp": datetime.now().isoformat(),
                            "type": "text_to_emoji"
                        })
                        save_history(history)
                        
                        st.success("✨ Translation completed!")
                        st.rerun()
                    else:
                        st.error("Translation failed. Please try again or check your API key.")
                        
                except ValueError as e:
                    st.error(f"Configuration error: {e}")
                    st.info("💡 Make sure your OpenAI API key is set in the .env file")
                except Exception as e:
                    logger.error(f"Translation error: {e}")
                    st.error("❌ Translation failed. Please try again later.")
        else:
            st.warning("⚠️ Please enter some text to translate.")
    
    st.markdown("---")
    st.markdown("### 🔄 Reverse Translation")
    emoji_input = st.text_input("Enter emojis to interpret:", placeholder="e.g. 🎉✈️🌍")
    
    if st.button("🔄 Interpret Emojis", use_container_width=True, disabled=not emoji_input.strip()):
        if emoji_input.strip():
            with st.spinner("🤖 Interpreting emojis..."):
                try:
                    translator = EmojiTranslator()
                    text_result = translator.translate_reverse(emoji_input.strip())
                    
                    if text_result and not text_result.startswith("Error:"):
                        # Get emoji codes for the input emojis
                        emoji_codes = get_emoji_codes(emoji_input.strip())
                        emoji_codes_str = ", ".join(emoji_codes)

                        # Update session state
                        st.session_state.translation_result = text_result
                        st.session_state.emoji_codes = emoji_codes_str

                        # Add to history
                        history = load_history()
                        history.append({
                            "input": emoji_input.strip(),
                            "translation": text_result,
                            "emoji_codes": emoji_codes,
                            "timestamp": datetime.now().isoformat(),
                            "type": "emoji_to_text"
                        })
                        save_history(history)
                        
                        st.success("✨ Interpretation completed!")
                        st.rerun()
                    else:
                        st.error("Interpretation failed. Please try again or check your API key.")
                        
                except ValueError as e:
                    st.error(f"Configuration error: {e}")
                    st.info("💡 Make sure your OpenAI API key is set in the .env file")
                except Exception as e:
                    logger.error(f"Reverse translation error: {e}")
                    st.error("❌ Interpretation failed. Please try again later.")
        else:
            st.warning("⚠️ Please enter some emojis to interpret.")

# Main content area
st.markdown('<div class="title">✨ Emoji Mood Translator ✨</div>', unsafe_allow_html=True)

# Update translation box display
if st.session_state.translation_result:
    emoji_codes_section = ""
    if st.session_state.emoji_codes:
        emoji_codes_section = f'<div class="emoji-codes"><span class="code-label">Emoji Codes:</span> {st.session_state.emoji_codes}</div>'
    
    st.markdown(
        f'''<div class="translation-box">
            <div class="emoji-result">
                {st.session_state.translation_result}
            </div>
            {emoji_codes_section}
        </div>''', 
        unsafe_allow_html=True
    )
    
    # Add copy buttons below the result
    if st.session_state.translation_result:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Result", key="copy_result"):
                copy_to_clipboard_safe(st.session_state.translation_result, "Result copied!")
        with col2:
            if st.session_state.emoji_codes and st.button("📋 Copy Unicode", key="copy_unicode"):
                copy_to_clipboard_safe(st.session_state.emoji_codes, "Unicode codes copied!")
else:
    st.markdown(
        '''<div class="translation-box">
            <div class="emoji-result">✨ Enter text to translate ✨</div>
        </div>''',
        unsafe_allow_html=True
    )

# Add JavaScript for copy callback
st.markdown("""
    <script>
        window.streamlitCopy = (type) => {
            window.streamlit.setComponentValue({
                type: 'copy',
                data: type
            });
        }
    </script>
""", unsafe_allow_html=True)

# Handle copy events
if st.session_state.get('component_value'):
    value = st.session_state.component_value
    if value.get('type') == 'copy':
        if value['data'] == 'emoji':
            copy_to_clipboard(st.session_state.translation_result, "Emoji copied!")
        elif value['data'] == 'codes':
            copy_to_clipboard(st.session_state.emoji_codes, "Codes copied!")

# Load user history
user_history = load_history()

# Show history in main area
st.subheader("🕘 Translation History")

if user_history:
    # Add controls for history
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search history:", 
                                   key="search_history", 
                                   help="Search through your translation history",
                                   placeholder="Search translations...")
    
    with col2:
        show_count = st.selectbox("Show:", [10, 25, 50], key="show_count")
    
    with col3:
        if st.button("🗑️ Clear All", help="Clear entire history"):
            st.session_state.confirm_clear = True

    # Confirmation dialog for clearing history
    if st.session_state.get('confirm_clear', False):
        st.warning("⚠️ This will delete all your translation history. Are you sure?")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✅ Yes, clear all"):
                save_history([])  # Save empty history
                st.session_state.confirm_clear = False
                st.success("🗑️ History cleared!")
                st.rerun()
        with col_no:
            if st.button("❌ Cancel"):
                st.session_state.confirm_clear = False
                st.rerun()

    # Filter and display history
    filtered_history = user_history
    if search_query:
        filtered_history = [
            item for item in user_history 
            if search_query.lower() in item['input'].lower() 
            or search_query.lower() in item['translation'].lower()
        ]
    
    # Show recent items
    recent_history = list(reversed(filtered_history[-show_count:]))
    
    if recent_history:
        for i, item in enumerate(recent_history):
            is_emoji_to_text = item.get('type') == 'emoji_to_text'
            timestamp = item.get('timestamp', '')
            
            # Format timestamp
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    time_str = dt.strftime("%m/%d %H:%M")
                except:
                    time_str = ""
            else:
                time_str = ""
            
            # Create expandable history item
            with st.expander(f"{'📖' if is_emoji_to_text else '😊'} {item['input'][:30]}{'...' if len(item['input']) > 30 else ''} {time_str}"):
                col_content, col_copy = st.columns([4, 1])
                
                with col_content:
                    st.write(f"**{'Emojis' if is_emoji_to_text else 'Input'}:** {item['input']}")
                    st.write(f"**{'Meaning' if is_emoji_to_text else 'Translation'}:** {item['translation']}")
                    
                    if item.get('emoji_codes'):
                        st.caption(f"**Unicode:** {', '.join(item['emoji_codes'][:5])}{'...' if len(item['emoji_codes']) > 5 else ''}")
                
                with col_copy:
                    if st.button("📋", key=f"copy_{i}", help="Copy result"):
                        copy_to_clipboard_safe(item['translation'], "Copied!")
    else:
        st.info("🔍 No results found for your search.")
else:
    st.info("📝 No translation history yet. Your translations will appear here after you use the app!")
