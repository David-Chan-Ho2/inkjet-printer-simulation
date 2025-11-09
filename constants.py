import numpy as np

# Droplet Properties
DROPLET_DIAMETER = 84E-6        # Diameter of the droplet in meters [m]
DROPLET_CHARGE = -1.9E-10       # Charge of the droplet in Coulombs [C]
DROPLET_VELOCITY = 20           # Velocity of the droplet in meters per second [m/s]
DROPLET_DENSITY = 1000          # Density of the droplet in kilogram per meter cubed [kg/m^3]

# Printer Configuration
PRINTER_RESOLUTION = 300        # Printer resolution in dots per inch [dpi]
TOTAL_DISTANCE = 3E-3           # Distance between the droplet gun and the paper [m]
CAPACITOR_WIDTH = 1E-3          # Width of the capacitor [m]
CAPACITOR_LENGTH = 0.5E-3       # Length of the capacitor [m]
CAPACITOR_DISTANCE = 1.25E-3    # Distance between the capacitor and the paper [m]

# Paper Dimensions
PAPER_HEIGHT = 11               # Height of the paper in inches [in]
PAPER_WIDTH = 8.5               # Width of the paper in inches [in]

# Conversion
INCHES_2_METERS = 2.54E-2       # Conversion from inches to meters [m]

# Gun Visualization Geometry
GUN_WIDTH = 0.2E-3              # Small width for the gun [m]
GUN_HEIGHT = 0.5E-3             # Height of the gun, centered vertically [m]
GUN_X_START = -0.4E-3           # Position slightly before x=0 [m]
GUN_Y_START = -GUN_HEIGHT / 2   # Starting Y position of the gun [m]

# Animation Parameters
FRAMES_PER_DOT_INTERVAL = 50
ANIMATION_SPEED_FACTOR = 5000