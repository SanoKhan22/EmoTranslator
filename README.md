# 🎭 EmoTranslator - Emoji Mood Translator

A beautiful Streamlit web application that translates text emotions into emojis and vice versa using OpenAI's GPT API. Express your feelings through emojis or decode emoji combinations back to text!

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![OpenAI](https://img.shields.io/badge/openai-v1.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **🔄 Bidirectional Translation**: Convert text to emojis and emojis back to text
- **🎨 Beautiful Dark Theme**: Modern, eye-friendly interface with custom styling
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🕘 Translation History**: Keep track of all your translations with search functionality
- **📋 One-Click Copy**: Copy results to clipboard instantly
- **🎯 Multiple Translation Styles**: Choose between Standard, Minimal, and Expressive modes
- **🔍 Smart Search**: Find past translations quickly with built-in search
- **📊 Unicode Display**: See Unicode codes for all emojis
- **⚡ Real-time Feedback**: Loading indicators and user-friendly error messages

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SanoKhan22/EmoTranslator.git
   cd EmoTranslator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required: OpenAI API Configuration
OPENAI_API_KEY=sk-your-api-key-here

# Optional: Model Configuration (default: gpt-3.5-turbo)
OPENAI_MODEL=gpt-3.5-turbo

# Optional: Application Settings
MAX_HISTORY_ITEMS=50
MAX_INPUT_CHARACTERS=200
```

### Translation Styles

- **Standard**: Basic emotion-to-emoji translation (2-4 emojis)
- **Minimal**: Simple, concise translations (1-2 emojis)
- **Expressive**: Detailed emotional combinations (3-6 emojis)

## 📁 Project Structure

```
EmoTranslator/
├── app.py              # Main Streamlit application
├── translator.py       # EmojiTranslator class with OpenAI integration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .gitignore         # Git ignore rules
├── storage.json       # Translation history (auto-generated)
├── test.py           # Basic styling tests
├── README.md         # This file
└── tests/            # Test files (optional)
    └── test_translator.py
```

## 🎯 Usage Examples

### Text to Emoji Translation
```
Input: "I'm so excited for vacation!"
Output: 🎉✈️🌴😄

Input: "Feeling stressed about work"
Output: 😰💼📊⏰
```

### Emoji to Text Translation
```
Input: 🎂🎉🎈🥳
Output: "It's someone's birthday and we're celebrating!"

Input: ☕📚💻😴
Output: "Late night studying with coffee, feeling tired"
```

## 🧪 Running Tests

Create and run basic tests:

```bash
# Install pytest
pip install pytest

# Run tests
pytest tests/
```

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your `OPENAI_API_KEY` in the Streamlit Cloud secrets

### Heroku Deployment

1. Create a `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\\
   [server]\\n\\
   headless = true\\n\\
   port = $PORT\\n\\
   enableCORS = false\\n\\
   \\n\\
   " > ~/.streamlit/config.toml
   ```

3. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t emotranslator .
docker run -p 8501:8501 --env-file .env emotranslator
```

## 🔧 Development

### Setting up Development Environment

1. **Clone and install in development mode**
   ```bash
   git clone https://github.com/SanoKhan22/EmoTranslator.git
   cd EmoTranslator
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If you create this for dev dependencies
   ```

2. **Install pre-commit hooks** (optional)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Code Style

This project follows Python best practices:
- Type hints for better code documentation
- Comprehensive error handling
- Logging for debugging
- Modular code structure

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 📝 API Usage and Costs

This application uses OpenAI's API. Be aware of the costs:
- GPT-3.5-turbo: ~$0.002 per 1K tokens
- Each translation uses approximately 50-150 tokens
- Monitor your usage on the [OpenAI dashboard](https://platform.openai.com/usage)

## 🛡️ Security

- Never commit your `.env` file or API keys
- Use environment variables for all sensitive configuration
- Regularly rotate your API keys
- Monitor API usage for unexpected spikes

## 📊 Features Roadmap

- [ ] **Multiple Language Support**: Translate emotions in different languages
- [ ] **Custom Emoji Sets**: Create and use custom emoji combinations
- [ ] **Batch Processing**: Translate multiple texts at once
- [ ] **Export History**: Export translation history as CSV/JSON
- [ ] **Emoji Analytics**: Statistics on most used emojis
- [ ] **Social Sharing**: Share translations directly to social media
- [ ] **Voice Input**: Speak your emotions for translation
- [ ] **Emoji Reactions**: Rate translations for improved AI training

## ❓ Troubleshooting

### Common Issues

**"Import errors when running"**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**"OpenAI API key not found"**
- Check your `.env` file exists and contains `OPENAI_API_KEY=your-key`
- Ensure the `.env` file is in the same directory as `app.py`

**"Streamlit not found"**
- Install Streamlit: `pip install streamlit>=1.28.0`

**"Translation fails"**
- Verify your OpenAI API key is valid and has credits
- Check your internet connection
- Look at the error logs in the Streamlit interface

### Getting Help

- 📧 Open an issue on GitHub
- 💬 Check existing issues for solutions
- 📖 Read the OpenAI API documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [OpenAI](https://openai.com/) for the powerful GPT API
- The emoji community for making digital communication more expressive

## 📈 Version History

- **v2.0.0** (Current) - Complete rewrite with modern Python practices, enhanced UI, better error handling
- **v1.0.0** - Initial release with basic text-to-emoji translation

---

Made with ❤️ by [SanoKhan22](https://github.com/SanoKhan22)

**Star ⭐ this repo if you find it helpful!**