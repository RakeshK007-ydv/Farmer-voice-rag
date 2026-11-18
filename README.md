# 🌾 AI Voice Assistant for Farmers

An AI-powered agricultural assistant that helps farmers get information about wheat cultivation through voice and text questions.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant agricultural information and generate answers using Google's Gemini API.

## Features

- Voice-based question input.
- Punjabi and Hindi voice transcription.
- English, Hindi and Punjabi text questions.
- Agriculture knowledge retrieval using ChromaDB.
- Semantic search using text embeddings.
- Context-based AI answers using Gemini.
- Persistent vector database.

## Technologies Used

- Python
- Google Gemini API
- Gemini Embeddings
- ChromaDB
- Speech-to-Text
- SoundDevice
- SciPy

## Project Structure

```text
FARMER_STRUCTURE_VOICE/
│
├── Main.py
├── farmer_structure_voice.py
├── wheat.txt
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

The `farmer_database` folder is created automatically when the application runs.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd FARMER_STRUCTURE_VOICE
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.env` file in the project folder.

Add:

```env
GEMINI_API_KEY=your_actual_api_key
```

Never share your API key publicly.

## Run the Application

Execute:

```bash
python Main.py
```

Speak your agricultural question when prompted.

The application records your question, converts speech into text, retrieves relevant information from ChromaDB and generates an AI-powered answer.

## How It Works

```text
Farmer's Voice
      |
      v
Speech-to-Text
      |
      v
Question Embedding
      |
      v
ChromaDB Similarity Search
      |
      v
Relevant Agricultural Information
      |
      v
Gemini AI
      |
      v
Generated Answer
```

## Current Knowledge Base

The current knowledge base focuses on wheat cultivation, including:

- Wheat growing period.
- Irrigation requirements.
- Major wheat diseases.
- Fertilizer requirements.
- Soil and weather conditions.
- Wheat harvesting.
- Nutritional benefits and uses.

## Future Improvements

- Add more crops.
- Add Awadhi language support.
- Add spoken AI responses.
- Develop a user-friendly interface.
- Expand the agricultural knowledge base.

## Project Purpose

The goal is to make agricultural information more accessible to farmers through AI-powered voice interaction in their preferred languages.