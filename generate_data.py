# /generate_data.py

import pandas as pd
from itertools import product
from tqdm import tqdm
import os

# Import our validator class from the src directory
from src.validator import SpurGearValidator

def generate_dataset():
    """
    Generates a dataset of valid spur gear designs by iterating through
    a predefined design space and validating each combination.
    """
    print("Starting dataset generation...")

    # --- 1. Define the Design Space ---
    # These are the ranges of parameters we will iterate through.
    # A wider range will create a more diverse dataset but take longer to run.

    # Input Conditions
    power_kw_range = [10, 20, 30, 40, 50]
    pinion_speed_rpm_range = [1000, 1500, 2000, 2500, 3000]
    ratio_range = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

    # Geometric Design Parameters
    module_range = [2, 2.5, 3, 3.5, 4, 5, 6]
    pinion_teeth_range = range(18, 41) # Range from 18 to 40 teeth
    face_width_mm_range = [f * 10 for f in range(3, 11)] # 30, 40, ..., 100 mm

    # Material Properties (List of material dictionaries)
    materials = [
        {
            "material_name": "StandardSteel",
            "material_allowable_bending_stress_mpa": 200,
            "material_allowable_contact_stress_mpa": 700,
        },
        {
            "material_name": "HardenedSteel",
            "material_allowable_bending_stress_mpa": 250,
            "material_allowable_contact_stress_mpa": 1000,
        }
    ]

    # Fixed Constraints
    min_safety_factor = 1.5
    pressure_angle_deg = 20.0

    # --- 2. Create All Possible Combinations ---
    # Use itertools.product to create a Cartesian product of all parameter lists.
    # This is more efficient than deeply nested for-loops.
    
    design_space = list(product(
        power_kw_range,
        pinion_speed_rpm_range,
        ratio_range,
        module_range,
        pinion_teeth_range,
        face_width_mm_range,
        materials
    ))
    
    total_combinations = len(design_space)
    print(f"Created {total_combinations:,} possible design combinations to test.")

    # --- 3. Iterate and Validate ---
    valid_designs = []
    
    # tqdm will create a smart progress bar
    for combo in tqdm(design_space, desc="Validating Designs"):
        # Unpack the current combination
        p_kw, np_rpm, ratio, mod, zp, b_mm, material = combo
        
        # Assemble the design parameter dictionary for the validator
        design_params = {
            "power_kw": p_kw,
            "pinion_speed_rpm": np_rpm,
            "ratio": ratio,
            "module": mod,
            "pinion_teeth": zp,
            "face_width_mm": b_mm,
            "pressure_angle_deg": pressure_angle_deg,
            "min_safety_factor": min_safety_factor,
            **material # Unpack the material properties into the dict
        }
        
        # Instantiate the validator and check the design
        validator = SpurGearValidator(design_params)
        if validator.is_valid():
            # If valid, add the complete parameter set to our list
            valid_designs.append(design_params)

    # --- 4. Save the Dataset ---
    print("\nValidation complete.")
    
    if not valid_designs:
        print("No valid designs were found. Consider widening parameter ranges or lowering constraints.")
        return

    print(f"Found {len(valid_designs):,} valid designs.")
    
    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(valid_designs)
    
    # Create a 'data' directory if it doesn't exist
    output_dir = 'data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Define the output path and save the file
    output_path = os.path.join(output_dir, 'valid_gear_designs.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Dataset successfully saved to: {output_path}")


if __name__ == "__main__":
    generate_dataset()
