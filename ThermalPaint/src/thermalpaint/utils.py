import math

def rgb_to_blind_angle(r: int, g: int, b: int) -> float:
    """
    Converts RGB color to a servo angle for the ThermoBlinds.
    Logic: RGB -> Hue -> Custom Mapping -> Angle
    """
    # 1. Normalize RGB
    min_val = min(r, g, b)
    max_val = max(r, g, b)
    delta = max_val - min_val

    # 2. Calculate Hue
    if delta == 0:
        h = 0.0
    elif max_val == r:
        h = 60.0 * ((g - b) / delta)
    elif max_val == g:
        h = 60.0 * (2.0 + (b - r) / delta)
    else:
        h = 60.0 * (4.0 + (r - g) / delta)

    if h < -30.0:
        h += 360.0

    # 3. Map Hue to Fin Angle (Equation 7 logic)
    # Cosine mapping based on Hue
    cos_arg = 1.0 - (330.0 - h) / 360.0
    cos_arg = max(-1.0, min(1.0, cos_arg)) # Clamp for safety

    angle = math.degrees(math.acos(cos_arg))

    # 4. Enforce Mechanical Limits
    if 0.0 < angle < 10.0:
        angle = 10.0
    elif angle < 0.0:
        angle = 10.0
    elif angle > 90.0:
        angle = 90.0
        
    return angle