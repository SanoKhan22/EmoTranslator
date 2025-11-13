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

# Theme customization - Modern Design Enhancement
st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --primary-bg: #0D1117;
            --secondary-bg: #161B22;
            --accent-bg: #21262D;
            --primary-text: #F0F6FC;
            --secondary-text: #8B949E;
            --accent-color: #58A6FF;
            --success-color: #3FB950;
            --warning-color: #F85149;
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
            --shadow-lg: 0 8px 25px rgba(0,0,0,0.5);
            --border-radius: 12px;
        }
        
        .main {
            background: var(--primary-bg);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .title {
            font-size: 3.5rem;
            text-align: center;
            background: var(--gradient-1);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            text-shadow: none;
            letter-spacing: -0.02em;
            animation: titleGlow 3s ease-in-out infinite alternate;
        }
        
        @keyframes titleGlow {
            from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.3)); }
            to { filter: drop-shadow(0 0 20px rgba(118, 75, 162, 0.5)); }
        }
        
        .subtitle {
            font-size: 1.8rem;
            color: var(--primary-text);
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        
        .translation-box {
            background: var(--secondary-bg);
            background-image: var(--gradient-3);
            padding: 2.5rem;
            border-radius: var(--border-radius);
            font-size: 2.5rem;
            text-align: center;
            border: 2px solid transparent;
            background-clip: padding-box;
            box-shadow: var(--shadow-lg);
            color: var(--primary-text);
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .translation-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--gradient-1);
            opacity: 0.1;
            z-index: -1;
        }
        
        .translation-box:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg), 0 0 30px rgba(102, 126, 234, 0.3);
        }
        
        .emoji-result {
            margin-bottom: 1rem;
            filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));
            animation: emojiPulse 2s ease-in-out infinite alternate;
        }
        
        @keyframes emojiPulse {
            from { transform: scale(1); }
            to { transform: scale(1.02); }
        }
        
        .emoji-codes {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: var(--secondary-text);
            margin-top: 1rem;
            background: rgba(88, 166, 255, 0.1);
            padding: 0.8rem;
            border-radius: 8px;
            border-left: 3px solid var(--accent-color);
            backdrop-filter: blur(10px);
        }
        
        .code-label {
            color: var(--accent-color);
            font-weight: 500;
        }
        
        .history-box {
            background: var(--secondary-bg);
            padding: 1.2rem;
            border-radius: var(--border-radius);
            margin-bottom: 1rem;
            color: var(--primary-text);
            border: 1px solid var(--accent-bg);
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }
        
        .history-box:hover {
            border-color: var(--accent-color);
            box-shadow: var(--shadow-md);
        }
        
        .stTextArea textarea {
            font-size: 1.1rem !important;
            padding: 1rem !important;
            border-radius: var(--border-radius) !important;
            border: 2px solid var(--accent-bg) !important;
            min-height: 120px !important;
            width: 100% !important;
            font-family: 'Inter', sans-serif !important;
            background-color: var(--secondary-bg) !important;
            color: var(--primary-text) !important;
            transition: all 0.2s ease !important;
        }
        
        .stTextArea textarea:focus {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1) !important;
        }
        
        .stButton button {
            background: var(--gradient-1) !important;
            color: white !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            display: block !important;
            margin: 1.5rem auto !important;
            padding: 0.8rem 2rem !important;
            font-size: 1rem !important;
            border: none !important;
            border-radius: var(--border-radius) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        .stButton button:hover {
            background: var(--gradient-2) !important;
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        .stButton button:disabled {
            opacity: 0.5 !important;
            cursor: not-allowed !important;
            transform: none !important;
        }
        
        .copy-icon {
            color: var(--accent-color) !important;
            cursor: pointer !important;
            padding: 0.5rem !important;
            border-radius: 8px !important;
            display: inline-flex !important;
            align-items: center !important;
            transition: all 0.2s ease !important;
            margin-left: 0.8rem !important;
            font-size: 1rem !important;
            background: rgba(88, 166, 255, 0.1) !important;
        }
        
        .copy-icon:hover {
            background: rgba(88, 166, 255, 0.2) !important;
            transform: scale(1.1) !important;
        }
        
        .tooltip:hover::after {
            background: var(--accent-bg);
            color: var(--primary-text);
            padding: 0.5rem 0.8rem;
            border-radius: 6px;
            font-size: 0.8rem;
            border: 1px solid var(--accent-color);
        }
        
        /* Enhanced Sidebar Styling */
        .css-1d391kg {
            background: var(--secondary-bg) !important;
            border-right: 1px solid var(--accent-bg) !important;
        }
        
        /* Selectbox Styling */
        .stSelectbox > div > div {
            background: var(--secondary-bg) !important;
            border: 2px solid var(--accent-bg) !important;
            border-radius: var(--border-radius) !important;
            color: var(--primary-text) !important;
        }
        
        .stSelectbox > div > div:focus-within {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1) !important;
        }
        
        /* Success/Error Messages */
        .stSuccess {
            background: rgba(63, 185, 80, 0.1) !important;
            border: 1px solid var(--success-color) !important;
            border-radius: var(--border-radius) !important;
        }
        
        .stError {
            background: rgba(248, 81, 73, 0.1) !important;
            border: 1px solid var(--warning-color) !important;
            border-radius: var(--border-radius) !important;
        }
        
        /* Spinner Animation */
        .stSpinner > div {
            border-top-color: var(--accent-color) !important;
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background: var(--secondary-bg) !important;
            border-radius: var(--border-radius) !important;
            border: 1px solid var(--accent-bg) !important;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: var(--accent-color) !important;
        }
        
        /* Placeholder and disabled text */
        ::placeholder {
            color: var(--secondary-text) !important;
        }
        
        .disabled {
            color: var(--secondary-text) !important;
        }
        
        /* Loading Animation for Results */
        .result-loading {
            animation: resultSlideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes resultSlideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Character Counter Styling */
        .char-counter {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--secondary-text);
            text-align: right;
            margin-top: 0.3rem;
        }
        
        .char-counter.warning {
            color: var(--warning-color);
        }
        
        .char-counter.danger {
            color: var(--warning-color);
            font-weight: 500;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .title {
                font-size: 2.5rem !important;
                margin-bottom: 1.5rem !important;
            }
            
            .translation-box {
                font-size: 2rem !important;
                padding: 1.5rem !important;
            }
            
            .stTextArea textarea {
                font-size: 1rem !important;
            }
        }
        
        @media (max-width: 480px) {
            .title {
                font-size: 2rem !important;
            }
            
            .translation-box {
                font-size: 1.5rem !important;
                padding: 1rem !important;
            }
        }
        
        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Enhanced focus states */
        *:focus {
            outline: 2px solid var(--accent-color);
            outline-offset: 2px;
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
    
    # Display character counter in sidebar with enhanced styling
    counter_class = (
        "char-counter danger" if chars_left < 20 else 
        "char-counter warning" if chars_left < 40 else 
        "char-counter"
    )
    
    st.markdown(f'<div class="{counter_class}">{chars_left} characters remaining</div>', unsafe_allow_html=True)
    
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

# Main content area with interactive demo header
st.markdown('''
<div class="title">✨ Emoji Mood Translator ✨</div>

<!-- Interactive Demo Section -->
<div class="demo-header" id="demoHeader">
    <div class="demo-input">
        <span class="demo-label">💭 Example:</span>
        <span class="demo-typing" id="demoTyping"></span>
        <span class="demo-cursor" id="demoCursor">|</span>
    </div>
    <div class="demo-arrow" id="demoArrow">
        <span class="thinking-dots" id="demoThinking">🤖✨</span>
        <span class="magic-transform" id="demoTransform">➡️</span>
    </div>
    <div class="demo-result" id="demoResult"></div>
</div>

<div style="text-align: center; margin-bottom: 2rem; margin-top: 1rem;">
    <p style="color: var(--secondary-text); font-size: 1rem; font-weight: 300; margin: 0; opacity: 0.8;">
        See the magic happen above, then try it yourself below! ⬇️
    </p>
</div>

<script>
    const demoExamples = [
        { text: "I'm so excited today!", emoji: "🎉😊✨" },
        { text: "Feeling creative", emoji: "🎨💡🌟" },
        { text: "Love this weather", emoji: "☀️🌈💕" },
        { text: "Tired but happy", emoji: "😴😊💤" },
        { text: "Missing home", emoji: "🏠💙😢" }
    ];

    let demoIndex = 0;
    let demoIsTyping = false;

    function startDemoTyping() {
        const typingElement = document.getElementById('demoTyping');
        const cursor = document.getElementById('demoCursor');
        const thinking = document.getElementById('demoThinking');
        const transform = document.getElementById('demoTransform');
        const result = document.getElementById('demoResult');

        if (!typingElement) return;

        const currentExample = demoExamples[demoIndex];
        typingElement.innerHTML = '';
        result.innerHTML = '';
        thinking.style.display = 'inline';
        transform.style.display = 'none';
        
        let i = 0;
        demoIsTyping = true;

        function typeChar() {
            if (i < currentExample.text.length) {
                typingElement.innerHTML += currentExample.text.charAt(i);
                i++;
                setTimeout(typeChar, 80);
            } else {
                demoIsTyping = false;
                // Show thinking
                setTimeout(() => {
                    thinking.style.display = 'none';
                    transform.style.display = 'inline';
                    setTimeout(() => {
                        transform.style.display = 'none';
                        result.innerHTML = currentExample.emoji;
                        result.style.animation = 'demoEmojiPop 0.5s ease';
                        setTimeout(() => {
                            demoIndex = (demoIndex + 1) % demoExamples.length;
                            setTimeout(startDemoTyping, 2500);
                        }, 2000);
                    }, 800);
                }, 1500);
            }
        }
        typeChar();
    }

    // Start demo after page loads
    setTimeout(startDemoTyping, 2000);
</script>

<style>
    .demo-header {
        background: rgba(33, 38, 45, 0.6);
        border: 1px solid rgba(88, 166, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem auto;
        max-width: 600px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .demo-header:hover {
        border-color: rgba(88, 166, 255, 0.5);
        box-shadow: 0 5px 20px rgba(88, 166, 255, 0.1);
    }
    
    .demo-input {
        font-size: 1.2rem;
        margin-bottom: 1rem;
        min-height: 1.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .demo-label {
        color: var(--secondary-text);
        font-weight: 500;
    }
    
    .demo-typing {
        color: var(--primary-text);
        font-weight: 500;
        min-width: 200px;
        text-align: left;
    }
    
    .demo-cursor {
        color: var(--accent-color);
        animation: demoBlink 1s infinite;
        font-weight: bold;
    }
    
    @keyframes demoBlink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    .demo-arrow {
        margin: 1rem 0;
        font-size: 1.5rem;
        min-height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .thinking-dots {
        animation: demoThinking 1.5s ease-in-out infinite;
    }
    
    @keyframes demoThinking {
        0%, 60%, 100% { transform: scale(1); }
        30% { transform: scale(1.1); }
    }
    
    .magic-transform {
        animation: demoSlide 0.8s ease-in-out;
    }
    
    @keyframes demoSlide {
        0% { transform: translateX(-20px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    .demo-result {
        font-size: 2.5rem;
        min-height: 3rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    @keyframes demoEmojiPop {
        0% { transform: scale(0.5); opacity: 0; }
        50% { transform: scale(1.1); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Make demo responsive */
    @media (max-width: 768px) {
        .demo-header {
            margin: 1rem;
            padding: 1rem;
        }
        
        .demo-input {
            font-size: 1rem;
            flex-direction: column;
            gap: 0.3rem;
        }
        
        .demo-typing {
            min-width: auto;
            text-align: center;
        }
        
        .demo-result {
            font-size: 2rem;
        }
    }
</style>
''', unsafe_allow_html=True)

# Update translation box display
if st.session_state.translation_result:
    emoji_codes_section = ""
    if st.session_state.emoji_codes:
        emoji_codes_section = f'<div class="emoji-codes"><span class="code-label">Emoji Codes:</span> {st.session_state.emoji_codes}</div>'
    
    st.markdown(
        f'''<div class="translation-box result-loading">
            <div class="emoji-result">
                {st.session_state.translation_result}
            </div>
            {emoji_codes_section}
        </div>''', 
        unsafe_allow_html=True
    )
    
    # Add copy buttons below the result with enhanced styling
    if st.session_state.translation_result:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                if st.button("📋 Copy Result", key="copy_result", use_container_width=True):
                    copy_to_clipboard_safe(st.session_state.translation_result, "✨ Result copied to clipboard!")
            with subcol2:
                if st.session_state.emoji_codes and st.button("� Copy Unicode", key="copy_unicode", use_container_width=True):
                    copy_to_clipboard_safe(st.session_state.emoji_codes, "✨ Unicode codes copied!")
else:
    st.markdown(
        '''<div class="translation-box">
            <div class="emoji-result">✨ Enter text to translate ✨</div>
        </div>''',
        unsafe_allow_html=True
    )

# Add Particle Background and Enhanced JavaScript
st.markdown("""
    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        // Particle background
        particlesJS("particles-js", {
            "particles": {
                "number": {"value": 50, "density": {"enable": true, "value_area": 800}},
                "color": {"value": "#58A6FF"},
                "shape": {"type": "circle"},
                "opacity": {"value": 0.1, "random": true},
                "size": {"value": 3, "random": true},
                "line_linked": {"enable": true, "distance": 150, "color": "#58A6FF", "opacity": 0.05, "width": 1},
                "move": {"enable": true, "speed": 1, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false}
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {"onhover": {"enable": true, "mode": "repulse"}, "onclick": {"enable": true, "mode": "push"}, "resize": true},
                "modes": {"grab": {"distance": 140, "line_linked": {"opacity": 1}}, "bubble": {"distance": 200, "size": 40, "duration": 2, "opacity": 8, "speed": 3}, "repulse": {"distance": 100, "duration": 0.4}, "push": {"particles_nb": 2}, "remove": {"particles_nb": 2}}
            },
            "retina_detect": true
        });
        
        // Copy functionality
        window.streamlitCopy = (type) => {
            window.streamlit.setComponentValue({
                type: 'copy',
                data: type
            });
        }
        
        // Success animation
        function showSuccessAnimation() {
            const body = document.querySelector('.main');
            body.style.transform = 'scale(1.01)';
            setTimeout(() => {
                body.style.transform = 'scale(1)';
            }, 200);
        }
    </script>
    
    <style>
        #particles-js {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: var(--primary-bg);
        }
        
        .main > .block-container {
            position: relative;
            z-index: 1;
        }
    </style>
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

# Show history in main area with enhanced styling
st.markdown('''
<div style="margin-top: 3rem;">
    <h3 style="color: var(--primary-text); font-family: 'Inter', sans-serif; font-weight: 600; margin-bottom: 1.5rem;">
        🕘 Translation History
    </h3>
</div>
''', unsafe_allow_html=True)

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
