import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. Page Configuration
st.set_page_config(
    page_title="TrailCrafter | High-Altitude Trek Planner",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS styling for a polished look
st.markdown("""
<style>
    /* Metric / Stat Badge highlights */
    .hero-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2.2rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.9;
        margin: 0;
    }
    .badge-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        border-radius: 18px;
        padding: 0.25rem 0.75rem;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-top: 0.6rem;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. Environment and LangChain setup
load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an elite high-altitude expedition leader and wilderness safety expert. "
        "Provide direct, highly structured, practical, and safety-critical advice formatted with clear markdown headers, "
        "bullet points, and bold text."
    ),
    (
        "user",
        "I am planning to trek {trek_name}. "
        "My fitness level is {fitness_level} and my planned trekking season is {season}. "
        "Please provide:\n"
        "### 1. Difficulty & Route Profile (Altitude, terrain, realistic challenge for my level)\n"
        "### 2. Mandatory Gear Checklist (Top 3 non-negotiables for this season)\n"
        "### 3. Acclimatization & Safety Protocol (Specific altitude management tips)\n"
        "### 4. Preparation Timeline (Specific weeks of training required)"
    )
])

parser = StrOutputParser()
trek_chain = prompt_template | model | parser

# 4. Sidebar: Helpful references & disclaimer
with st.sidebar:
    st.header("🧭 Expedition Base")
    st.info(
        "**Pro Tip:** Always build a buffer day into any Himalayan or high-altitude itinerary "
        "for unexpected weather or acclimatization delays."
    )
    
    st.markdown("---")
    st.subheader("🎒 Golden Rules of Trekking")
    st.markdown("""
    * **Climb high, sleep low.**
    * **Hydrate:** 3–4 liters of fluids per day.
    * **Never ignore a headache** at altitudes above 2,500m.
    * **Leave no trace** — pack out everything you pack in.
    """)
    st.markdown("---")
    st.caption("Powered by LangChain LCEL & GPT-4o-mini")

# 5. Hero Header Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🏔️ TrailCrafter AI</div>
    <div class="hero-subtitle">High-altitude expedition intelligence tailored to your fitness and itinerary.</div>
    <span class="badge-pill">⚡ Real-time LCEL Stream</span>
    <span class="badge-pill">🛡️ Altitude Safety Checks</span>
    <span class="badge-pill">🎒 Gear Tailoring</span>
</div>
""", unsafe_allow_html=True)

# 6. Quick Trek Picker Chips
st.markdown("##### 📍 Popular Trek Presets (click to autofill)")
chip_cols = st.columns(4)
default_trek = ""

if chip_cols[0].button("❄️ Kedarkantha (Winter)"):
    st.session_state["trek_input"] = "Kedarkantha, Uttarakhand"
    st.session_state["season_input"] = "Winter (Dec - Feb)"
if chip_cols[1].button("🌸 Sandakphu (Singalila)"):
    st.session_state["trek_input"] = "Sandakphu, West Bengal"
    st.session_state["season_input"] = "Spring (Mar - May)"
if chip_cols[2].button("🏔️ Roopkund / Ali Bedni"):
    st.session_state["trek_input"] = "Ali Bedni Bugyal, Uttarakhand"
    st.session_state["season_input"] = "Autumn (Sep - Nov)"
if chip_cols[3].button("🏕️ Hampta Pass (Crossover)"):
    st.session_state["trek_input"] = "Hampta Pass, Himachal"
    st.session_state["season_input"] = "Monsoon/Summer (Jul - Aug)"

# 7. Main Input Card Form
with st.form("trek_planner_form"):
    col1, col2, col3 = st.columns([2, 1.2, 1.2])
    
    with col1:
        current_trek = st.session_state.get("trek_input", "")
        trek_name = st.text_input(
            "Trek Name or Region",
            value=current_trek,
            placeholder="e.g., Annapurna Circuit, Kashmir Great Lakes, Rupin Pass"
        )
    
    with col2:
        fitness_level = st.selectbox(
            "Current Fitness Level",
            ["Beginner (Walks/Light jogs)", "Intermediate (Regular 5k/Gym)", "Advanced (Marathons/Trekker)"]
        )
        
    with col3:
        season_options = ["Autumn (Sep - Nov)", "Winter (Dec - Feb)", "Spring (Mar - May)", "Monsoon/Summer (Jun - Aug)"]
        selected_season = st.session_state.get("season_input", season_options[0])
        default_index = season_options.index(selected_season) if selected_season in season_options else 0
        season = st.selectbox("Trek Season", season_options, index=default_index)

    submitted = st.form_submit_button("⚡ Generate Expedition Plan", type="primary", use_container_width=True)

# 8. Output Display Container
if submitted:
    if not trek_name.strip():
        st.warning("⚠️ Please enter a destination or select one of the presets above.")
    else:
        st.markdown(f"### 📋 Custom Expedition Brief: **{trek_name}**")
        
        # Summary tags
        tag_col1, tag_col2, tag_col3 = st.columns(3)
        tag_col1.metric("Destination", trek_name.split(",")[0])
        tag_col2.metric("Target Fitness", fitness_level.split(" ")[0])
        tag_col3.metric("Window", season.split(" ")[0])
        
        st.divider()

        # Stream real-time output into a styled callout container
        with st.container(border=True):
            st.write_stream(
                trek_chain.stream({
                    "trek_name": trek_name,
                    "fitness_level": fitness_level,
                    "season": season
                })
            )