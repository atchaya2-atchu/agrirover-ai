import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AgriRover AI",
    page_icon="🚜",
    layout="wide"
)

def calculate_priority(quantity, waiting_time, urgency, readiness):
    urgency_points = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }

    readiness_points = {
        "Not Ready": 1,
        "Ready": 3
    }

    score = (
        urgency_points[urgency] * 40
        + readiness_points[readiness] * 20
        + waiting_time * 5
        + quantity * 0.1
    )

    return round(score, 2)

if "farms" not in st.session_state:
    st.session_state.farms = []

if "mission_started" not in st.session_state:
    st.session_state.mission_started = False

if "current_stop" not in st.session_state:
    st.session_state.current_stop = 0

st.title("🚜 AgriRover AI")
st.subheader("AI-Enabled First-Mile Agricultural Logistics")
st.write("Smart farm dispatch, pickup prioritization and autonomous rover coordination.")

st.divider()

st.sidebar.header("🌾 Farm Request")

farm_name = st.sidebar.text_input(
    "Farm Name",
    placeholder="Example: FARM F"
)

crop = st.sidebar.selectbox(
    "Crop",
    ["Pineapple", "Ginger", "Turmeric", "Chilli", "Maize", "Other"]
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

rover_capacity = st.sidebar.number_input(
    "Rover Cargo Capacity (kg)",
    min_value=1.0,
    value=15.0
)

if st.sidebar.button("➕ Add Farm"):
    if farm_name.strip():
        st.session_state.farms.append({
            "Farm": farm_name.strip().upper(),
            "Crop": crop,
            "Quantity_kg": quantity,
            "Readiness": readiness,
            "Waiting_Time_hr": waiting_time,
            "Urgency": urgency
        })
        st.sidebar.success("Farm request added.")
    else:
        st.sidebar.warning("Enter a farm name first.")

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

    st.session_state.mission_started = False
    st.session_state.current_stop = 0

if not st.session_state.farms:
    st.info("No farm requests yet. Use 'Load Demo Farms' or add a farm from the sidebar.")
    st.stop()

df = pd.DataFrame(st.session_state.farms)

df["Priority_Score"] = df.apply(
    lambda row: calculate_priority(
        row["Quantity_kg"],
        row["Waiting_Time_hr"],
        row["Urgency"],
        row["Readiness"]
    ),
    axis=1
)

result = (
    df.sort_values("Priority_Score", ascending=False)
    .reset_index(drop=True)
)

result["Pickup_Order"] = range(1, len(result) + 1)

c1, c2, c3, c4 = st.columns(4)

c1.metric("🌾 Farm Requests", len(result))
c2.metric("📦 Total Queued Cargo", f"{result['Quantity_kg'].sum():.0f} kg")
c3.metric("🔥 High Priority", len(result[result["Urgency"] == "High"]))
c4.metric("🚜 Rover Status", "READY")

st.divider()

st.header("🏢 Collection Centre Communication Network")

network_html = """
<div style="
display:flex;
align-items:center;
justify-content:center;
gap:12px;
flex-wrap:wrap;
padding:20px 5px;
">

<div style="padding:18px;border:2px solid #4b5563;border-radius:12px;text-align:center;min-width:130px;">
🌾<br><b>FARM NODES</b><br>A • B • C • D • E
</div>

<div style="font-size:28px;">→</div>

<div style="padding:18px;border:2px solid #4b5563;border-radius:12px;text-align:center;min-width:130px;">
📡<br><b>LoRa SX1278</b><br>Wireless Link
</div>

<div style="font-size:28px;">→</div>

<div style="padding:18px;border:2px solid #4b5563;border-radius:12px;text-align:center;min-width:150px;">
🏢<br><b>COLLECTION CENTRE</b><br>Dispatch Control
</div>

<div style="font-size:28px;">→</div>

<div style="padding:18px;border:2px solid #4b5563;border-radius:12px;text-align:center;min-width:140px;">
🤖<br><b>AI ENGINE</b><br>Pickup Ranking
</div>

<div style="font-size:28px;">→</div>

<div style="padding:18px;border:2px solid #4b5563;border-radius:12px;text-align:center;min-width:130px;">
🚜<br><b>CARGO ROVER</b><br>Autonomous Pickup
</div>

</div>
"""

st.markdown(network_html, unsafe_allow_html=True)

st.divider()

st.header("🗺️ AI-Generated Pickup Route")

route = result["Farm"].tolist()

positions = {
    "FARM A": (-3, 2),
    "FARM B": (-3, -2),
    "FARM C": (3, 2),
    "FARM D": (3, -2),
    "FARM E": (5, 0)
}

fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(0, 0, s=500, marker="s")

ax.text(
    0,
    -0.55,
    "COLLECTION\nCENTRE",
    ha="center",
    fontweight="bold"
)

for farm, (x, y) in positions.items():
    ax.scatter(x, y, s=350)
    ax.text(
        x,
        y + 0.35,
        farm,
        ha="center",
        fontweight="bold"
    )

last_x = 0
last_y = 0

for farm in route:
    if farm in positions:
        x, y = positions[farm]

        ax.plot(
            [last_x, x],
            [last_y, y],
            linestyle="--",
            linewidth=1.8
        )

        last_x = x
        last_y = y

ax.set_title("Recommended Farm Pickup Sequence")
ax.set_xlabel("Demo terrain coordinate")
ax.set_ylabel("Demo terrain coordinate")
ax.grid(alpha=0.25)

st.pyplot(fig)

st.caption("Schematic route for prototype demonstration; not a geographic map.")

st.success(f"🚚 Route: {' → '.join(route)}")

st.divider()

left, right = st.columns(2)

with left:
    st.header("📡 LoRa Communication Status")
    st.success("🟢 LoRa SX1278 — LINK ONLINE")
    st.write("Communication path: Farm Node → Collection Centre → Rover")
    st.write("Protocol: LoRa point-to-point")
    st.write("Controller: ESP32")
    st.progress(1.0)
    st.caption("Communication status shown here is a prototype software simulation.")

with right:
    st.header("🚨 Rover Sensor Status")

    sensor1, sensor2 = st.columns(2)

    with sensor1:
        st.success("🟢 ESP32")
        st.success("🟢 IR Trail Sensor")

    with sensor2:
        st.success("🟢 HC-SR04")
        st.success("🟢 Motor Driver")

    st.info("Obstacle detection is represented through the HC-SR04 ultrasonic sensor.")

st.divider()

st.header("🤖 AI Decision Explanation")

top = result.iloc[0]

st.success(f"Priority #1: {top['Farm']} — {top['Crop']}")

reason_col1, reason_col2, reason_col3, reason_col4 = st.columns(4)

with reason_col1:
    st.metric("Urgency", top["Urgency"])

with reason_col2:
    st.metric("Waiting Time", f"{top['Waiting_Time_hr']:.0f} h")

with reason_col3:
    st.metric("Quantity", f"{top['Quantity_kg']:.0f} kg")

with reason_col4:
    st.metric("Priority Score", f"{top['Priority_Score']:.1f}")

st.write(
    f"""
The priority engine ranked {top['Farm']} first because its combined
priority score is the highest among the current farm requests.

The score considers harvest urgency, harvest readiness, waiting time
and quantity of produce. The pickup sequence changes when the farm
conditions change.
"""
)

st.divider()

st.header("📈 Priority Score Analysis")

fig2, ax2 = plt.subplots(figsize=(10, 4))

ax2.bar(
    result["Farm"],
    result["Priority_Score"]
)

ax2.set_xlabel("Farm")
ax2.set_ylabel("Priority Score")
ax2.set_title("AI-Based Farm Pickup Priority")
ax2.grid(axis="y", alpha=0.25)

st.pyplot(fig2)

st.divider()

st.header("📋 AI Recommended Pickup Order")

table = result[
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
    table,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.header("📦 Rover Cargo Capacity")

cargo_col1, cargo_col2 = st.columns(2)

with cargo_col1:
    st.metric(
        "Prototype Rover Capacity",
        f"{rover_capacity:.0f} kg"
    )

with cargo_col2:
    first_pickup = top["Quantity_kg"]
    st.metric(
        "First Pickup Load",
        f"{first_pickup:.0f} kg"
    )

load_ratio = min(
    first_pickup / rover_capacity,
    1.0
)

st.progress(load_ratio)

if first_pickup > rover_capacity:
    st.warning(
        "The selected farm quantity exceeds one rover trip capacity. "
        "The system can divide the pickup into multiple trips."
    )
else:
    st.success("First pickup fits within the prototype rover capacity.")

st.divider()

st.header("🚚 Live Rover Mission")

mission_left, mission_right = st.columns(2)

with mission_left:
    st.subheader("Mission Route")
    st.write(" → ".join(route))

    if st.button("🚀 DISPATCH ROVER", type="primary"):
        st.session_state.mission_started = True
        st.session_state.current_stop = 0
        st.rerun()

with mission_right:

    if st.session_state.mission_started:

        current = st.session_state.current_stop

        if current < len(route):

            current_farm = route[current]

            st.warning(
                f"🚜 Rover travelling to {current_farm}"
            )

            st.progress(current / len(route))

            st.write(
                f"Mission stop: {current + 1} / {len(route)}"
            )

            st.write(
                f"📡 LoRa command: NAVIGATE → {current_farm}"
            )

            if st.button("➡️ Simulate Arrival"):
                st.session_state.current_stop += 1
                st.rerun()

        else:

            st.success("🏁 All scheduled pickups completed.")
            st.success("🚜 Rover returned to Collection Centre.")

            if st.button("Reset Mission"):
                st.session_state.mission_started = False
                st.session_state.current_stop = 0
                st.rerun()

    else:
        st.info("Rover is waiting for dispatch command.")

st.divider()

st.header("⚙️ Technical Stack")

tech = pd.DataFrame({
    "System": [
        "AI Priority Engine",
        "Communication",
        "Main Controller",
        "Trail Navigation",
        "Obstacle Detection",
        "Motor Control"
    ],
    "Technology": [
        "Python weighted decision model",
        "LoRa SX1278",
        "ESP32",
        "IR Sensor Array",
        "HC-SR04 Ultrasonic",
        "L298N + Geared DC Motors"
    ]
})

st.table(tech)
