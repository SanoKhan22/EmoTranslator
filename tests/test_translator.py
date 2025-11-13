"""
Tests for the EmojiTranslator class.
"""

import pytest
import os
from unittest.mock import Mock, patch
from translator import EmojiTranslator


class TestEmojiTranslator:
    """Test cases for the EmojiTranslator class."""

    def test_init_without_api_key(self):
        """Test that initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is required"):
                EmojiTranslator()

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_init_with_api_key(self):
        """Test successful initialization with API key."""
        translator = EmojiTranslator()
        assert translator.model_engine == "gpt-3.5-turbo"

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_init_with_custom_model(self):
        """Test initialization with custom model."""
        translator = EmojiTranslator(model="gpt-4")
        assert translator.model_engine == "gpt-4"

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('translator.OpenAI')
    def test_translate_empty_input(self, mock_openai):
        """Test translation with empty input."""
        translator = EmojiTranslator()
        
        # Test empty string
        result = translator.translate("")
        assert result == "❓"
        
        # Test whitespace only
        result = translator.translate("   ")
        assert result == "❓"

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('translator.OpenAI')
    def test_translate_success(self, mock_openai):
        """Test successful translation."""
        # Mock the OpenAI response
        mock_response = Mock()
        mock_response.choices[0].message.content.strip.return_value = "😊✨"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        translator = EmojiTranslator()
        result = translator.translate("I'm happy")
        
        assert result == "😊✨"
        mock_openai.return_value.chat.completions.create.assert_called_once()

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('translator.OpenAI')
    def test_translate_api_error(self, mock_openai):
        """Test translation with API error."""
        from openai import OpenAIError
        
        # Mock API error
        mock_openai.return_value.chat.completions.create.side_effect = OpenAIError("API Error")
        
        translator = EmojiTranslator()
        result = translator.translate("I'm happy")
        
        assert result == "❌🤖"

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('translator.OpenAI')
    def test_translate_reverse_empty_input(self, mock_openai):
        """Test reverse translation with empty input."""
        translator = EmojiTranslator()
        
        # Test empty string
        result = translator.translate_reverse("")
        assert result == "No emojis provided"
        
        # Test whitespace only
        result = translator.translate_reverse("   ")
        assert result == "No emojis provided"

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('translator.OpenAI')
    def test_translate_reverse_success(self, mock_openai):
        """Test successful reverse translation."""
        # Mock the OpenAI response
        mock_response = Mock()
        mock_response.choices[0].message.content.strip.return_value = "I'm feeling happy"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        translator = EmojiTranslator()
        result = translator.translate_reverse("😊✨")
        
        assert result == "I'm feeling happy"
        mock_openai.return_value.chat.completions.create.assert_called_once()

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('translator.OpenAI')
    def test_translate_reverse_api_error(self, mock_openai):
        """Test reverse translation with API error."""
        from openai import OpenAIError
        
        # Mock API error
        mock_openai.return_value.chat.completions.create.side_effect = OpenAIError("API Error")
        
        translator = EmojiTranslator()
        result = translator.translate_reverse("😊✨")
        
        assert result == "Error: Unable to connect to translation service"

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('translator.OpenAI')
    def test_translate_empty_response(self, mock_openai):
        """Test translation with empty API response."""
        # Mock empty response
        mock_response = Mock()
        mock_response.choices[0].message.content.strip.return_value = ""
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        translator = EmojiTranslator()
        result = translator.translate("I'm happy")
        
        assert result == "😊"  # Default emoji for empty response

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('translator.OpenAI')
    def test_translate_reverse_empty_response(self, mock_openai):
        """Test reverse translation with empty API response."""
        # Mock empty response
        mock_response = Mock()
        mock_response.choices[0].message.content.strip.return_value = ""
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        translator = EmojiTranslator()
        result = translator.translate_reverse("😊✨")
        
        assert result == "Unable to interpret these emojis"


if __name__ == "__main__":
    pytest.main([__file__])