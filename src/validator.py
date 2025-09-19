# /src/validator.py

import math

class SpurGearValidator:
    """
    A class to validate a single spur gear pair design based on geometric
    and stress constraints.

    Formulas are based on simplified, standard mechanical engineering principles
    (e.g., Lewis Bending Equation, Buckingham's wear equation) with factors
    approximated from AGMA standards for preliminary design.
    """

    def __init__(self, design_params: dict):
        """
        Initializes the validator with all design parameters.

        Args:
            design_params (dict): A dictionary containing all required
                                  parameters for the gear pair design.
        """
        # --- Unpack Input Parameters ---
        # Performance
        self.P_kw = design_params['power_kw']
        self.Np_rpm = design_params['pinion_speed_rpm']
        self.ratio = design_params['ratio']
        
        # Geometry
        self.m = design_params['module']
        self.Zp = int(design_params['pinion_teeth'])
        self.b_mm = design_params['face_width_mm']
        self.phi_deg = design_params.get('pressure_angle_deg', 20.0)

        # Material Properties (for both gears, assumed to be the same steel)
        self.mat_allowable_bending_stress = design_params['material_allowable_bending_stress_mpa']
        self.mat_allowable_contact_stress = design_params['material_allowable_contact_stress_mpa']
        self.elastic_coeff_Cp = design_params.get('elastic_coefficient_cp', 191) # For Steel-Steel

        # Constraints
        self.min_safety_factor = design_params['min_safety_factor']
        
        # --- Pre-calculate Derived Properties ---
        self.phi_rad = math.radians(self.phi_deg)
        self.Zg = int(round(self.Zp * self.ratio))
        
        # Diameters
        self.dp_mm = self.m * self.Zp
        self.dg_mm = self.m * self.Zg
        
        # Center Distance
        self.C_mm = (self.dp_mm + self.dg_mm) / 2
        
        # Pitch-line velocity
        self.v_mps = (math.pi * self.dp_mm * self.Np_rpm) / (60 * 1000)
        
        # Transmitted Load
        self.Wt_N = self._calculate_tangential_load()

    def _calculate_tangential_load(self) -> float:
        """Calculates the tangential load (transmitted load) in Newtons."""
        power_watts = self.P_kw * 1000
        if self.v_mps == 0:
            return 0
        return power_watts / self.v_mps

    def _check_interference(self) -> (bool, str):
        """
        Checks for interference. Uses a simplified rule for standard gears.
        A common rule of thumb for a 20-degree pressure angle is Zp >= 17.
        """
        min_teeth = 17 
        if self.Zp < min_teeth:
            return False, f"Interference Risk: Pinion teeth ({self.Zp}) is less than recommended minimum ({min_teeth})."
        return True, "No interference."

    def _check_contact_ratio(self) -> (bool, str):
        """
        Calculates and checks the contact ratio. Must be > 1.4 for smooth operation.
        """
        # Radii
        r_p = self.dp_mm / 2
        r_g = self.dg_mm / 2
        
        # Addendum assuming standard full-depth teeth (addendum = 1 * module)
        addendum = self.m
        ra_p = r_p + addendum
        ra_g = r_g + addendum
        
        # Base circle radii
        rb_p = r_p * math.cos(self.phi_rad)
        rb_g = r_g * math.cos(self.phi_rad)
        
        # Path of contact
        p1 = math.sqrt(ra_p**2 - rb_p**2)
        p2 = math.sqrt(ra_g**2 - rb_g**2)
        p3 = self.C_mm * math.sin(self.phi_rad)
        
        path_of_contact = p1 + p2 - p3
        
        # Base pitch
        pb = self.m * math.pi * math.cos(self.phi_rad)
        
        contact_ratio = path_of_contact / pb
        
        if contact_ratio < 1.4:
            return False, f"Contact Ratio ({contact_ratio:.2f}) is below the recommended minimum of 1.4."
        return True, f"Contact Ratio ({contact_ratio:.2f}) is acceptable."

    def _calculate_stresses(self) -> (float, float):
        """
        Calculates both bending and contact stresses.
        Returns:
            (max_bending_stress_mpa, contact_stress_mpa)
        """
        # --- K Factors (simplified approximations) ---
        # Dynamic Factor (Barth's Equation for standard quality gears)
        Kv = (6.1 + self.v_mps) / 6.1
        # Overload Factor (assuming moderate shock)
        Ko = 1.25
        # Load Distribution Factor (assuming standard mounting)
        Km = 1.3
        
        # --- Bending Stress (Lewis Formula with AGMA factors) ---
        # Lewis Form Factor (Y) - approximation
        Yp = 0.484 - (2.87 / self.Zp)
        Yg = 0.484 - (2.87 / self.Zg)
        
        # The gear with the smaller form factor is weaker (usually the pinion)
        bending_stress_p = (self.Wt_N * Kv * Ko * Km) / (self.b_mm * self.m * Yp)
        bending_stress_g = (self.Wt_N * Kv * Ko * Km) / (self.b_mm * self.m * Yg)
        max_bending_stress = max(bending_stress_p, bending_stress_g)

        # --- Contact Stress (Buckingham's Wear Equation) ---
        # Geometry Factor (I)
        I = (math.sin(self.phi_rad) * math.cos(self.phi_rad) / 2) * (self.ratio / (self.ratio + 1))
        
        if self.b_mm * self.dp_mm * I == 0:
             contact_stress = float('inf')
        else:
             load_term = (self.Wt_N * Kv * Ko * Km) / (self.b_mm * self.dp_mm * I)
             contact_stress = self.elastic_coeff_Cp * math.sqrt(load_term)

        return max_bending_stress, contact_stress

    def is_valid(self, verbose=False) -> bool:
        """
        Runs all checks to validate the entire gear design.

        Args:
            verbose (bool): If True, prints the reason for success or failure.
        
        Returns:
            bool: True if the design is valid, False otherwise.
        """
        # 1. Geometric Checks
        is_ok, reason = self._check_interference()
        if not is_ok:
            if verbose: print(f"FAIL: {reason}")
            return False
            
        is_ok, reason = self._check_contact_ratio()
        if not is_ok:
            if verbose: print(f"FAIL: {reason}")
            return False

        # 2. Stress and Safety Factor Checks
        bending_stress, contact_stress = self._calculate_stresses()
        
        sf_bending = self.mat_allowable_bending_stress / bending_stress if bending_stress > 0 else float('inf')
        sf_contact = self.mat_allowable_contact_stress / contact_stress if contact_stress > 0 else float('inf')

        if sf_bending < self.min_safety_factor:
            if verbose: print(f"FAIL: Bending safety factor ({sf_bending:.2f}) is below minimum ({self.min_safety_factor}). Stress: {bending_stress:.1f} MPa.")
            return False

        if sf_contact < self.min_safety_factor:
            if verbose: print(f"FAIL: Contact safety factor ({sf_contact:.2f}) is below minimum ({self.min_safety_factor}). Stress: {contact_stress:.1f} MPa.")
            return False
            
        if verbose:
            print("SUCCESS: Design is valid.")
            print(f"  - Bending Safety Factor: {sf_bending:.2f}")
            print(f"  - Contact Safety Factor: {sf_contact:.2f}")

        return True


# --- Example Usage ---
if __name__ == "__main__":
    
    # Common material properties for a standard steel gear
   # Change the material properties to reflect a stronger, heat-treated steel
    hardened_steel_material = {
        "material_allowable_bending_stress_mpa": 250,  # Stronger in bending
        "material_allowable_contact_stress_mpa": 1000, # Significantly stronger in contact
    }

    # 1. A DESIGN THAT SHOULD WORK
    print("--- Checking Good Design ---")
    good_design = {
        "power_kw": 50,
        "pinion_speed_rpm": 3000,
        "ratio": 4.0,
        "module": 6,
        "pinion_teeth": 38,
        "face_width_mm": 97,
        "min_safety_factor": 1.5,
        **hardened_steel_material # Use the new, stronger material
    }
    validator = SpurGearValidator(good_design)
    validator.is_valid(verbose=True)
    print("\n" + "="*30 + "\n")


    # 2. A DESIGN THAT SHOULD FAIL DUE TO INTERFERENCE
    print("--- Checking Bad Design (Interference) ---")
    bad_design_interference = good_design.copy()
    bad_design_interference["pinion_teeth"] = 15 # Too few teeth
    
    validator = SpurGearValidator(bad_design_interference)
    validator.is_valid(verbose=True)
    print("\n" + "="*30 + "\n")


    # 3. A DESIGN THAT SHOULD FAIL DUE TO STRESS
    print("--- Checking Bad Design (Stress Failure) ---")
    bad_design_stress = good_design.copy()
    bad_design_stress["face_width_mm"] = 15 # Too narrow to handle the load
    
    validator = SpurGearValidator(bad_design_stress)
    validator.is_valid(verbose=True)
    print("\n" + "="*30 + "\n")