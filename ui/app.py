"""
Explainable Cardiovascular Digital Twin - Research Demonstration UI

CRITICAL SAFETY NOTES:
======================
- This is a RESEARCH SIMULATION, not a clinical tool
- All outputs are simulated responses, not real predictions
- Uses conservative language to avoid overclaiming
- Prominent disclaimers throughout

Author: Major Project
Date: January 2026
"""

import streamlit as st
import sys
import os

# Add project root and src to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

# Import section modules
from sections.input_panel import render_input_panel
from sections.output_panel import render_output_panel
from sections.metrics_panel import render_metrics_panel
from sections.methodology_panel import render_methodology_panel
from sections.transparency_panel import render_transparency_panel
from sections.disclaimer_panel import render_disclaimer_panel
from sections.optimizer_panel import render_optimizer_panel
from assets.icons import icon


# Page configuration
st.set_page_config(
    page_title="Cardiovascular Digital Twin",
    page_icon="❤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional medical dashboard styling
st.markdown("""
<style>
    /* ===== GLOBAL RESET ===== */
    .block-container { padding-top: 1rem; }
    
    /* ===== HEADER GRADIENT BAR ===== */
    .gradient-header {
        background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 50%, #3182ce 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(26, 54, 93, 0.3);
    }
    .gradient-header h1 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .gradient-header p {
        color: #bee3f8;
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
        font-weight: 400;
    }
    
    /* ===== BUTTON STYLING ===== */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 2px 8px rgba(43, 108, 176, 0.3);
        transition: all 0.2s;
    }
    .stButton>button[kind="primary"]:hover {
        box-shadow: 0 4px 12px rgba(43, 108, 176, 0.5);
        transform: translateY(-1px);
        color: white;
    }
    
    /* ===== ALERT TWEAKS ===== */
    .stAlert { border-radius: 10px; }
    
    /* ===== FOOTER ===== */
    .pro-footer {
        background: linear-gradient(135deg, #1a365d 0%, #2d3748 100%);
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-top: 2rem;
    }
    .pro-footer .title { color: #e2e8f0; font-size: 13px; font-weight: 600; margin-bottom: 4px; }
    .pro-footer .body { color: #a0aec0; font-size: 12px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# Theme selection logic
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

def toggle_theme():
    st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'

# INJECT DYNAMIC THEMES
if st.session_state['theme'] == 'light':
    st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    .stApp, .stApp p, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stMarkdown {
        color: #1a202c !important;
    }
    [data-testid="stSidebar"] { background-color: #f7fafc !important; }
    .gradient-header h1 { color: #ffffff !important; }
    .pro-footer .title { color: #e2e8f0 !important; }
    [data-testid="stMetric"] { background-color: #edf2f7 !important; border-color: #e2e8f0 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #edf2f7 !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #ffffff !important; color: #2b6cb0 !important; }
    .stTabs [data-baseweb="tab"] { color: #4a5568 !important; }
    .info-card { background-color: #ffffff !important; border-color: #e2e8f0 !important; }
    .info-card h4 { color: #2b6cb0 !important; }
    .info-card p { color: #4a5568 !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117 !important; }
    .stApp, .stApp p, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stMarkdown {
        color: #fafafa !important;
    }
    [data-testid="stSidebar"] { background-color: #262730 !important; }
    .gradient-header h1 { color: #ffffff !important; }
    .pro-footer .title { color: #e2e8f0 !important; }
    [data-testid="stMetric"] { background-color: #1e1e24 !important; border-color: #333 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #262730 !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #0e1117 !important; color: #90cdf4 !important; }
    .stTabs [data-baseweb="tab"] { color: #a0aec0 !important; }
    .info-card { background-color: #1e1e24 !important; border-color: #333 !important; }
    .info-card h4 { color: #90cdf4 !important; }
    .info-card p { color: #a0aec0 !important; }
    </style>
    """, unsafe_allow_html=True)

# Professional gradient header with SVG icon
header_icon = icon('heart-pulse', size=28, color='#ffffff')
st.markdown(f"""
<div class="gradient-header">
    <h1>{header_icon} Cardiovascular Digital Twin</h1>
    <p>Explainable AI-Driven Research Platform &bull; Physiology-Inspired Simulation</p>
</div>
""", unsafe_allow_html=True)


# SIDEBAR: Controls Only
st.sidebar.title("Controls")

# Theme Toggle Button
theme_icon = "🌞 Light Mode" if st.session_state['theme'] == 'dark' else "🌙 Dark Mode"
st.sidebar.button(theme_icon, on_click=toggle_theme, use_container_width=True)

# Version selector (clean, minimal)
version = st.sidebar.radio(
    "Version",
    options=["V1", "V2"],
    format_func=lambda x: f"● {x}: {'Synthetic' if x == 'V1' else 'Real-World Grounded'}",
    help="V1: Method validation (clean synthetic)\nV2: Robustness testing (noise-grounded + uncertainty)"
)

version_tag = version

st.sidebar.markdown("---")

# Get patient profile from input panel
patient_profile = render_input_panel()

# Run simulation button
if st.sidebar.button("Run Simulation", type="primary", use_container_width=True):
    st.session_state['run_simulation'] = True
    st.session_state['patient_profile'] = patient_profile
    st.session_state['version'] = version_tag

# Horizontal Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Simulation",
    "Treatment Optimizer",
    "Metrics",
    "Methodology",
    "Transparency",
    "Disclaimers"
])

# Tab 1: Simulation
with tab1:
    if st.session_state.get('run_simulation', False):
        render_output_panel(
            st.session_state.get('patient_profile', patient_profile),
            st.session_state.get('version', version_tag)
        )
    else:
        st.info("Configure patient profile in the sidebar and click 'Run Simulation'")
        
        # Show example
        st.subheader("What-If Scenario Exploration")
        st.markdown("""
        This interface enables exploration of simulated cardiovascular response trends:
        
        1. Configure a synthetic patient profile
        2. Select an intervention class
        3. Run the simulation
        4. Explore simulated response trends
        """)

# Tab 2: Treatment Optimizer
with tab2:
    render_optimizer_panel(patient_profile)

# Tab 3: Metrics
with tab3:
    render_metrics_panel(version_tag)

# Tab 4: Methodology
with tab4:
    render_methodology_panel()

# Tab 5: Transparency
with tab5:
    render_transparency_panel()

# Tab 6: Disclaimers
with tab6:
    render_disclaimer_panel()

# Professional footer
st.markdown("""
<div class="pro-footer">
    <div class="title">Research Simulation Notice</div>
    <div class="body">
        This interface demonstrates methodology using synthetic data. 
        Outputs represent simulated relative trends under modeled assumptions, not real patient measurements. 
        Not for clinical use.
    </div>
</div>
""", unsafe_allow_html=True)

st.caption("**Cardiovascular Digital Twin** | Research Demonstration | January 2026")

