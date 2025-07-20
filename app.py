import streamlit as st
from translator import EmojiTranslator
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import pyperclip  # Add this import for clipboard operations

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    if st.button("🔁 Translate to Emoji", use_container_width=True):
        if user_input:
            try:
                translator = EmojiTranslator()
                emoji_result = translator.translate(user_input)
                
                # Get emoji codes, excluding ZWJ characters
                emoji_codes = [f"U+{ord(c):X}" for c in emoji_result if ord(c) != 0x200D]
                emoji_codes_str = ", ".join(emoji_codes)

                # Update session state
                st.session_state.translation_result = emoji_result
                st.session_state.emoji_codes = emoji_codes_str

                # Save to history with emoji codes
                try:
                    with open("storage.json", "r") as f:
                        user_history = json.load(f)
                except FileNotFoundError:
                    user_history = []

                user_history.append({
                    "input": user_input,
                    "translation": emoji_result,
                    "emoji_codes": emoji_codes
                })
                with open("storage.json", "w") as f:
                    json.dump(user_history, f, indent=4)
                
                # Use st.rerun() instead of experimental_rerun
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred during translation: {e}")
        else:
            st.warning("Please enter some text to translate.")
    
    st.markdown("---")
    st.markdown("### 🔄 Reverse Translation")
    emoji_input = st.text_input("Enter emojis to interpret:", placeholder="e.g. 🎉✈️🌍")
    
    if st.button("🔄 Interpret Emojis", use_container_width=True):
        if emoji_input:
            try:
                translator = EmojiTranslator()
                text_result = translator.translate_reverse(emoji_input)
                
                # Get emoji codes for the input emojis
                emoji_codes = [f"U+{ord(c):X}" for c in emoji_input if ord(c) != 0x200D]
                emoji_codes_str = ", ".join(emoji_codes)

                # Update session state with both interpretation and codes
                st.session_state.translation_result = text_result
                st.session_state.emoji_codes = emoji_codes_str

                # Add to history with reversed flag and emoji codes
                try:
                    with open("storage.json", "r") as f:
                        user_history = json.load(f)
                except FileNotFoundError:
                    user_history = []

                user_history.append({
                    "input": emoji_input,
                    "translation": text_result,
                    "type": "reverse",
                    "emoji_codes": emoji_codes
                })
                with open("storage.json", "w") as f:
                    json.dump(user_history, f, indent=4)

            except Exception as e:
                st.error(f"An error occurred during interpretation: {e}")
        else:
            st.warning("Please enter some emojis to interpret.")

# Main content area
st.markdown('<div class="title">✨ Emoji Mood Translator ✨</div>', unsafe_allow_html=True)

# Update translation box display
if st.session_state.translation_result:
    st.markdown(
        f'''<div class="translation-box">
            <div class="emoji-result">
                {st.session_state.translation_result}
                <span class="tooltip">
                    <span class="copy-icon" onclick="navigator.clipboard.writeText('{st.session_state.translation_result}')">
                        <i class="fas fa-copy"></i>
                    </span>
                </span>
            </div>
            {f'<div class="emoji-codes"><span class="code-label">Emoji Codes:</span> {st.session_state.emoji_codes}<span class="tooltip"><span class="copy-icon" onclick="navigator.clipboard.writeText(\'{st.session_state.emoji_codes}\')"><i class="fas fa-copy"></i></span></span></div>' if st.session_state.emoji_codes else ''}
        </div>''', 
        unsafe_allow_html=True
    )
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
try:
    with open("storage.json", "r") as f:
        user_history = json.load(f)
except FileNotFoundError:
    user_history = []

# Show history in main area
st.subheader("🕘 Translation History")

# Add search box for history
search_query = st.text_input("🔍 Search history:", key="search_history", help="Search through your translation history")

# Add clear history button in a column layout
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🗑️ Clear"):
        user_history = []
        with open("storage.json", "w") as f:
            json.dump(user_history, f, indent=4)

# Modify history display to include search
if user_history:
    filtered_history = user_history
    if search_query:
        filtered_history = [
            item for item in user_history 
            if search_query.lower() in item['input'].lower() 
            or search_query.lower() in item['translation'].lower()
        ]
    
    for item in reversed(filtered_history[-10:]):
        is_reverse = item.get('type') == 'reverse'
        st.markdown(f"""
            <div class="history-box">
                <b>{'Emojis' if is_reverse else 'Input'}:</b> {item['input']}<br>
                <b>{'Meaning' if is_reverse else 'Translation'}:</b> {item['translation']}<br>
                {'' if is_reverse else f'<small><b>Emoji Codes:</b> {", ".join(item.get("emoji_codes", []))}</small>'}
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("No translation history yet. Your results will appear here.")
