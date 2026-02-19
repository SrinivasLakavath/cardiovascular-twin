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

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import section modules
from sections.input_panel import render_input_panel
from sections.output_panel import render_output_panel
from sections.metrics_panel import render_metrics_panel
from sections.methodology_panel import render_methodology_panel
from sections.transparency_panel import render_transparency_panel
from sections.disclaimer_panel import render_disclaimer_panel


# Page configuration
st.set_page_config(
    page_title="Cardiovascular Digital Twin - Research Demo",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2D3748;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #718096;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    .stAlert {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    /* Professional tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 500;
    }
    /* Reduce button colors */
    .stButton>button[kind="primary"] {
        background-color: #2B6CB0;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<p class="main-header">🫀 Cardiovascular Digital Twin</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Research Demonstration</p>', unsafe_allow_html=True)

# SIDEBAR: Controls Only (LAYER 1 - Primary interaction)
st.sidebar.title("⚙️ Controls")

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
if st.sidebar.button("🚀 Run Simulation", type="primary", use_container_width=True):
    st.session_state['run_simulation'] = True
    st.session_state['patient_profile'] = patient_profile
    st.session_state['version'] = version_tag

# Horizontal Navigation Tabs (much more accessible)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Simulation",
    "📊 Metrics",
    "🔬 Methodology",
    "🔍 Transparency",
    "⚠️ Disclaimers"
])

# Tab 1: Simulation
with tab1:
    if st.session_state.get('run_simulation', False):
        render_output_panel(
            st.session_state.get('patient_profile', patient_profile),
            st.session_state.get('version', version_tag)
        )
    else:
        st.info("👈 Configure patient profile and click 'Run Simulation'")
        
        # Show example
        st.subheader("What-If Scenario Exploration")
        st.markdown("""
        This interface enables exploration of simulated cardiovascular response trends:
        
        1. Configure a synthetic patient profile
        2. Select an intervention class
        3. Run the simulation
        4. Explore simulated response trends
        """)

# Tab 2: Metrics
with tab2:
    render_metrics_panel(version_tag)

# Tab 3: Methodology
with tab3:
    render_methodology_panel()

# Tab 4: Transparency
with tab4:
    render_transparency_panel()

# Tab 5: Disclaimers
with tab5:
    render_disclaimer_panel()

# LAYER 3: Safety Notice (Neutral, calm, footer-style)
st.markdown("---")
st.markdown("""
<div style="background-color: #2D3748; border-left: 3px solid #718096; padding: 12px 16px; border-radius: 4px; margin-top: 24px;">
    <div style="color: #E2E8F0; font-size: 13px; font-weight: 500; margin-bottom: 4px;">Research Simulation Notice</div>
    <div style="color: #A0AEC0; font-size: 12px; line-height: 1.6;">
        This interface demonstrates methodology using synthetic data. 
        Outputs represent simulated relative trends under modeled assumptions, not real patient measurements. 
        Not for clinical use.
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.caption("""
**Cardiovascular Digital Twin** | Research Demonstration | January 2026
""")
