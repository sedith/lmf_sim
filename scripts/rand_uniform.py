import xml.etree.ElementTree as ET
import numpy as np
import os


PATH_RESOURCES = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../resources')
PATH_WORLDS = os.path.join(PATH_RESOURCES, 'worlds/')
PATH_MODELS = os.path.join(PATH_RESOURCES, 'environment_assets/')


## function to generate random pose values
def random_pose(x_range, y_range, z_range, roll_range, pitch_range, yaw_range):
    x = np.random.uniform(*x_range)
    y = np.random.uniform(*y_range)
    z = np.random.uniform(*z_range)
    roll = np.random.uniform(*roll_range)
    pitch = np.random.uniform(*pitch_range)
    yaw = np.random.uniform(*yaw_range)
    return f"{x} {y} {z} {roll} {pitch} {yaw}"

## get list of models
models = []
for path, subdirs, files in os.walk(PATH_MODELS):
    if not path.endswith('unused'):
        for name in files:
            models.append(os.path.join(path, name))
print(str(np.random.choice(models)))

## load the SDF file
tree = ET.parse(os.path.join(PATH_WORLDS, 'empty.sdf'))
root = tree.getroot()

## find the <world> element
world = root.find('world')
if world is None:
    raise ValueError('no <world> element found in the SDF file')

## define ranges for randomization
x_range = (-5.0, 5.0)  # x position range
y_range = (-4.0, 4.0)  # y position range
z_range = (0.0, 3.0)   # z position range (height)
roll_range = (-np.pi, np.pi)  # roll orientation range
pitch_range = (-np.pi/2, np.pi/2)  # pitch orientation range
yaw_range = (-np.pi, np.pi)  # yaw orientation range

## randomize poses
n_obstacles = 50
for i in range(n_obstacles):
    include = ET.Element('include')

    static = ET.SubElement(include, 'static')
    static.text = 'true'

    name = ET.SubElement(include, 'name')
    name.text = f'obs_{i}'

    pose = ET.SubElement(include, 'pose')
    pose.text = random_pose(x_range, y_range, z_range, roll_range, pitch_range, yaw_range)

    uri = ET.SubElement(include, 'uri')
    uri.text = np.random.choice(models)

    world.append(include)

## write the updated SDF file to a new file
tree.write(os.path.join(PATH_WORLDS, 'random.sdf'), xml_declaration=True, method='xml', encoding='UTF-8')

print("Randomization complete! New world file saved.")
