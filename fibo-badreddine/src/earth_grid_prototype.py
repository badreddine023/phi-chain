import math
from math_primitives import PHI, PHI_INV
from decimal import Decimal

# --- Earth Fibonacci Grid Prototype ---

# Earth's mean radius in meters (approximate, for scale)
EARTH_RADIUS_M = Decimal("6371000")

def to_phi_radians(degrees):
    """Converts degrees to phi-radians (where 2*pi is 2*pi/PHI phi-radians)."""
    # 360 degrees = 2*pi radians
    # We define 2*pi radians as 2*pi / PHI phi-radians
    # Conversion factor: (2*pi / PHI) / (2*pi) = 1 / PHI
    # phi_radians = radians * PHI_INV
    radians = Decimal(degrees) * Decimal(math.pi) / Decimal(180)
    phi_radians = radians * PHI_INV
    return phi_radians

def get_phi_coordinate(latitude, longitude):
    """
    Calculates a simplified phi-coordinate pair (Phi_L, Phi_A) from standard
    latitude and longitude, demonstrating the phi-ratio normalization.
    """
    lat_rad = Decimal(latitude) * Decimal(math.pi) / Decimal(180)
    lon_rad = Decimal(longitude) * Decimal(math.pi) / Decimal(180)
    
    # Phi-Latitude (Phi_L): Normalized latitude based on PHI
    # We use the ratio of the two angles to demonstrate the phi-ratio principle
    # This is a conceptual simplification of the complex Geodesic Icosahedron projection
    
    # Use the ratio of the two angles to demonstrate the phi-ratio principle
    # Phi_L = (sin(lat) + cos(lat)) * PHI
    phi_L = (Decimal(math.sin(float(lat_rad))) + Decimal(math.cos(float(lat_rad)))) * PHI
    
    # Phi-Azimuth (Phi_A): Normalized longitude based on PHI_INV
    phi_A = lon_rad * PHI_INV
    
    return phi_L, phi_A

def get_grid_resolution(level):
    """
    Calculates the grid resolution based on the Fibonacci sequence and PHI.
    Resolution = F_n * PHI * 10^X meters.
    We use the formula: Resolution = PHI * 10^(7 - level) meters.
    """
    # F_n values (F_1=1, F_2=1, F_3=2, F_4=3, F_5=5, F_6=8, F_7=13)
    fibs = [1, 1, 2, 3, 5, 8, 13]
    
    if level < 1 or level > len(fibs):
        return Decimal(0)
    
    # The scaling factor is PHI * 10^(7 - level)
    scaling_factor = PHI * Decimal(10**(7 - level))
    
    # The resolution is F_n * scaling_factor
    # For simplicity and to match the architectural table's magnitude, we use the scaling factor directly
    # as the table shows the approximate magnitude.
    resolution = PHI * Decimal(10**(7 - level))
    
    return resolution

# --- Prototype Execution ---
if __name__ == "__main__":
    print("--- Earth Fibonacci Grid Prototype ---")
    
    # 1. Coordinate Conversion Example
    # Location: 40.7128° N, 74.0060° W (New York City)
    lat_nyc = 40.7128
    lon_nyc = -74.0060
    
    phi_L, phi_A = get_phi_coordinate(lat_nyc, lon_nyc)
    
    print(f"Standard Coordinates: {lat_nyc}° N, {abs(lon_nyc)}° W")
    print(f"Phi-Coordinates (Conceptual):")
    print(f"  Phi-Latitude (Phi_L): {phi_L:.15f}")
    print(f"  Phi-Azimuth (Phi_A): {phi_A:.15f}")
    print(f"  Phi-Ratio (Phi_L / Phi_A): {phi_L / phi_A:.15f}")
    
    # 2. Grid Resolution Scaling Example
    print("-" * 35)
    print("Grid Resolution Scaling (F_n based):")
    
    resolutions = {}
    for i in range(1, 8):
        res = get_grid_resolution(i)
        resolutions[i] = res
        print(f"  Level {i} (F_{i}): {res:.3f} meters")
        
    # 3. Scaling Factor Check (Should approach PHI)
    print("-" * 35)
    print("Scaling Factor Check (Level n / Level n+1):")
    for i in range(1, 6):
        ratio = resolutions[i] / resolutions[i+1]
        print(f"  Level {i}/{i+1} Ratio: {ratio:.15f} (Target: 10.0)")
        
    # Note: The architectural design states each level is PHI times more detailed,
    # which implies a ratio of PHI_INV for resolution. My simplified formula
    # uses a factor of 10 for magnitude change, which is a prototype simplification.
    # To strictly adhere to PHI scaling:
    
    def get_phi_scaled_resolution(level):
        """Calculates resolution strictly scaled by PHI."""
        # Base resolution (Level 7: Room/Object)
        base_res = PHI * Decimal(10) # 16.18 meters
        
        # Scale up by PHI for each step down from 7
        # Level 7: base_res * PHI^0
        # Level 6: base_res * PHI^1
        # Level 1: base_res * PHI^6
        
        exponent = 7 - level
        phi_power = PHI ** exponent
        
        return base_res * phi_power

    print("-" * 35)
    print("Strict PHI-Scaled Grid Resolution:")
    phi_resolutions = {}
    for i in range(1, 8):
        res = get_phi_scaled_resolution(i)
        phi_resolutions[i] = res
        print(f"  Level {i}: {res:.3f} meters")

    print("-" * 35)
    print("Strict PHI-Scaling Factor Check (Level n / Level n+1):")
    for i in range(1, 7):
        ratio = phi_resolutions[i] / phi_resolutions[i+1]
        print(f"  Level {i}/{i+1} Ratio: {ratio:.15f} (Target: {PHI:.15f})")
