# /app.py

import streamlit as st
import pandas as pd
import os
import sys

# --- Path Correction ---
# This ensures we can import our generator from the src directory
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.generator import GearGenerator

# --- App Configuration ---
st.set_page_config(
    page_title="AI Spur Gear Designer",
    page_icon="⚙️",
    layout="wide"
)

# --- Caching the Generator ---
# This is crucial! It prevents the app from reloading the heavyweight
# TensorFlow model every time a widget is changed. The generator is
# created once and reused for subsequent requests.
@st.cache_resource
def load_generator():
    """Loads the GearGenerator instance and caches it."""
    model_path = os.path.join(project_root, 'models')
    try:
        generator = GearGenerator(model_dir=model_path)
        return generator
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        st.error("Please ensure the 'models' directory and its contents are in the correct location.")
        return None

generator = load_generator()

# --- UI Layout ---
st.title("⚙️ AI-Powered Spur Gear Designer")
st.write(
    "Specify your design requirements in the sidebar. The AI model will generate "
    "multiple valid gear design options that meet your criteria."
)

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("Design Requirements")

    # --- Performance Inputs ---
    st.subheader("Performance")
    power_kw = st.slider("Power (kW)", min_value=5, max_value=50, value=25, step=5)
    pinion_speed_rpm = st.slider("Pinion Speed (RPM)", min_value=500, max_value=3000, value=2000, step=100)
    ratio = st.slider("Gear Ratio", min_value=1.5, max_value=4.0, value=2.5, step=0.1)

    # --- Material Selection ---
    st.subheader("Material")
    # Define material properties in a dictionary for easy lookup
    material_options = {
        "Standard Steel": {
            "material_name": "StandardSteel",
            "material_allowable_bending_stress_mpa": 200,
            "material_allowable_contact_stress_mpa": 700,
        },
        "Hardened Steel": {
            "material_name": "HardenedSteel",
            "material_allowable_bending_stress_mpa": 250,
            "material_allowable_contact_stress_mpa": 1000,
        }
    }
    selected_material_name = st.selectbox("Select Material", options=list(material_options.keys()))
    
    # Get the full properties dictionary for the selected material
    material_properties = material_options[selected_material_name]

    # --- Generate Button ---
    st.write("---")
    num_designs_to_generate = st.number_input("Number of designs to generate", min_value=1, max_value=10, value=3)
    
    generate_button = st.button("Generate Designs", type="primary", use_container_width=True)


# --- Main Content Area for Displaying Results ---
if generate_button and generator:
    # Assemble the user request dictionary
    user_request = {
        "power_kw": power_kw,
        "pinion_speed_rpm": pinion_speed_rpm,
        "ratio": ratio,
        **material_properties
    }

    # Use a spinner to show that the app is working
    with st.spinner("🧠 AI is thinking... Generating and verifying designs..."):
        try:
            final_designs = generator.generate_verified_designs(
                user_request, 
                num_designs=num_designs_to_generate
            )
        except Exception as e:
            st.error(f"An error occurred during generation: {e}")
            final_designs = []

    st.subheader("Generated Design Options & Measurements")

    if final_designs:
        # Create a list to hold the display data
        display_data = []
        for design in final_designs:
            # --- Calculate additional measurements ---
            module = design['module']
            pinion_teeth = design['pinion_teeth']
            
            gear_teeth = round(pinion_teeth * user_request['ratio'])
            pinion_diameter = module * pinion_teeth
            gear_diameter = module * gear_teeth
            center_distance = (pinion_diameter + gear_diameter) / 2
            
            display_data.append({
                "Module": module,
                "Pinion Teeth": pinion_teeth,
                "Gear Teeth": gear_teeth,
                "Face Width (mm)": design['face_width_mm'],
                "Pinion Diameter (mm)": f"{pinion_diameter:.2f}",
                "Gear Diameter (mm)": f"{gear_diameter:.2f}",
                "Center Distance (mm)": f"{center_distance:.2f}"
            })
        
        # Display results in a clean DataFrame
        df_results = pd.DataFrame(display_data)
        st.dataframe(df_results, use_container_width=True)

    else:
        st.warning(
            "No valid designs could be found for the specified requirements. "
            "This can happen if the constraints are too demanding for the selected material. "
            "Try increasing the power of the material or reducing the load/speed."
        )

elif not generator:
    st.error("Generator could not be loaded. The application cannot run.")
