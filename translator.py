import os
import logging
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class EmojiTranslator:
    """
    A class to translate text to emojis and vice versa using OpenAI's API.
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize the EmojiTranslator with OpenAI client and model configuration.
        
        Args:
            model: The OpenAI model to use for translations (default: gpt-3.5-turbo)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
            
        self.client = OpenAI(api_key=api_key)
        self.model_engine = model
        self.few_shot_examples = [
            {"role": "system", "content": "You are an emoji translator. You must respond only with emojis, no text. Combine 2-6 emojis to convey complex emotions and situations accurately."},
            {"role": "user", "content": "I'm feeling great today"},
            {"role": "assistant", "content": "😄🌟✨"},
            {"role": "user", "content": "Just completed my project"},
            {"role": "assistant", "content": "✅🎉🏆"},
            {"role": "user", "content": "Learning to code"},
            {"role": "assistant", "content": "👩‍💻📚✨"}
        ]
        self.reverse_examples = [
            {"role": "system", "content": "You are an emoji interpreter. Convert emojis into descriptive text that captures their combined meaning."},
            {"role": "user", "content": "🎉✈️🌍🏡💼😄"},
            {"role": "assistant", "content": "I got a new job and I'm moving abroad!"},
            {"role": "user", "content": "😫📚💻⏰😵‍💫☕"},
            {"role": "assistant", "content": "I feel tired and stressed with school work."}
        ]

    def translate(self, text: str) -> str:
        """
        Translate text to emojis using OpenAI's API.
        
        Args:
            text: The text to translate to emojis
            
        Returns:
            String containing emojis representing the input text
        """
        if not text or not text.strip():
            return "❓"  # Question mark emoji for empty input
            
        try:
            messages = self.few_shot_examples.copy()
            messages.append({"role": "user", "content": f"Translate this to emoji: {text.strip()}"})
            
            response = self.client.chat.completions.create(
                model=self.model_engine,
                messages=messages,
                max_tokens=15,  # Increased for better emoji combinations
                temperature=0.5,
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"Successfully translated text to emojis: {text[:50]}... -> {result}")
            return result if result else "😊"  # Default emoji if empty response
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error during translation: {str(e)}")
            return "❌🤖"  # Error emoji combination
        except Exception as e:
            logger.error(f"Unexpected error during translation: {str(e)}")
            return "❌"

    def translate_reverse(self, emojis: str) -> str:
        """
        Translate emojis back to descriptive text using OpenAI's API.
        
        Args:
            emojis: The emojis to translate to text
            
        Returns:
            String describing the meaning of the emojis
        """
        if not emojis or not emojis.strip():
            return "No emojis provided"
            
        try:
            messages = self.reverse_examples.copy()
            messages.append({"role": "user", "content": f"Interpret these emojis: {emojis.strip()}"})
            
            response = self.client.chat.completions.create(
                model=self.model_engine,
                messages=messages,
                max_tokens=100,  # Increased for better descriptions
                temperature=0.7,
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"Successfully translated emojis to text: {emojis} -> {result[:50]}...")
            return result if result else "Unable to interpret these emojis"
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error during reverse translation: {str(e)}")
            return "Error: Unable to connect to translation service"
        except Exception as e:
            logger.error(f"Unexpected error during reverse translation: {str(e)}")
            return "Error: Translation failed"
