import xml.etree.ElementTree as ET
import random
import numpy as np


# Function to generate random pose values
def random_pose(x_range, y_range, z_range, roll_range, pitch_range, yaw_range):
    x = random.uniform(*x_range)
    y = random.uniform(*y_range)
    z = random.uniform(*z_range)
    roll = random.uniform(*roll_range)
    pitch = random.uniform(*pitch_range)
    yaw = random.uniform(*yaw_range)
    return f"{x} {y} {z} {roll} {pitch} {yaw}"

# Load the SDF file
tree = ET.parse('random.sdf')
root = tree.getroot()

# Define ranges for randomization
x_range = (-5.0, 5.0)  # x position range
y_range = (-3.0, 3.0)  # y position range
z_range = (0.0, 3.0)   # z position range (height)
roll_range = (-np.pi, np.pi)  # roll orientation range
pitch_range = (-np.pi/2, np.pi/2)  # pitch orientation range
yaw_range = (-np.pi, np.pi)  # yaw orientation range

# Iterate through the models in the SDF file and randomize their poses
for model in root.findall('.//include'):
    pose = model.find('pose')
    if pose is not None:
        random_pose_values = random_pose(x_range, y_range, z_range, roll_range, pitch_range, yaw_range)
        pose.text = random_pose_values  # Update the pose values with randomized values

# Write the updated SDF file to a new file
tree.write('random.sdf')

print("Randomization complete! New world file saved.")
