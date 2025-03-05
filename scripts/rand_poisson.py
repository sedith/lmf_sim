import xml.etree.ElementTree as ET
import random
import numpy as np
import scipy as sp
import os
import copy


PATH_RESOURCES = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../resources')
PATH_WORLDS = os.path.join(PATH_RESOURCES, 'worlds/')
PATH_MODELS = os.path.join(PATH_RESOURCES, 'environment_assets/')


## generate random pose values
def random_poses(n, radius, range):
    poisson_engine = sp.stats.qmc.PoissonDisk(
        d=3,
        radius=radius / range,
        ncandidates=500,
        seed=None,
    )
    return (poisson_engine.random(n) - np.array([0.5, 0.5, 0])) * range


if __name__ == '__main__':
    ## load the SDF file
    tree = ET.parse(os.path.join(PATH_WORLDS, 'empty.sdf'))
    root = tree.getroot()

    ## find the <world> element
    world = root.find('world')
    if world is None:
        raise ValueError('no <world> element found in the SDF file')

    ## add random obstacles
    chunks_radius = [1.3, 1.3, 1.3]
    poisson_domain_size = 5
    x_offset = 2 + poisson_domain_size / 2
    obs_idx = 0
    for j,r in enumerate(chunks_radius):
        poisson_obs = random_poses(1000, r, poisson_domain_size)
        n_obstacles = poisson_obs.shape[0]
        print(f'placing {n_obstacles} obstacles in the chunk {j} (Poisson radius: {r})')
        for i in range(n_obstacles):
            include = ET.Element('include')

            static = ET.SubElement(include, 'static')
            static.text = 'true'

            name = ET.SubElement(include, 'name')
            name.text = f'obs_{obs_idx}'
            obs_idx += 1

            pose = ET.SubElement(include, 'pose')
            pose.text = f'{poisson_obs[i][0] + x_offset} {poisson_obs[i][1]} {poisson_obs[i][2]} 0 0 0'

            uri = ET.SubElement(include, 'uri')
            uri.text = os.path.join(PATH_MODELS, 'objects_large/sphere_50cm.urdf')

            world.append(include)
        x_offset += poisson_domain_size + 1

    ## update ground
    s_x = len(chunks_radius) * (poisson_domain_size + 1) + 4  # from -1m to 1m past the obstacles
    c_x = s_x / 2 - 1
    for model in world.findall('model'):
        if model.get('name') == 'ground_plane':
            field = model.find('link/collision/geometry/box/size')
            field.text = f'{s_x} {poisson_domain_size} 0.1'
            field = model.find('link/visual/geometry/box/size')
            field.text = f'{s_x} {poisson_domain_size} 0.1'
            field = model.find('link/pose')
            field.text = f'{c_x} 0 -0.05 0 0 0'
            ground = model
            break

    ## add ceiling
    ceil = copy.deepcopy(ground)
    ceil.set('name', 'ceil')
    field = ceil.find('link/pose')
    field.text = f'{c_x} 0 {poisson_domain_size + 0.05} 0 0 0'
    world.append(ceil)

    ## add left wall
    lwall = copy.deepcopy(ground)
    lwall.set('name', 'lwall')
    field = lwall.find('link/pose')
    field.text = f'{c_x} {poisson_domain_size / 2} {poisson_domain_size / 2} 1.57 0 0'
    world.append(lwall)

    ## add right wall
    rwall = copy.deepcopy(ground)
    rwall.set('name', 'rwall')
    field = rwall.find('link/pose')
    field.text = f'{c_x} {- poisson_domain_size / 2} {poisson_domain_size / 2} 1.57 0 0'
    world.append(rwall)

    ## write the updated SDF file to a new file
    tree.write(os.path.join(PATH_WORLDS, 'random.sdf'), xml_declaration=True, method='xml', encoding='UTF-8')

    print('randomization complete, new world file saved')
