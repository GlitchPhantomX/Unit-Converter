import streamlit as st

# Custom CSS for Styling
st.markdown("""
    <style>
    .main {
        background-color: #F5F5F5;
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #2E3440;
        color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #4A90E2;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #357ABD;
    }
    .footer {
     
        width: 100%;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Dark Mode / Light Mode Toggle
dark_mode = st.sidebar.checkbox("Dark Mode 🌙")
if dark_mode:
    st.markdown("""
        <style>
        .main {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        h1, h2, h3 {
            color: #FFA500;
        }
        </style>
        """, unsafe_allow_html=True)

# Main Title
st.markdown(
    """
    <h1 style='color: #FF6F61; text-align: center; font-family: "Georgia", serif; font-size: 2.5em;'>
        🌟 UnitWizard: Smart Conversion at Your Fingertips ✨
    </h1>
    """,
    unsafe_allow_html=True
)

# Sidebar for Selecting Unit Type
unit_type = st.sidebar.radio("Select Conversion Type:", ["Length Converter", "Weight Converter", "Temperature Converter", "Volume Converter", "Time Converter", "Area Converter"])

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Length Converter
if unit_type == "Length Converter":
    st.markdown("<h2 style='color: #FFA500;'>📏 Length Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of length such as kilometers, meters, centimeters, and more.")

    length_units = {
        "Kilometre": 1000,
        "Metre": 1,
        "Centimetre": 0.01,
        "Millimetre": 0.001,
        "Micrometre": 0.000001,
        "Nanometre": 0.000000001,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254,
        "Nautical Mile": 1852
    }

    amount = st.number_input("Enter length:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Length):", list(length_units.keys()))
    to_unit = st.selectbox("To (Length):", list(length_units.keys()))

    if st.button("Convert Length"):
        result = amount * (length_units[to_unit] / length_units[from_unit])
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Weight Converter
elif unit_type == "Weight Converter":
    st.markdown("<h2 style='color: #FF5733;'>⚖️ Weight Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of weight such as kilograms, grams, pounds, and ounces.")

    weight_units = {
        "Kilogram": 1,
        "Gram": 0.001,
        "Pound": 0.453592,
        "Ounce": 0.0283495
    }

    amount = st.number_input("Enter weight:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Weight):", list(weight_units.keys()))
    to_unit = st.selectbox("To (Weight):", list(weight_units.keys()))

    if st.button("Convert Weight"):
        result = amount * (weight_units[to_unit] / weight_units[from_unit])
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Temperature Converter
elif unit_type == "Temperature Converter":
    st.markdown("<h2 style='color: #FF1493;'>🌡️ Temperature Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of temperature such as Celsius, Fahrenheit, and Kelvin.")

    temperature_units = {
        "Celsius": 1,
        "Fahrenheit": 1,
        "Kelvin": 1
    }

    amount = st.number_input("Enter temperature:", format="%.2f")
    from_unit = st.selectbox("From (Temperature):", list(temperature_units.keys()))
    to_unit = st.selectbox("To (Temperature):", list(temperature_units.keys()))

    if st.button("Convert Temperature"):
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                result = (amount * 9/5) + 32
            elif to_unit == "Kelvin":
                result = amount + 273.15
            else:
                result = amount
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                result = (amount - 32) * 5/9
            elif to_unit == "Kelvin":
                result = (amount - 32) * 5/9 + 273.15
            else:
                result = amount
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                result = amount - 273.15
            elif to_unit == "Fahrenheit":
                result = (amount - 273.15) * 9/5 + 32
            else:
                result = amount
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Volume Converter
elif unit_type == "Volume Converter":
    st.markdown("<h2 style='color: #32CD32;'>🧴 Volume Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of volume such as liters, milliliters, gallons, and more.")

    volume_units = {
        "Litre": 1,
        "Millilitre": 0.001,
        "Gallon": 3.78541,
        "Quart": 0.946353,
        "Pint": 0.473176,
        "Cup": 0.24,
        "Fluid Ounce": 0.0295735
    }

    amount = st.number_input("Enter volume:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Volume):", list(volume_units.keys()))
    to_unit = st.selectbox("To (Volume):", list(volume_units.keys()))

    if st.button("Convert Volume"):
        result = amount * (volume_units[to_unit] / volume_units[from_unit])
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Time Converter
elif unit_type == "Time Converter":
    st.markdown("<h2 style='color: #FFD700;'>⏰ Time Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of time such as seconds, minutes, hours, days, and more.")

    time_units = {
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800,
        "Month": 2628000,
        "Year": 31536000
    }

    amount = st.number_input("Enter time:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Time):", list(time_units.keys()))
    to_unit = st.selectbox("To (Time):", list(time_units.keys()))

    if st.button("Convert Time"):
        result = amount * (time_units[to_unit] / time_units[from_unit])
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Area Converter
elif unit_type == "Area Converter":
    st.markdown("<h2 style='color: #8A2BE2;'>📐 Area Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of area such as square meters, square kilometers, square feet, and more.")

    area_units = {
        "Square Metre": 1,
        "Square Kilometre": 1000000,
        "Square Foot": 0.092903,
        "Acre": 4046.86,
        "Hectare": 10000
    }

    amount = st.number_input("Enter area:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Area):", list(area_units.keys()))
    to_unit = st.selectbox("To (Area):", list(area_units.keys()))

    if st.button("Convert Area"):
        result = amount * (area_units[to_unit] / area_units[from_unit])
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Display History
if st.session_state['history']:
    st.sidebar.markdown("### Conversion History")
    for item in st.session_state['history']:
        st.sidebar.write(item)

# Footer
st.markdown("<div class='footer'>Made with ❤️ by Areesha Abdul Sattar</div>", unsafe_allow_html=True)