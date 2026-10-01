import time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="AI Digital Twin & Troubleshooter",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 AI Industrial Automation Digital Twin")
st.caption("Stage 1: Virtual Plant & Baseline Dynamic Simulation Engine")

# Initialize session state variables for process values and controls
if "tank_level" not in st.session_state:
    st.session_state.tank_level = 50.0  # Percentage (0-100%)
if "inflow_rate" not in st.session_state:
    st.session_state.inflow_rate = 12.0  # m3/h
if "outflow_rate" not in st.session_state:
    st.session_state.outflow_rate = 10.0  # m3/h
if "pump_status" not in st.session_state:
    st.session_state.pump_status = True  # True = RUNNING
if "valve_position" not in st.session_state:
    st.session_state.valve_position = 50.0  # 0-100% open
if "history" not in st.session_state:
    st.session_state.history = []


# ==========================================
# 2. SIMULATION & PLC LOGIC ENGINE
# ==========================================
def run_simulation_step():
    """Simulates 1 second of physical dynamics and PLC scan loop."""
    dt = 0.5  # Time step factor

    # Calculate actual flow dynamics
    actual_inflow = (
        st.session_state.inflow_rate if st.session_state.pump_status else 0.0
    )
    actual_outflow = (
        st.session_state.valve_position / 100.0
    ) * st.session_state.outflow_rate

    # Mass Balance Equation: dL/dt = (Inflow - Outflow) / Area
    delta_level = (actual_inflow - actual_outflow) * dt
    st.session_state.tank_level = float(
        np.clip(st.session_state.tank_level + delta_level, 0.0, 100.0)
    )

    # PLC Reading Simulation (LT-101)
    lt_101 = st.session_state.tank_level

    # PLC Logic Alarms
    high_alarm = lt_101 >= 85.0
    low_alarm = lt_101 <= 15.0

    # Log historical data point
    st.session_state.history.append({
        "Timestamp": pd.Timestamp.now().strftime("%H:%M:%S"),
        "LT_101_Level": round(lt_101, 2),
        "Inflow": actual_inflow,
        "Outflow": round(actual_outflow, 2),
        "Pump": "RUNNING" if st.session_state.pump_status else "STOPPED",
        "High_Alarm": high_alarm,
        "Low_Alarm": low_alarm,
    })

    # Limit history log memory to last 50 steps
    if len(st.session_state.history) > 50:
        st.session_state.history.pop(0)

    return lt_101, high_alarm, low_alarm


# Run one step of simulation on render
current_lt101, hi_alarm, lo_alarm = run_simulation_step()

# ==========================================
# 3. SIDEBAR: PLANT CONTROL PANEL
# ==========================================
st.sidebar.header("🕹️ Operator Controls")

st.session_state.pump_status = st.sidebar.toggle(
    "Pump P-101 Power", value=st.session_state.pump_status
)

st.session_state.inflow_rate = st.sidebar.slider(
    "Inflow Rate (m3/h)",
    min_value=0.0,
    max_value=30.0,
    value=float(st.session_state.inflow_rate),
)

st.session_state.valve_position = st.sidebar.slider(
    "Control Valve FCV-101 Opening (%)",
    min_value=0.0,
    max_value=100.0,
    value=float(st.session_state.valve_position),
)

st.sidebar.markdown("---")
if st.sidebar.button("Reset Simulation"):
    st.session_state.tank_level = 50.0
    st.session_state.history = []
    st.rerun()

# ==========================================
# 4. HMI / SCADA VISUALIZATION LAYOUT
# ==========================================
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🖥️ Tank Level Gauge (LT-101)")

    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=current_lt101,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Tank Level (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "royalblue"},
                "steps": [
                    {"range": [0, 15], "color": "lightcoral"},
                    {"range": [15, 85], "color": "lightgreen"},
                    {"range": [85, 100], "color": "lightcoral"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": current_lt101,
                },
            },
        )
    )
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("### Alarm Panel")
    if hi_alarm:
        st.error("🚨 HIGH LEVEL ALARM (>= 85%)")
    elif lo_alarm:
        st.warning("⚠️ LOW LEVEL ALARM (<= 15%)")
    else:
        st.success("✅ SYSTEM NORMAL")

with col2:
    st.subheader("📈 Real-Time Process Trend")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)

        fig_trend = go.Figure()
        fig_trend.add_trace(
            go.Scatter(
                x=df["Timestamp"],
                y=df["LT_101_Level"],
                mode="lines+markers",
                name="LT-101 (%)",
                line=dict(color="royalblue", width=2),
            )
        )
        fig_trend.add_hline(
            y=85,
            line_dash="dash",
            line_color="red",
            annotation_text="High Alarm",
        )
        fig_trend.add_hline(
            y=15,
            line_dash="dash",
            line_color="orange",
            annotation_text="Low Alarm",
        )

        fig_trend.update_layout(
            yaxis=dict(range=[0, 100], title="Level (%)"),
            xaxis=dict(title="Time"),
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# ==========================================
# 5. PROCESS DATA READOUT TABLE
# ==========================================
st.markdown("---")
st.subheader("📋 PLC Input/Output Table")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Pump P-101", "RUNNING" if st.session_state.pump_status else "STOPPED")
m2.metric("Inflow", f"{st.session_state.inflow_rate} m3/h")
m3.metric("FCV-101 Opening", f"{st.session_state.valve_position}%")
m4.metric("LT-101 Signal", f"{round(current_lt101, 1)} %")

time.sleep(1)
st.rerun()
import streamlit as st
from simulation.virtual_plant import VirtualPlant
from engineering.diagnostic_engine import DiagnosticEngine
from engineering.prognostics_engine import PrognosticsEngine
from agents.cmms_agent import CMMSAgent

st.set_page_config(page_title="AI Instrumentation Engine Stage 1+2", layout="wide")

st.title("AI INSTRUMENTATION ENGINE (Stage 1 + Stage 2)")
st.caption("Intelligent Diagnostics, Predictive RUL Prognostics & Automated CMMS Dispatch")

# Initialize Plant & Engines
if 'plant' not in st.session_state:
    st.session_state.plant = VirtualPlant()

plant_data = st.session_state.plant.tick()

# Stage 2 RUL Evaluation
prog_engine = PrognosticsEngine()
rul_results = prog_engine.evaluate_rul(plant_data)

st.subheader("Stage 2 Remaining Useful Life (RUL) Forecast")
col1, col2 = st.columns(2)
col1.metric("PT-101 RUL", f"{rul_results['pt101_rul_days']} Days", f"Drift: {rul_results['drift_rate']:.2f} bar/day")
col2.metric("CV-101 RUL", f"{rul_results['cv101_rul_days']} Days", f"Wear Index: {rul_results['wear_index']}%")

if st.button("🚀 DISPATCH AUTOMATED WORK ORDER"):
    cmms = CMMSAgent()
    wo = cmms.generate_work_order(rul_results)
    st.success(f"Dispatched Work Order: {wo['wo_id']} to SAP CMMS")
