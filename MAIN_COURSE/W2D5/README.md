# 🏔️ TrailCrafter AI — High-Altitude Trek Planner

TrailCrafter AI is an AI-powered trekking planner built with **Streamlit, LangChain, and OpenAI GPT-4o-mini**.

It generates a personalized high-altitude expedition plan based on:

* 🏔️ Trek destination
* 💪 Current fitness level
* 🌦️ Trekking season

The application provides practical guidance on trek difficulty, essential gear, acclimatization, altitude safety, and training preparation.

---

## ✨ Features

### 🏔️ Personalized Trek Planning

Enter a trek or region and receive an AI-generated expedition brief tailored to your fitness level and trekking season.

### 📍 Popular Trek Presets

Quickly select from predefined trekking destinations:

* ❄️ Kedarkantha — Winter
* 🌸 Sandakphu — Spring
* 🏔️ Ali Bedni Bugyal — Autumn
* 🏕️ Hampta Pass — Summer/Monsoon

### 💪 Fitness-Based Recommendations

The application supports three fitness levels:

* Beginner — Walks / Light jogs
* Intermediate — Regular 5K / Gym
* Advanced — Marathon / Experienced Trekker

### 🎒 Gear Recommendations

The AI identifies the most important gear and season-specific essentials for the selected trek.

### 🏔️ Altitude & Acclimatization Guidance

The generated plan includes altitude management and safety recommendations.

### 🏃 Training Timeline

The AI provides a suggested preparation and training timeline based on the trek and fitness level.

### ⚡ Streaming AI Response

The response is streamed in real time using LangChain's LCEL pipeline and Streamlit's `write_stream()` functionality.

---

## 🛠️ Technology Stack

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| Python             | Application development         |
| Streamlit          | Web application UI              |
| LangChain          | LLM orchestration               |
| OpenAI GPT-4o-mini | AI model                        |
| python-dotenv      | Environment variable management |

---

## 🧠 LangChain Architecture

The application uses a simple LangChain Expression Language (LCEL) pipeline:

```text
User Input
    ↓
ChatPromptTemplate
    ↓
GPT-4o-mini
    ↓
StrOutputParser
    ↓
Streamlit UI
```

The chain is created using:

```python
trek_chain = prompt_template | model | parser
```

This demonstrates how multiple LangChain components can be connected together to create an LLM application.

---

## 📋 AI-Generated Expedition Brief

For each trek, TrailCrafter AI generates four sections:

### 1. Difficulty & Route Profile

Includes:

* Altitude
* Terrain
* Overall difficulty
* Challenge relative to the user's fitness level

### 2. Mandatory Gear Checklist

Provides the top essential gear recommendations based on the trekking season.

### 3. Acclimatization & Safety Protocol

Provides altitude-management and safety recommendations.

### 4. Preparation Timeline

Provides a suggested number of weeks and training recommendations for preparation.

---

## 📁 Project Structure

```text
W2D5/
│
├── basic_app.py
├── .env
└── .gitignore
```

> `.env` should **never be committed to Git**, because it contains your API key.

---

## 🔑 Environment Setup

Create a `.env` file in the project directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
.env.*
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Create a virtual environment

```bash
python3 -m venv course_venv
```

### 3. Activate the virtual environment

#### macOS / Linux

```bash
source course_venv/bin/activate
```

#### Windows

```bash
course_venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install streamlit python-dotenv langchain-core langchain-openai
```

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run basic_app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open it in your browser to use TrailCrafter AI.

---

## 🔄 How It Works

1. User selects or enters a trekking destination.
2. User selects their fitness level.
3. User selects the trekking season.
4. The application creates a structured prompt.
5. LangChain sends the prompt to GPT-4o-mini.
6. The model generates a personalized expedition plan.
7. `StrOutputParser` converts the response into a string.
8. Streamlit streams the response to the UI.

```text
                    ┌──────────────────┐
                    │    User Input    │
                    │ Trek / Fitness   │
                    │     / Season     │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ ChatPromptTemplate│
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │   GPT-4o-mini    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ StrOutputParser  │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Streamlit UI     │
                    └──────────────────┘
```

---

## ⚠️ Safety Disclaimer

TrailCrafter AI provides **AI-generated trekking guidance for informational purposes only**.

High-altitude trekking can involve serious risks including altitude sickness, extreme weather, injury, and other emergencies.

Always verify recommendations with:

* Qualified trekking guides
* Local authorities
* Experienced mountaineering professionals
* Medical professionals when appropriate
* Current weather and route conditions

AI-generated information should **not replace professional medical or expedition advice**.

---

## 🔮 Future Enhancements

Possible improvements include:

* 🗺️ Interactive trekking maps
* 🌦️ Live weather integration
* 📊 Fitness assessment
* 🏃 Personalized workout plans
* 🎒 Complete packing-list generator
* 💰 Trek budget estimation
* 🏕️ Accommodation recommendations
* 🚑 Emergency and evacuation information
* 📅 Day-by-day itinerary generation
* 🤖 Agentic AI workflow with external tools

---

## 👩‍💻 Learning Objectives

This project demonstrates practical usage of:

* Streamlit application development
* Environment variables and API keys
* OpenAI LLM integration
* LangChain
* ChatPromptTemplate
* LangChain Expression Language (LCEL)
* Output parsers
* LLM streaming
* Prompt engineering
* Building an AI-powered application with Python

---

## 📌 Project

**TrailCrafter AI — High-Altitude Expedition Intelligence**

Built using **Python + Streamlit + LangChain + OpenAI**.
