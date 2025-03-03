import streamlit as st
import google.generativeai as genai
import time
import pyperclip 
import json 
from streamlit_mic_recorder import mic_recorder
import matplotlib.pyplot as plt
import seaborn as sns 
import tkinter as tk

genai.configure(api_key="AIzaSyAOmHc2oPhLEe_n2-g3ZU4ZVKhG8c694_Y")

models = genai.list_models()
for model in models:
    print(model.name)

model = genai.GenerativeModel("gemini-2.0-flash") 

def chat_with_gemini(prompt):
    response = model.generate_content(prompt)  
    return response.text

st.set_page_config(page_title="UnitWizard & AI Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Montserrat:wght@400;700&family=Poppins:wght@400;700&display=swap');

    .main {
        background: linear-gradient(135deg, #F5F5F5, #E0E0E0);
        padding: 20px;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
        transition: background 0.5s ease, color 0.5s ease;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #2E3440, #4C566A);
        color: #FFFFFF;
        font-family: 'Roboto', sans-serif;
    }
    h1, h2, h3 {
        color: #4A90E2;
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button {
    color: #000000; /* Set text color to black */
    background-color: #E52020; /* Add a background color for visibility */
    border-radius: 5px;
    padding: 10px 20px;
    border: none;
    font-family: 'Roboto', sans-serif;
    transition: background 0.3s ease, color 0.3s ease;
}

  .stButton>button:hover {
    background-color: #C41C1C; /* Darker shade on hover */
    color: #FFFFFF; /* Change text color on hover */
}
    .footer {
        width: 100%;
        color: white;
        text-align: center;
        padding: 10px;
        font-family: 'Roboto', sans-serif;
    }
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .icon {
        font-size: 24px;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

dark_mode = st.sidebar.checkbox("Dark Mode 🌙")
if dark_mode:
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #1E1E1E, #2E2E2E);
            color: #FFFFFF;
        }
        h1, h2, h3 {
            color: #FFA500;
        }
        .stButton>button {
            background: linear-gradient(135deg, #FFA500, #FF8C00);
            color: white;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #FF8C00, #FFA500);
        }
        </style>
        """, unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='color: #FF6F61; text-align: center; font-family: "Georgia", serif; font-size: 2.5em;'>
        🌟 UnitWizard: Smart Conversion at Your Fingertips ✨
    </h1>
    """,
    unsafe_allow_html=True
)

unit_type = st.sidebar.selectbox("Select Conversion Type:", [
    "Length Converter", "Weight Converter", "Temperature Converter", 
    "Volume Converter", "Time Converter", "Area Converter", 
    "Pressure Converter", "Speed Converter", "Energy Converter"
])

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []

def swap_units():
    if 'from_unit' in st.session_state and 'to_unit' in st.session_state:
        st.session_state['from_unit'], st.session_state['to_unit'] = st.session_state['to_unit'], st.session_state['from_unit']

tab1, tab2, tab3 = st.tabs(["📏 Converter Unit", "🤖 Gemini Chatbot", "🎯 Quiz Mode"])

with tab1:
    if unit_type == "Length Converter":
        st.markdown("<h2 style='color: #FFA500;'><span class='icon'>📏</span>Length Converter</h2>", unsafe_allow_html=True)
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

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = [value * (length_units[to_unit] / length_units[from_unit]) for value in values]
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        amount = st.number_input("Enter length:", min_value=0.0, format="%.2f")
        from_unit = st.selectbox("From (Length):", list(length_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Length):", [u for u in length_units.keys() if u != from_unit], key='to_unit')

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Length"):
                with st.spinner('Converting...'):
                    time.sleep(1)
                    result = amount * (length_units[to_unit] / length_units[from_unit])
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals():
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Kilometre" and to_unit == "Metre":
            st.write("1 kilometer is approximately the length of 10 football fields.")
        elif from_unit == "Metre" and to_unit == "Centimetre":
            st.write("1 meter is approximately the height of a doorknob from the ground.")
        elif from_unit == "Inch" and to_unit == "Centimetre":
            st.write("1 inch is approximately the width of a standard paperclip.")

    elif unit_type == "Weight Converter":
        st.markdown("<h2 style='color: #FF5733;'><span class='icon'>⚖️</span>Weight Converter</h2>", unsafe_allow_html=True)
        st.write("Convert between different units of weight such as kilograms, grams, pounds, and ounces.")

        weight_units = {
            "Kilogram": 1,
            "Gram": 0.001,
            "Pound": 0.453592,
            "Ounce": 0.0283495
        }

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = [value * (weight_units[to_unit] / weight_units[from_unit]) for value in values]
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        amount = st.number_input("Enter weight:", min_value=0.0, format="%.2f")
        from_unit = st.selectbox("From (Weight):", list(weight_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Weight):", [u for u in weight_units.keys() if u != from_unit], key='to_unit')

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Weight"):
                with st.spinner('Converting...'):
                    time.sleep(1)  
                    result = amount * (weight_units[to_unit] / weight_units[from_unit])
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals(): 
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Kilogram" and to_unit == "Pound":
            st.write("1 kilogram is approximately the weight of a small pineapple.")
        elif from_unit == "Pound" and to_unit == "Ounce":
            st.write("1 pound is approximately the weight of a loaf of bread.")
        elif from_unit == "Gram" and to_unit == "Ounce":
            st.write("1 gram is approximately the weight of a paperclip.")

    elif unit_type == "Temperature Converter":
        st.markdown("<h2 style='color: #FF1493;'><span class='icon'>🌡️</span>Temperature Converter</h2>", unsafe_allow_html=True)
        st.write("Convert between different units of temperature such as Celsius, Fahrenheit, and Kelvin.")

        temperature_units = {
            "Celsius": 1,
            "Fahrenheit": 1,
            "Kelvin": 1
        }

        amount = st.number_input("Enter temperature:", format="%.2f")
        from_unit = st.selectbox("From (Temperature):", list(temperature_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Temperature):", [u for u in temperature_units.keys() if u != from_unit], key='to_unit')

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = []
            for value in values:
                if from_unit == "Celsius":
                    if to_unit == "Fahrenheit":
                        result = (value * 9/5) + 32
                    elif to_unit == "Kelvin":
                        result = value + 273.15
                    else:
                        result = value
                elif from_unit == "Fahrenheit":
                    if to_unit == "Celsius":
                        result = (value - 32) * 5/9
                    elif to_unit == "Kelvin":
                        result = (value - 32) * 5/9 + 273.15
                    else:
                        result = value
                elif from_unit == "Kelvin":
                    if to_unit == "Celsius":
                        result = value - 273.15
                    elif to_unit == "Fahrenheit":
                        result = (value - 273.15) * 9/5 + 32
                    else:
                        result = value
                results.append(result)
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Temperature"):
                with st.spinner('Converting...'):
                    time.sleep(1)  
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
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals(): 
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            st.write("0°C is the freezing point of water, which is 32°F.")
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            st.write("32°F is the freezing point of water, which is 0°C.")
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            st.write("0°C is 273.15K, the freezing point of water in Kelvin.")

    elif unit_type == "Volume Converter":
        st.markdown("<h2 style='color: #32CD32;'><span class='icon'>🧴</span>Volume Converter</h2>", unsafe_allow_html=True)
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

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = [value * (volume_units[to_unit] / volume_units[from_unit]) for value in values]
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        amount = st.number_input("Enter volume:", min_value=0.0, format="%.2f")
        from_unit = st.selectbox("From (Volume):", list(volume_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Volume):", [u for u in volume_units.keys() if u != from_unit], key='to_unit')

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Volume"):
                with st.spinner('Converting...'):
                    time.sleep(1)  
                    result = amount * (volume_units[to_unit] / volume_units[from_unit])
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals(): 
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Litre" and to_unit == "Millilitre":
            st.write("1 litre is equivalent to 1000 millilitres, roughly the volume of a standard water bottle.")
        elif from_unit == "Gallon" and to_unit == "Litre":
            st.write("1 gallon is approximately 3.785 litres, the volume of a large milk jug.")
        elif from_unit == "Fluid Ounce" and to_unit == "Millilitre":
            st.write("1 fluid ounce is approximately 29.57 millilitres, the volume of a standard shot glass.")

    elif unit_type == "Time Converter":
        st.markdown("<h2 style='color: #FFD700;'><span class='icon'>⏰</span>Time Converter</h2>", unsafe_allow_html=True)
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

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = [value * (time_units[to_unit] / time_units[from_unit]) for value in values]
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        amount = st.number_input("Enter time:", min_value=0.0, format="%.2f")
        from_unit = st.selectbox("From (Time):", list(time_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Time):", [u for u in time_units.keys() if u != from_unit], key='to_unit')

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Time"):
                with st.spinner('Converting...'):
                    time.sleep(1)  
                    result = amount * (time_units[to_unit] / time_units[from_unit])
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals():  
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Minute" and to_unit == "Second":
            st.write("1 minute is 60 seconds, the time it takes to boil an egg.")
        elif from_unit == "Hour" and to_unit == "Minute":
            st.write("1 hour is 60 minutes, the duration of a typical movie.")
        elif from_unit == "Day" and to_unit == "Hour":
            st.write("1 day is 24 hours, the time it takes for the Earth to complete one rotation.")

    elif unit_type == "Area Converter":
        st.markdown("<h2 style='color: #8A2BE2;'><span class='icon'>📐</span>Area Converter</h2>", unsafe_allow_html=True)
        st.write("Convert between different units of area such as square meters, square kilometers, square feet, and more.")

        area_units = {
            "Square Metre": 1,
            "Square Kilometre": 1000000,
            "Square Foot": 0.092903,
            "Acre": 4046.86,
            "Hectare": 10000
        }

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = [value * (area_units[to_unit] / area_units[from_unit]) for value in values]
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        amount = st.number_input("Enter area:", min_value=0.0, format="%.2f")
        from_unit = st.selectbox("From (Area):", list(area_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Area):", [u for u in area_units.keys() if u != from_unit], key='to_unit')

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Area"):
                with st.spinner('Converting...'):
                    time.sleep(1) 
                    result = amount * (area_units[to_unit] / area_units[from_unit])
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals():
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Square Metre" and to_unit == "Square Foot":
            st.write("1 square metre is approximately 10.76 square feet, the area of a small room.")
        elif from_unit == "Acre" and to_unit == "Square Metre":
            st.write("1 acre is approximately 4046.86 square metres, the area of a football field.")
        elif from_unit == "Hectare" and to_unit == "Acre":
            st.write("1 hectare is approximately 2.47 acres, the area of a large farm field.")

    elif unit_type == "Pressure Converter":
        st.markdown("<h2 style='color: #FF4500;'><span class='icon'>📉</span>Pressure Converter</h2>", unsafe_allow_html=True)
        st.write("Convert between different units of pressure such as Pascal, Bar, PSI, and more.")

        pressure_units = {
            "Pascal": 1,
            "Bar": 100000,
            "PSI": 6894.76,
            "Atmosphere": 101325,
            "Torr": 133.322
        }

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = [value * (pressure_units[to_unit] / pressure_units[from_unit]) for value in values]
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        amount = st.number_input("Enter pressure:", min_value=0.0, format="%.2f")
        from_unit = st.selectbox("From (Pressure):", list(pressure_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Pressure):", [u for u in pressure_units.keys() if u != from_unit], key='to_unit')

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Pressure"):
                with st.spinner('Converting...'):
                    time.sleep(1) 
                    result = amount * (pressure_units[to_unit] / pressure_units[from_unit])
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals():  
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Pascal" and to_unit == "Bar":
            st.write("1 Pascal is a very small unit of pressure, while 1 Bar is approximately the pressure of the Earth's atmosphere at sea level.")
        elif from_unit == "PSI" and to_unit == "Pascal":
            st.write("1 PSI is approximately 6894.76 Pascals, the pressure exerted by a small weight on a small area.")
        elif from_unit == "Atmosphere" and to_unit == "Torr":
            st.write("1 Atmosphere is approximately 760 Torr, the pressure exerted by a column of mercury 760 mm high.")

    elif unit_type == "Speed Converter":
        st.markdown("<h2 style='color: #00BFFF;'><span class='icon'>🚗</span>Speed Converter</h2>", unsafe_allow_html=True)
        st.write("Convert between different units of speed such as meters per second, kilometers per hour, miles per hour, and more.")

        speed_units = {
            "Metre per Second": 1,
            "Kilometre per Hour": 0.277778,
            "Mile per Hour": 0.44704,
            "Knot": 0.514444,
            "Foot per Second": 0.3048
        }

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = [value * (speed_units[to_unit] / speed_units[from_unit]) for value in values]
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        amount = st.number_input("Enter speed:", min_value=0.0, format="%.2f")
        from_unit = st.selectbox("From (Speed):", list(speed_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Speed):", [u for u in speed_units.keys() if u != from_unit], key='to_unit')

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Speed"):
                with st.spinner('Converting...'):
                    time.sleep(1) 
                    result = amount * (speed_units[to_unit] / speed_units[from_unit])
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals():  
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Metre per Second" and to_unit == "Kilometre per Hour":
            st.write("1 metre per second is approximately 3.6 kilometres per hour, the speed of a slow walk.")
        elif from_unit == "Mile per Hour" and to_unit == "Kilometre per Hour":
            st.write("1 mile per hour is approximately 1.609 kilometres per hour, the speed limit in many residential areas.")
        elif from_unit == "Knot" and to_unit == "Metre per Second":
            st.write("1 knot is approximately 0.514 metres per second, the speed of a ship at sea.")

    elif unit_type == "Energy Converter":
        st.markdown("<h2 style='color: #FF69B4;'><span class='icon'>⚡</span>Energy Converter</h2>", unsafe_allow_html=True)
        st.write("Convert between different units of energy such as Joules, Calories, Kilowatt-hours, and more.")

        energy_units = {
            "Joule": 1,
            "Calorie": 4.184,
            "Kilowatt-hour": 3600000,
            "British Thermal Unit (BTU)": 1055.06,
            "Electronvolt": 1.60218e-19
        }

        st.markdown("### Bulk Conversion")
        bulk_input = st.text_area("Enter multiple values (comma-separated):")
        if bulk_input:
            values = [float(x.strip()) for x in bulk_input.split(",")]
            results = [value * (energy_units[to_unit] / energy_units[from_unit]) for value in values]
            st.write("Bulk Conversion Results:")
            for value, result in zip(values, results):
                st.write(f"{value} {from_unit} = {result:.4f} {to_unit}")

        amount = st.number_input("Enter energy:", min_value=0.0, format="%.2f")
        from_unit = st.selectbox("From (Energy):", list(energy_units.keys()), key='from_unit')
        to_unit = st.selectbox("To (Energy):", [u for u in energy_units.keys() if u != from_unit], key='to_unit')

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Convert Energy"):
                with st.spinner('Converting...'):
                    time.sleep(1)  
                    result = amount * (energy_units[to_unit] / energy_units[from_unit])
                    st.markdown(f"<div class='fade-in'>{amount} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)
                    st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    pyperclip.copy(f"{amount} {from_unit} = {result:.4f} {to_unit}")
                    st.success("Result copied to clipboard!")
        with col2:
            if st.button("Swap Units 🔄", on_click=swap_units):
                pass

        if 'result' in locals() or 'result' in globals(): 
            st.markdown("### Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(x=[from_unit, to_unit], y=[amount, result], palette="viridis")
            ax.set_ylabel('Value')
            ax.set_title(f'Conversion from {from_unit} to {to_unit}')
            st.pyplot(fig)
        else:
            st.warning("Please perform a conversion first to view the graph.")

        st.markdown("### Real-World Example")
        if from_unit == "Joule" and to_unit == "Calorie":
            st.write("1 Joule is approximately 0.239 Calories, the energy required to lift a small apple 1 metre.")
        elif from_unit == "Kilowatt-hour" and to_unit == "Joule":
            st.write("1 Kilowatt-hour is 3.6 million Joules, the energy consumed by a 100-watt bulb in 10 hours.")
        elif from_unit == "British Thermal Unit (BTU)" and to_unit == "Joule":
            st.write("1 BTU is approximately 1055.06 Joules, the energy required to heat 1 pound of water by 1°F.")

with tab2:
    st.markdown("<h2 style='color: #4CAF50; text-align: center;'>🤖 Gemini Chatbot</h2>", unsafe_allow_html=True)

    if "chat_sessions" not in st.session_state:
        st.session_state["chat_sessions"] = []
    if "current_chat" not in st.session_state:
        st.session_state["current_chat"] = []

    def new_chat():
        """Starts a new chat session and adds the first user prompt as a label."""
        if st.session_state["current_chat"]:
            first_message = st.session_state["current_chat"][0]["content"] if st.session_state["current_chat"] else "New Chat"
            st.session_state["chat_sessions"].append({"label": first_message, "messages": st.session_state["current_chat"]})
        st.session_state["current_chat"] = []

    for message in st.session_state["current_chat"]:
        with st.chat_message(message["role"]):
            st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state["current_chat"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"**User:** {user_input}")

        with st.spinner("Thinking..."):
            bot_response = chat_with_gemini(user_input)
        
        st.session_state["current_chat"].append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(f"**Assistant:** {bot_response}")

with tab3:
    st.markdown("<h2 style='color: #FF4500; text-align: center;'>🎯 Quiz Mode</h2>", unsafe_allow_html=True)
    st.write("Test your knowledge of unit conversions with this fun quiz!")

    quiz_questions = [
        {
            "question": "How many meters are in 1 kilometer?",
            "options": ["10", "100", "1000", "10000"],
            "answer": "1000"
        },
        {
            "question": "How many grams are in 1 kilogram?",
            "options": ["10", "100", "1000", "10000"],
            "answer": "1000"
        },
        {
            "question": "How many seconds are in 1 minute?",
            "options": ["30", "60", "90", "120"],
            "answer": "60"
        },
        {
            "question": "How many liters are in 1 gallon?",
            "options": ["2.5", "3.785", "4.5", "5"],
            "answer": "3.785"
        },
        {
            "question": "How many centimeters are in 1 meter?",
            "options": ["10", "100", "1000", "10000"],
            "answer": "100"
        }
    ]

    if 'quiz_index' not in st.session_state:
        st.session_state['quiz_index'] = 0
    if 'score' not in st.session_state:
        st.session_state['score'] = 0

    current_question = quiz_questions[st.session_state['quiz_index']]
    st.markdown(f"**Question {st.session_state['quiz_index'] + 1}:** {current_question['question']}")
    user_answer = st.radio("Select your answer:", current_question['options'])

    if st.button("Submit Answer"):
        if user_answer == current_question['answer']:
            st.session_state['score'] += 1
            st.success("Correct! 🎉")
        else:
            st.error(f"Wrong! The correct answer is {current_question['answer']}.")

        if st.session_state['quiz_index'] < len(quiz_questions) - 1:
            st.session_state['quiz_index'] += 1
        else:
            st.balloons()
            st.markdown(f"### Quiz Complete! Your score is {st.session_state['score']}/{len(quiz_questions)}")
            if st.button("Restart Quiz"):
                st.session_state['quiz_index'] = 0
                st.session_state['score'] = 0

if st.session_state['history']:
    st.sidebar.markdown("### Conversion History")
    for item in st.session_state['history']:
        st.sidebar.write(item)
    if st.sidebar.button("Clear History"):
        st.session_state['history'] = []

st.sidebar.markdown("### Favorites")
favorite_conversion = st.sidebar.text_input("Add a favorite conversion (e.g., 'Meters to Feet'):")
if st.sidebar.button("Add Favorite"):
    if favorite_conversion:
        st.session_state['favorites'].append(favorite_conversion)
        st.sidebar.success(f"Added '{favorite_conversion}' to favorites!")

if st.session_state['favorites']:
    st.sidebar.markdown("#### Saved Favorites")
    for fav in st.session_state['favorites']:
        st.sidebar.write(fav)

st.markdown("<div class='footer'>Made with ❤️ by Areesha Abdul Sattar</div>", unsafe_allow_html=True)