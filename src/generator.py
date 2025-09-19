# /src/generator.py

import numpy as np
import pandas as pd
import joblib
import os
import sys
import tensorflow as tf
from tensorflow.keras import layers, Model

# --- Path Correction ---
# Add the project root directory to the Python path.
# This allows us to import from the 'src' module, regardless of where this script is run from.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import our validator class
from src.validator import SpurGearValidator

class GearGenerator:
    """
    A class to generate new, verified spur gear designs using a trained CVAE model.
    """
    def __init__(self, model_dir='models'):
        """
        Initializes the generator by loading the trained decoder model and preprocessors.
        """
        print("Initializing GearGenerator...")
        # --- 1. Load Preprocessors ---
        self.preprocessor_conditions = joblib.load(os.path.join(model_dir, 'preprocessor_conditions.joblib'))
        self.preprocessor_design = joblib.load(os.path.join(model_dir, 'preprocessor_design.joblib'))
        print("Preprocessors loaded.")

        # --- 2. Load the entire Decoder Model ---
        # We now load from the .keras file, which is the modern, recommended format.
        self.decoder = tf.keras.models.load_model(os.path.join(model_dir, 'decoder_model.keras'))
        print("Decoder model loaded.")

        # --- 3. Store necessary dimensions from loaded components ---
        self.latent_dim = self.decoder.input_shape[0][1] # Get latent dim from model's input shape
        
        print("Initialization complete.")

    def _prepare_inputs(self, user_inputs: dict):
        """
        Takes raw user inputs and preprocesses them into the scaled,
        one-hot encoded format the model expects.
        """
        # Convert the single dictionary to a DataFrame with one row
        input_df = pd.DataFrame([user_inputs])
        
        # Ensure the column order is the same as during training
        # This is crucial for the preprocessor to work correctly
        condition_cols_ordered = [
            'power_kw', 'pinion_speed_rpm', 'ratio',
            'material_allowable_bending_stress_mpa', 'material_allowable_contact_stress_mpa',
            'material_name'
        ]
        input_df = input_df[condition_cols_ordered]

        # Transform the data
        processed_input = self.preprocessor_conditions.transform(input_df)
        return processed_input

    def _decode_outputs(self, model_outputs: np.ndarray):
        """
        Takes the raw, scaled output from the model and inverse-transforms it
        back into human-readable engineering values.
        """
        # Inverse transform to get real values
        real_outputs = self.preprocessor_design.inverse_transform(model_outputs)
        
        # Round the values to be realistic
        # Module: round to nearest 0.5
        real_outputs[:, 0] = np.round(real_outputs[:, 0] * 2) / 2
        # Pinion Teeth: round to nearest integer
        real_outputs[:, 1] = np.round(real_outputs[:, 1])
        # Face Width: round to nearest integer
        real_outputs[:, 2] = np.round(real_outputs[:, 2])
        
        return real_outputs

    def generate_verified_designs(self, user_inputs: dict, num_designs: int = 5):
        """
        The main public method. Generates and verifies designs until the
        requested number of unique, valid designs is found.
        """
        print(f"\nStarting generation for: {user_inputs}")
        # Prepare the user's input conditions once
        processed_conditions = self._prepare_inputs(user_inputs)
        
        valid_designs = []
        generated_hashes = set()
        
        attempts = 0
        max_attempts = 500 # To prevent infinite loops

        while len(valid_designs) < num_designs and attempts < max_attempts:
            # Generate a batch of random latent vectors
            # The batch size is larger than needed to increase chances of finding valid designs
            batch_size = num_designs * 10 # Increased batch size for better efficiency
            random_latent_vectors = np.random.normal(size=(batch_size, self.latent_dim))
            
            # Repeat the condition vector to match the batch size
            repeated_conditions = np.repeat(processed_conditions, batch_size, axis=0)
            
            # Use the decoder to generate a batch of design proposals
            generated_outputs = self.decoder.predict([random_latent_vectors, repeated_conditions], verbose=0)
            
            # Decode the proposals into real engineering values
            decoded_designs = self._decode_outputs(generated_outputs)
            
            # Verify each proposal
            for design in decoded_designs:
                module, pinion_teeth, face_width = design
                
                # Create a hash to check for uniqueness
                design_hash = (module, int(pinion_teeth), int(face_width))
                if design_hash in generated_hashes:
                    continue # Skip if we've already seen this exact design
                generated_hashes.add(design_hash)

                # Assemble the full parameter dictionary for the validator
                full_design_params = {
                    **user_inputs,
                    "module": module,
                    "pinion_teeth": int(pinion_teeth),
                    "face_width_mm": int(face_width),
                    "min_safety_factor": 1.5 # Assuming a fixed SF for now
                }
                
                validator = SpurGearValidator(full_design_params)
                if validator.is_valid():
                    valid_designs.append(full_design_params)
                    print(f"  Found valid design ({len(valid_designs)}/{num_designs}): {design_hash}")
                    # If we have enough, break the inner loop
                    if len(valid_designs) >= num_designs:
                        break
            
            attempts += 1

        if not valid_designs:
            print("Could not find enough valid designs within the attempt limit.")
        
        return valid_designs[:num_designs]


# --- Example Usage ---
if __name__ == "__main__":
    # Construct an absolute path to the models directory
    # This is more robust than using a relative path like '../models'
    model_path = os.path.join(project_root, 'models')
    
    # Create an instance of the generator using the robust path
    generator = GearGenerator(model_dir=model_path)
    
    # Define the user's requirements
    # This should be a challenging but feasible request based on our dataset
    user_request = {
        "power_kw": 25,
        "pinion_speed_rpm": 2000,
        "ratio": 2.5,
        "material_name": "HardenedSteel",
        "material_allowable_bending_stress_mpa": 250,
        "material_allowable_contact_stress_mpa": 1000,
    }
    
    # Generate 5 verified designs
    final_designs = generator.generate_verified_designs(user_request, num_designs=5)
    
    print("\n--- Final Verified Designs ---")
    if final_designs:
        for i, design in enumerate(final_designs):
            print(f"Option {i+1}:")
            print(f"  - Module: {design['module']}")
            print(f"  - Pinion Teeth: {design['pinion_teeth']}")
            print(f"  - Face Width: {design['face_width_mm']} mm")
    else:
        print("No designs were found that met the criteria.")
