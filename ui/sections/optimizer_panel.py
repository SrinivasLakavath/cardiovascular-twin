"""
Treatment Optimizer Panel — Prescriptive Analytics UI

Uses st.session_state to persist results across Streamlit reruns.
"""

import streamlit as st
import plotly.graph_objects as go
import sys
import os

# Ensure project root on path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def render_optimizer_panel(patient_profile):
    """Render the Treatment Optimizer panel."""
    st.subheader("Treatment Optimizer")
    st.caption("AI-driven prescriptive analytics \u2014 finds the optimal treatment to reach your target BP.")
    
    # Cross-tab navigation
    st.info(
        "Run a simulation in the **Simulation** tab first to see detailed "
        "SHAP explanations of how each patient feature influences the predicted response."
    )
    
    st.markdown("---")
    
    # ========================================================================
    # TARGET BP INPUT
    # ========================================================================
    st.markdown("**Set Target Blood Pressure**")
    
    col_target1, col_target2 = st.columns(2)
    
    with col_target1:
        target_sbp = st.slider(
            "Target SBP (mmHg)",
            min_value=90, max_value=160, value=120, step=5,
            help="Desired systolic blood pressure after treatment"
        )
    
    with col_target2:
        target_dbp = st.slider(
            "Target DBP (mmHg)",
            min_value=50, max_value=100, value=80, step=5,
            help="Desired diastolic blood pressure after treatment"
        )
    
    # Current vs target
    baseline_sbp = patient_profile.get('baseline_sbp', 130)
    baseline_dbp = patient_profile.get('baseline_dbp', 85)
    
    needed_sbp = target_sbp - baseline_sbp
    needed_dbp = target_dbp - baseline_dbp
    
    col_curr, col_arrow, col_tgt = st.columns([2, 1, 2])
    with col_curr:
        st.metric("Current BP", f"{baseline_sbp}/{baseline_dbp}")
    with col_arrow:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### \u2192")
    with col_tgt:
        st.metric("Target BP", f"{target_sbp}/{target_dbp}",
                   delta=f"{needed_sbp:+d}/{needed_dbp:+d} mmHg needed")
    
    st.markdown("---")
    
    # ========================================================================
    # RUN OPTIMIZER
    # ========================================================================
    if st.button("Find Optimal Treatment", type="primary", use_container_width=True):
        with st.spinner("Searching 120 drug \u00d7 dosage combinations..."):
            try:
                from treatment_optimizer.optimizer import TreatmentOptimizer
                
                optimizer = TreatmentOptimizer()
                result = optimizer.optimize(patient_profile, target_sbp, target_dbp)
                
                st.session_state['optimizer_result'] = result
                st.session_state['optimizer_target'] = (target_sbp, target_dbp)
                st.session_state['optimizer_baseline'] = (baseline_sbp, baseline_dbp)
                
            except Exception as e:
                st.error(f"Optimizer Error: {str(e)}")
                st.info("Please ensure the surrogate model is trained (`twin_model/weights/`).")
    
    # ========================================================================
    # DISPLAY RESULTS
    # ========================================================================
    if 'optimizer_result' in st.session_state:
        result = st.session_state['optimizer_result']
        best = result['best']
        
        st.success("Optimization complete \u2014 best treatment found.")
        
        # ==============================================================
        # RECOMMENDATION
        # ==============================================================
        st.markdown("---")
        st.subheader("Recommended Treatment")
        
        col_drug, col_dose, col_pred = st.columns(3)
        
        with col_drug:
            st.metric(label="Drug", value=best['drug_name'])
            st.caption(best['mechanism'])
        
        with col_dose:
            st.metric(label="Optimal Dosage", value=f"{best['dosage']:.1f}x")
            if best['dosage'] <= 1.0:
                st.caption("Standard dose range")
            elif best['dosage'] <= 2.0:
                st.caption("Elevated dose")
            else:
                st.caption("High dose \u2014 monitor closely")
        
        with col_pred:
            st.metric(
                label="Predicted BP After Treatment",
                value=f"{best['predicted_sbp']:.0f}/{best['predicted_dbp']:.0f}",
                delta=f"{best['delta_sbp']:+.1f}/{best['delta_dbp']:+.1f} mmHg"
            )
        
        # Before \u2192 After
        st.markdown("---")
        col_b, col_a_arrow, col_a = st.columns([2, 1, 2])
        
        with col_b:
            st.metric("Before Treatment", f"{baseline_sbp}/{baseline_dbp} mmHg")
        with col_a_arrow:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### \u2192")
        with col_a:
            st.metric(
                "After Treatment (Predicted)",
                f"{best['predicted_sbp']:.0f}/{best['predicted_dbp']:.0f} mmHg",
                delta=f"{best['delta_sbp']:+.1f}/{best['delta_dbp']:+.1f}"
            )
        
        # Progress toward target
        st.markdown("---")
        st.markdown(f"**Safety Assessment:** {best['risk_level']}")
        
        # Clamp progress between 0.0 and 1.0 to prevent Streamlit exceptions on negative values
        pct_val = result.get('improvement_pct', 0)
        progress_val = max(0.0, min(pct_val / 100.0, 1.0))
        st.progress(progress_val)
        st.caption(f"**{pct_val:.1f}%** closer to target BP")
        
        # ==============================================================
        # DRUG COMPARISON CHART
        # ==============================================================
        st.markdown("---")
        st.subheader("Treatment Comparison")
        
        all_options = [best] + result['alternatives']
        drug_names = [f"{'* ' if i==0 else ''}{opt['drug_name']} ({opt['dosage']:.1f}x)" 
                      for i, opt in enumerate(all_options)]
        predicted_sbps = [opt['predicted_sbp'] for opt in all_options]
        
        colors = []
        for opt in all_options:
            if 'Safe' in opt['risk_level']:
                colors.append('#38a169')
            elif 'Caution' in opt['risk_level']:
                colors.append('#d69e2e')
            else:
                colors.append('#e53e3e')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=drug_names[::-1],
            x=predicted_sbps[::-1],
            orientation='h',
            marker_color=colors[::-1],
            text=[f'{s:.0f} mmHg' for s in predicted_sbps[::-1]],
            textposition='outside',
            textfont=dict(size=12, color='#2d3748')
        ))
        
        target_sbp_val = st.session_state.get('optimizer_target', (120, 80))[0]
        fig.add_vline(x=target_sbp_val, line_dash="dash", line_color="#3182ce",
                      annotation_text=f"Target: {target_sbp_val}",
                      annotation_position="top right")
        
        fig.update_layout(
            height=50 + len(all_options) * 50,
            margin=dict(l=20, r=60, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Predicted SBP (mmHg)', gridcolor='#edf2f7'),
            yaxis=dict(title=''),
            showlegend=False,
            font=dict(family='Arial', size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="drug_comparison_chart")
        
        # Alternative details
        if result['alternatives']:
            with st.expander("Alternative Treatment Details"):
                for i, alt in enumerate(result['alternatives'], 1):
                    st.markdown(f"**#{i+1}: {alt['drug_name']}** @ {alt['dosage']:.1f}x \u2192 "
                                f"{alt['predicted_sbp']:.0f}/{alt['predicted_dbp']:.0f} mmHg "
                                f"({alt['risk_level']})")
                    st.caption(f"Mechanism: {alt['mechanism']}")
                    if i < len(result['alternatives']):
                        st.markdown("---")
        
        # Metadata
        st.markdown("---")
        st.caption(f"Evaluated {result['total_evaluated']} drug \u00d7 dosage combinations using the ML surrogate model.")
        
        st.warning(
            "**Research Simulation Only.** These recommendations are generated by an ML surrogate model "
            "trained on synthetic data. They do NOT constitute medical advice and should NOT be used "
            "for any clinical decision-making."
        )
