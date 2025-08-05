# Tether — AI Voice Conversation Platform API

Welcome to **Tether**, the backend API powering immersive, real-time AI conversations with the voices of people you care about. Tether enables users to upload voice samples of relatives, friends, or even themselves — and then engage in conversations with AI that responds using those familiar voices.

---

## 🧠 About Tether

Choosing the right voice can make all the difference when it comes to emotional connection. **Tether** combines voice cloning, real-time AI inference, and seamless streaming to create personalized, natural conversations powered by modern LLMs and TTS (Text-to-Speech) engines.

Whether you want to:

- Preserve the voice of a loved one,
- Talk with an AI-powered memory,
- Create engaging experiences using custom voices,

**Tether** is built to support it with speed, privacy, and quality.

---

## ⚙️ Core Features

- 🎙️ **Voice Upload**  
  Upload voice samples to clone or synthesize voices of real people.

- 💬 **Real-time AI Conversation**  
  Chat with AI that responds instantly using the cloned voice.

- 🔊 **Seamless Text-to-Speech (TTS)**  
  Ultra-low-latency audio generation with emotional tone control.

- 🧑‍🤝‍🧑 **Multi-Voice Switching**  
  Users can talk to multiple AI agents with different voices.

- ☁️ **Cloud-ready, Scalable API**  
  Designed with scalability and performance in mind for production use.

---

## 🛠️ Tech Stack

- **Python** + **FastAPI / Django**
- **PostgreSQL** / **Redis**
- **LLM**: OpenAI GPT / Mixtral / Local models (flexible)
- **Voice Cloning**: ElevenLabs / XTTS / Bark
- **TTS Streaming**: WebRTC / HTTP Live Streaming
- **Frontend** (planned): Next.js + WebSockets + Web Audio API

---

## 📦 API Modules (Planned)

| Module             | Description |
|--------------------|-------------|
| `auth`             | User registration, login, and token auth |
| `voices`           | Upload, manage, and synthesize user-submitted voice samples |
| `chat`             | Real-time chat endpoint for AI interaction |
| `audio_stream`     | Streaming TTS output for fast client playback |
| `conversations`    | Save, replay, and organize past conversations |

---

## Getting Started

### Prerequisites

- Python 3.11+  
- pip  
- Virtualenv (recommended)  
- PostgreSQL or another database  

### Installation

1. Clone the repository  

   ```bash
   git clone https://github.com/selim-reza-UITS/07_tether.git
   cd < cloned folder >
    ```

2. Create and activate a virtual environment

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```
3. Install dependencies

   ```bash
   pip install -r requirements.txt
    ```
4. Configure your database settings in settings.py or via environment variables.
5. Apply migrations:

    ```bash
    python manage.py migrate

    ```
6. Run the development server

    ```bash
    python manage.py runserver
    ```

# API Documentation

Swagger/OpenAPI documentation is available at:

    http://127.0.0.1:8000/

# Contribution
Contributions and suggestions are welcome! Please fork the repository and open a pull request with your proposed changes.

# Contact
For questions or feedback, please reach out at [selim.reza.uits@gmail.com].

# Happy voice contacting with people! 🎁✨
