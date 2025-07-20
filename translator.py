import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class EmojiTranslator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_engine = "gpt-3.5-turbo"
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

    def translate(self, text):
        try:
            messages = self.few_shot_examples.copy()
            messages.append({"role": "user", "content": f"Translate this to emoji: {text}"})
            
            response = self.client.chat.completions.create(
                model=self.model_engine,
                messages=messages,
                max_tokens=10,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Debug - Error: {str(e)}")
            return f"Error: {str(e)}"

    def translate_reverse(self, emojis):
        try:
            messages = self.reverse_examples.copy()
            messages.append({"role": "user", "content": f"Interpret these emojis: {emojis}"})
            
            response = self.client.chat.completions.create(
                model=self.model_engine,
                messages=messages,
                max_tokens=50,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Debug - Error: {str(e)}")
            return f"Error: {str(e)}"
