
import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AgriRover AI",
    page_icon="🚜",
    layout="wide"
)

# -----------------------------
# AI PRIORITY ENGINE
# -----------------------------
def calculate_priority(quantity, waiting_time, urgency, readiness):

    urgency_score = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }

    readiness_score = {
        "Not Ready": 1,
        "Ready": 3
    }

    score = (
        urgency_score[urgency] * 40
        + readiness_score[readiness] * 20
        + waiting_time * 5
        + quantity * 0.1
    )

    return round(score, 2)


# -----------------------------
# TITLE
# -----------------------------
st.title("🚜 AgriRover AI")
st.subheader("AI-Enabled First-Mile Agricultural Logistics")

st.markdown(
    "### Smart Collection Centre Control Dashboard"
)

st.divider()

# -----------------------------
# SIDEBAR – FARM REQUEST
# -----------------------------
st.sidebar.header("🌾 Add Farm Request")

farm_name = st.sidebar.text_input(
    "Farm Name",
    placeholder="Example: FARM A"
)

crop = st.sidebar.selectbox(
    "Crop",
    [
        "Pineapple",
        "Ginger",
        "Turmeric",
        "Chilli",
        "Maize",
        "Other"
    ]
)

quantity = st.sidebar.number_input(
    "Quantity (kg)",
    min_value=1.0,
    value=50.0
)

readiness = st.sidebar.selectbox(
    "Harvest Readiness",
    ["Ready", "Not Ready"]
)

waiting_time = st.sidebar.number_input(
    "Waiting Time (hours)",
    min_value=0.0,
    value=1.0
)

urgency = st.sidebar.selectbox(
    "Urgency",
    ["Low", "Medium", "High"]
)

if "farms" not in st.session_state:
    st.session_state.farms = []


# -----------------------------
# ADD FARM BUTTON
# -----------------------------
if st.sidebar.button("➕ Add Farm"):

    if farm_name.strip() == "":
        st.sidebar.error("Enter a farm name.")

    else:
        st.session_state.farms.append({
            "Farm": farm_name.upper(),
            "Crop": crop,
            "Quantity_kg": quantity,
            "Readiness": readiness,
            "Waiting_Time_hr": waiting_time,
            "Urgency": urgency
        })

        st.sidebar.success(
            f"{farm_name.upper()} added successfully!"
        )


# -----------------------------
# DEMO DATA BUTTON
# -----------------------------
if st.sidebar.button("⚡ Load Demo Farms"):

    st.session_state.farms = [
        {
            "Farm": "FARM A",
            "Crop": "Pineapple",
            "Quantity_kg": 80,
            "Readiness": "Ready",
            "Waiting_Time_hr": 5,
            "Urgency": "High"
        },
        {
            "Farm": "FARM B",
            "Crop": "Ginger",
            "Quantity_kg": 40,
            "Readiness": "Ready",
            "Waiting_Time_hr": 2,
            "Urgency": "Medium"
        },
        {
            "Farm": "FARM C",
            "Crop": "Turmeric",
            "Quantity_kg": 100,
            "Readiness": "Ready",
            "Waiting_Time_hr": 7,
            "Urgency": "High"
        },
        {
            "Farm": "FARM D",
            "Crop": "Chilli",
            "Quantity_kg": 60,
            "Readiness": "Ready",
            "Waiting_Time_hr": 4,
            "Urgency": "Medium"
        },
        {
            "Farm": "FARM E",
            "Crop": "Maize",
            "Quantity_kg": 120,
            "Readiness": "Ready",
            "Waiting_Time_hr": 9,
            "Urgency": "High"
        }
    ]


# -----------------------------
# MAIN DASHBOARD
# -----------------------------
if len(st.session_state.farms) == 0:

    st.info(
        "No farm requests available. "
        "Use the sidebar to add farms or load the demo data."
    )

else:

    df = pd.DataFrame(st.session_state.farms)

    # Calculate AI priority
    df["Priority_Score"] = df.apply(
        lambda row: calculate_priority(
            row["Quantity_kg"],
            row["Waiting_Time_hr"],
            row["Urgency"],
            row["Readiness"]
        ),
        axis=1
    )

    # Sort by priority
    result = df.sort_values(
        by="Priority_Score",
        ascending=False
    ).reset_index(drop=True)

    result["Pickup_Order"] = range(
        1,
        len(result) + 1
    )

    # -------------------------
    # KPI CARDS
    # -------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌾 Farm Requests",
        len(result)
    )

    col2.metric(
        "📦 Total Cargo",
        f"{result['Quantity_kg'].sum():.0f} kg"
    )

    col3.metric(
        "🔥 High Priority",
        len(result[result["Urgency"] == "High"])
    )

    col4.metric(
        "🚜 Rover Status",
        "READY"
    )

    st.divider()

    # -------------------------
    # AI PRIORITY TABLE
    # -------------------------
    st.header("🤖 AI Recommended Pickup Order")

    display_df = result[
        [
            "Pickup_Order",
            "Farm",
            "Crop",
            "Quantity_kg",
            "Readiness",
            "Waiting_Time_hr",
            "Urgency",
            "Priority_Score"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -------------------------
    # ROVER ROUTE
    # -------------------------
    st.header("🚚 Autonomous Rover Mission")

    route = " → ".join(
        result["Farm"].tolist()
    )

    st.success(
        f"Recommended Rover Route:  {route}"
    )

    st.write(
        "The AI-generated pickup sequence is transmitted "
        "to the rover through the LoRa communication layer."
    )

    # -------------------------
    # DISPATCH
    # -------------------------
    if st.button(
        "🚀 DISPATCH ROVER",
        type="primary"
    ):

        st.success(
            "🚜 Rover mission dispatched successfully!"
        )

        st.write(
            f"Mission Route: **{route}**"
        )

        st.write(
            "📡 LoRa Status: Command Ready"
        )

        st.write(
            "🟢 Rover Status: Mission Initiated"
        )

    st.divider()

    # -------------------------
    # SYSTEM ARCHITECTURE
    # -------------------------
    st.header("🔗 System Architecture")

    st.markdown(
        """
        **🌾 Farm Nodes**
        ↓  
        **📡 LoRa Communication**
        ↓  
        **🏢 Collection Centre**
        ↓  
        **🤖 AI Pickup Prioritization**
        ↓  
        **🚚 Autonomous Cargo Rover**
        ↓  
        **📦 Farm-to-Collection Transport**
        """
    )
