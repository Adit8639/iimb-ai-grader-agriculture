import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# 1. PAGE CONFIG & PREMIUM CSS
st.set_page_config(page_title="Agri-Logistics Enabler MVP", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; color: #111827 !important; font-family: 'Inter', sans-serif; }
    h1, h2, h3, p, span { color: #111827 !important; }
    .metric-box { border: 1px solid #E5E7EB; border-radius: 8px; padding: 15px; background: #F9FAFB; text-align: center; }
    .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    .badge-fssai { background-color: #ECFDF5; color: #059669; border: 1px solid #6EE7B7; }
    </style>
""", unsafe_allow_html=True)

st.title("🌾 Multi-Layered Agri-Logistics Engine: Live Node Demo")
st.markdown("This terminal simulates a live **PACS Micro-Cold Hub**. It demonstrates the real-time AI quality grading, cold-storage shelf-life extension, and the subsequent financial value unlocked via ONDC routing.")

# --- STATE MANAGEMENT ---
if 'scanned' not in st.session_state:
    st.session_state.scanned = False
if 'data' not in st.session_state:
    st.session_state.data = {}

# --- SIDEBAR: NODE PARAMETERS ---
with st.sidebar:
    st.header("⚙️ Local Node Parameters")
    crop_type = st.selectbox("Commodity", ["Alphonso Mango", "Tomatoes", "Onions"])
    batch_volume = st.number_input("Batch Volume (kg)", min_value=100, max_value=5000, value=1000, step=100)
    current_temp = st.slider("Ambient Temperature (°C)", 20, 45, 38)
    
    st.markdown("---")
    st.markdown("**Governance Integration**")
    st.checkbox("Active FSSAI API Link", value=True, disabled=True)
    st.checkbox("ONDC Network Sync", value=True, disabled=True)

# --- UI LAYOUT ---
col_input, col_process = st.columns([1, 2])

with col_input:
    with st.container(border=True):
        st.subheader("1. AI Optical Grading")
        st.info("Upload standard lightbox photo for QCI-accredited grading.")
        uploaded_photo = st.file_uploader("Capture Batch Sample", type=['jpg', 'png'])
        
        if uploaded_photo and not st.session_state.scanned:
            if st.button("Initialize Grading Audit", type="primary", use_container_width=True):
                with st.spinner("Executing Computer Vision protocols..."):
                    time.sleep(1.5)
                    # Simulate rigorous statistical grading
                    st.session_state.data = {
                        'brix': round(random.uniform(16.0, 20.0), 1),
                        'defect_rate': round(random.uniform(0.5, 3.5), 2),
                        'size_variance': round(random.uniform(2.0, 5.0), 1),
                        'color_index': random.randint(85, 98)
                    }
                    st.session_state.scanned = True
                    st.rerun()

with col_process:
    if st.session_state.scanned:
        d = st.session_state.data
        
        # Grading Logic
        grade = "A" if d['defect_rate'] < 2.0 and d['brix'] > 17 else "B"
        
        st.subheader("2. Audit Results & Infrastructure Routing")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='metric-box'><b>Brix (Sweetness)</b><br><h2>{d['brix']}°</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-box'><b>Defect Rate</b><br><h2>{d['defect_rate']}%</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-box'><b>Size Variance</b><br><h2>{d['size_variance']}%</h2></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='metric-box'><b>FSSAI Grade</b><br><h2 style='color:#059669;'>{grade}</h2><span class='badge badge-fssai'>Verified</span></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Cold Pod Impact Logic
        st.markdown("### 🧊 PACS Solar Pod Allocation")
        spoilage_reduction = 30 if grade == "A" else 20
        shelf_life_ext = 12 if grade == "A" else 7
        st.success(f"**Asset Triggered:** Batch assigned to Solar Pod #4. Spoilage risk reduced from 30% to <2%. Shelf-life extended by {shelf_life_ext} days, enabling national transit feasibility.")

        st.markdown("---")
        
        # Economic Logic & Value Chain Mapping
        st.subheader("3. Economic Value Realization")
        
        # Dynamic Market Math
        base_price = 45 # Base Mandi price per kg
        
        # Traditional Route
        trad_rot_loss = batch_volume * 0.30 * base_price
        trad_arbitrary_loss = batch_volume * 0.20 * base_price
        trad_middlemen_cut = (batch_volume * 0.50) * (base_price * 0.40) # 6 middlemen take 40% of remaining
        trad_farmer_takehome = (batch_volume * 0.50 * base_price) - trad_middlemen_cut
        
        # Our SaaS/ONDC Route
        premium = 1.4 if grade == "A" else 1.15
        ondc_price = base_price * premium
        our_tech_fee = (batch_volume * ondc_price) * 0.015
        pacs_storage_fee = (batch_volume * ondc_price) * 0.02
        new_farmer_takehome = (batch_volume * ondc_price) - our_tech_fee - pacs_storage_fee

        # Visualizing the difference
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=['Traditional Supply Chain', 'Our Digital-Physical Overlay'],
            x=[trad_farmer_takehome, new_farmer_takehome],
            name='Farmer Realized Income',
            orientation='h',
            marker=dict(color='#059669')
        ))
        fig.add_trace(go.Bar(
            y=['Traditional Supply Chain', 'Our Digital-Physical Overlay'],
            x=[trad_rot_loss + trad_arbitrary_loss, 0],
            name='Value Destroyed (Rot & Rejection)',
            orientation='h',
            marker=dict(color='#DC2626')
        ))
        fig.add_trace(go.Bar(
            y=['Traditional Supply Chain', 'Our Digital-Physical Overlay'],
            x=[trad_middlemen_cut, our_tech_fee + pacs_storage_fee],
            name='Intermediary Costs / Platform Fees',
            orientation='h',
            marker=dict(color='#9CA3AF')
        ))

        fig.update_layout(
            barmode='stack', 
            title=f"Economic Distribution for {batch_volume}kg of {crop_type}",
            xaxis_title="Total Rupee Value (₹)",
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # The ultimate financial equation representation
        st.markdown(f"**Governing Equation:** The value retention achieved is calculated as $V_{{ret}} = (Vol \\times P_{{ondc}}) - (F_{{platform}} + C_{{storage}})$. By eliminating $30\\%$ physical rot  and bridging directly to corporate buyers, we increase farmer net income by **+ {((new_farmer_takehome - trad_farmer_takehome)/trad_farmer_takehome)*100:.1f}%**.")
        
        if st.button("Publish to ONDC Network ->", type="primary"):
            st.balloons()
            st.success("Batch successfully syndicated to Zomato Hyperpure, Reliance Fresh, and 4 other institutional buyers via ONDC API.")
            
    else:
        st.info("Awaiting sensor input. Please upload a sample image to begin the node simulation.")