# 🏔️ TrailCrafter AI

TrailCrafter AI is a **high-altitude trek planner** built using **Streamlit, LangChain, and OpenAI GPT-4o-mini**.

It generates personalized trekking guidance based on:

* 🏔️ Trek destination
* 💪 Fitness level
* 🌦️ Trekking season

### ✨ Features

* Trek difficulty and route profile
* Essential gear recommendations
* Acclimatization and altitude safety tips
* Training/preparation timeline
* Popular trek presets
* Real-time AI response streaming

### 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* OpenAI GPT-4o-mini
* python-dotenv

### 🚀 Run Locally

Install dependencies:

```bash
pip install streamlit python-dotenv langchain-core langchain-openai
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

Run the app:

```bash
streamlit run basic_app.py
```

> ⚠️ **Disclaimer:** AI-generated trekking advice is for informational purposes only. Always verify high-altitude safety information with qualified professionals and current local conditions.
