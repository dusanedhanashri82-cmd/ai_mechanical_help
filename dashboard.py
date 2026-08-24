import streamlit as st
import pandas as pd
from datetime import date, timedelta
import streamlit.components.v1 as components
from pathlib import Path
import base64


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Mechanical Help Center",
    page_icon="🏍️",
    layout="wide"
)

# ============================================================
# LOGIN PROTECTION
# ============================================================

if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please login first.")
    st.switch_page("app.py")

username = st.session_state.get("username", "User")

# ============================================================
# INITIALIZE SERVICE HISTORY
# ============================================================

if "history" not in st.session_state:
    st.session_state["history"] = []



# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Mechanical Help Center")
st.subheader(
    f"🏍️ Smart Self-Service Assistant for 2-Wheelers | Welcome {username} 👋"
)

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "🏠 Home",
        "🔧 Vehicle Diagnosis",
        "🛠 Maintenance Tips",
        "📋 Service History",
        "📞 Contact Support",
        "🚪 Logout"
    ]
)

# ============================================================
# HOME
# ============================================================

if menu == "🏠 Home":

    st.header("🏠 Vehicle Information")

    st.success(
        f"Welcome {username}! 🤖 Your AI Mechanical Help Center is ready."
    )

    col1, col2 = st.columns(2)

    with col1:

        company = st.selectbox(
            "🏍️ Vehicle Company",
            list(vehicle_data.keys())
        )

        model = st.selectbox(
            "🏍️ Vehicle Model",
            list(vehicle_data[company].keys())
        )

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            step=1
        )

    with col2:

        owner = st.text_input(
            "👤 Owner Name"
        )

        number = st.text_input(
            "🔢 Vehicle Number"
        )

        fuel = st.selectbox(
            "⛽ Fuel Type",
            [
                "Petrol",
                "Electric"
            ]
        )

    st.markdown("---")

    if st.button(
        "💾 Save Vehicle Information",
        use_container_width=True
    ):

        st.session_state["vehicle_info"] = {
            "Owner": owner,
            "Vehicle Number": number,
            "Company": company,
            "Model": model,
            "Year": year,
            "Fuel": fuel
        }

        st.success(
            "✅ Vehicle information saved successfully!"
        )

    st.info(
        "💡 Select an option from the left menu to use the vehicle services."
    )

# ============================================================
# 3D BIKE VIEW
# ============================================================

elif menu == "🏍️ 3D Bike View":

    st.header("🏍️ 360° 2-Wheeler Viewer")

    st.info(
        "Select your company and model to view the 3D vehicle."
    )

    company = st.selectbox(
        "Select Vehicle Company",
        list(vehicle_data.keys())
    )

    model = st.selectbox(
        "Select Vehicle Model",
        list(vehicle_data[company].keys())
    )

    model_path = vehicle_data[company][model]

    BASE_DIR = Path(__file__).resolve().parent

    model_file = BASE_DIR / model_path

    st.write("📁 3D Model Path:")
    st.code(str(model_file))

    if not model_file.exists():

        st.error("❌ 3D model file not found!")

        st.write("Expected location:")
        st.code(str(model_file))

        st.warning(
            f"Create the folder 'models' beside your dashboard.py "
            f"and place the GLB file for {company} {model} inside it."
        )

    else:

        st.success(
            f"✅ {company} {model} 3D model found!"
        )

        try:

            with open(model_file, "rb") as file:
                model_bytes = file.read()

            model_base64 = base64.b64encode(
                model_bytes
            ).decode("utf-8")

            model_url = (
                "data:model/gltf-binary;base64,"
                + model_base64
            )

            html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<script
type="module"
src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js">
</script>

<style>

html,
body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #eeeeee;
}}

model-viewer {{
    width: 100%;
    height: 650px;
    background: #eeeeee;
    border-radius: 15px;
}}

</style>

</head>

<body>

<model-viewer

src="{model_url}"

camera-controls

auto-rotate

auto-rotate-delay="0"

rotation-per-second="20deg"

shadow-intensity="1"

exposure="1"

camera-orbit="0deg 75deg 3m"

field-of-view="30deg"

interaction-prompt="auto"

loading="eager"

reveal="auto"

alt="{company} {model} 3D Model">

</model-viewer>

</body>

</html>
"""

            components.html(
                html,
                height=700,
                scrolling=False
            )

            st.info(
                "🖱️ Drag = Rotate | 🔍 Scroll = Zoom | 🔄 Auto-rotate = ON"
            )

        except Exception as e:

            st.error(
                "❌ Error loading the 3D model"
            )

            st.exception(e)

# ============================================================
# VEHICLE DIAGNOSIS
# ============================================================

elif menu == "🔧 Vehicle Diagnosis":

    st.header("🔧 2-Wheeler Vehicle Diagnosis")

    col1, col2 = st.columns(2)

    with col1:

        company = st.selectbox(
            "Vehicle Company",
            list(vehicle_data.keys()),
            key="diagnosis_company"
        )

        model = st.selectbox(
            "Vehicle Model",
            list(vehicle_data[company].keys()),
            key="diagnosis_model"
        )

    with col2:

        year = st.number_input(
            "Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            key="diagnosis_year"
        )

        problem = st.selectbox(
            "Select Vehicle Problem",
            [
                "Engine Not Starting",
                "Battery Problem",
                "Brake Problem",
                "Tyre Problem",
                "Engine Overheating",
                "Oil Leakage",
                "Chain/Sprocket Problem",
                "Clutch Problem",
                "Gear Shifting Problem",
                "Poor Mileage",
                "Low Pickup",
                "Excessive Smoke",
                "Strange Noise",
                "Electrical Problem",
                "Other"
            ]
        )

    description = st.text_area(
        "📝 Describe Your Problem"
    )

    if st.button(
        "🔧 Diagnose Vehicle",
        use_container_width=True
    ):

        if not description.strip():

            st.warning(
                "⚠️ Please describe your vehicle problem."
            )

        else:

            st.success(
                "✅ Diagnosis Request Processed"
            )

            st.write(
                "🏍️ Vehicle:",
                company,
                model
            )

            st.write(
                "📅 Year:",
                year
            )

            st.write(
                "⚠️ Problem:",
                problem
            )

            st.write(
                "📝 Description:",
                description
            )

            st.info(
                "🤖 AI diagnosis model can be connected here using "
                "your machine-learning model and maintenance dataset."
            )

# ============================================================
# MAINTENANCE TIPS
# ============================================================

elif menu == "🛠 Maintenance Tips":

    st.header("🛠 2-Wheeler Maintenance Tips")

    company = st.selectbox(
        "Select Company",
        list(vehicle_data.keys()),
        key="maintenance_company"
    )

    model = st.selectbox(
        "Select Model",
        list(vehicle_data[company].keys()),
        key="maintenance_model"
    )

    st.success(
        f"Maintenance Guide: {company} {model}"
    )

    tips = [

        "🛢️ Check and replace engine oil at the recommended interval.",

        "🛞 Check tyre pressure regularly.",

        "⛓️ Inspect and lubricate the chain regularly.",

        "🔋 Check battery condition and terminals.",

        "🛑 Check brake pads/shoes and brake fluid.",

        "💡 Check headlights, indicators and brake lights.",

        "⚙️ Check clutch and gear operation.",

        "⛽ Keep the fuel system clean.",

        "🔧 Follow the manufacturer's service schedule.",

        "🏍️ Do not ignore unusual sounds, vibrations or smoke."

    ]

    for tip in tips:
        st.write(tip)

# ============================================================
# SERVICE HISTORY
# ============================================================

elif menu == "📋 Service History":

    st.header("📋 2-Wheeler Service History")

    col1, col2 = st.columns(2)

    with col1:

        owner = st.text_input(
            "👤 Owner Name",
            key="service_owner"
        )

        company = st.selectbox(
            "🏍️ Vehicle Company",
            list(vehicle_data.keys()),
            key="service_company"
        )

        model = st.selectbox(
            "🏍️ Vehicle Model",
            list(vehicle_data[company].keys()),
            key="service_model"
        )

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            key="service_year"
        )

    with col2:

        service_no = st.text_input(
            "🔢 Service Number"
        )

        km = st.number_input(
            "🛣️ Current Kilometer",
            min_value=0,
            step=100
        )

        service_date = st.date_input(
            "📅 Service Date"
        )

        service_type = st.selectbox(
            "🔧 Service Type",
            [
                "General Service",
                "Engine Oil Change",
                "Brake Service",
                "Battery Check",
                "Chain Adjustment",
                "Chain & Sprocket Replacement",
                "Tyre Replacement",
                "Clutch Service",
                "Air Filter Replacement",
                "Spark Plug Replacement",
                "Wheel Alignment"
            ]
        )

    cost = st.number_input(
        "💰 Service Cost (₹)",
        min_value=0,
        step=100
    )

    notes = st.text_area(
        "📝 Mechanic Notes"
    )

    if st.button(
        "💾 Save Service Record",
        use_container_width=True
    ):

        next_date = (
            service_date +
            timedelta(days=180)
        )

        next_km = km + 5000

        st.session_state["history"].append(
            {
                "Owner": owner,
                "Company": company,
                "Model": model,
                "Year": year,
                "Service No": service_no,
                "Date": service_date,
                "Service": service_type,
                "KM": km,
                "Cost": cost,
                "Notes": notes,
                "Next Date": next_date,
                "Next KM": next_km
            }
        )

        st.success(
            "✅ Service Record Saved Successfully!"
        )

    if len(st.session_state["history"]) > 0:

        st.subheader(
            "📜 Previous Service History"
        )

        df = pd.DataFrame(
            st.session_state["history"]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        latest = st.session_state["history"][-1]

        st.subheader(
            "⏰ Next Service Reminder"
        )

        st.info(
            f"""
🏍️ Vehicle: {latest['Company']} {latest['Model']}

📅 Manufacturing Year: {latest['Year']}

📅 Next Service Date: {latest['Next Date']}

🛣️ Next Service KM: {latest['Next KM']} KM

💰 Last Service Cost: ₹{latest['Cost']}
"""
        )

# ============================================================
# CONTACT SUPPORT
# ============================================================

elif menu == "📞 Contact Support":

    st.header("📞 Contact Support")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📧 Email Support")

        st.write(
            "support@aimechanical.com"
        )

    with col2:

        st.subheader("📱 Phone Support")

        st.write(
            "+91 9876543210"
        )

    st.markdown("---")

    st.info(
        "For emergency vehicle problems, contact a qualified "
        "mechanic or authorized service center."
    )

# ============================================================
# LOGOUT
# ============================================================

elif menu == "🚪 Logout":

    st.warning(
        "🚪 Are you sure you want to logout?"
    )

    if st.button(
        "🚪 Logout Now",
        use_container_width=True
    ):

        st.session_state["logged_in"] = False
        st.session_state["username"] = None

        st.success(
            "✅ Logged out successfully!"
        )

        st.switch_page("app.py")