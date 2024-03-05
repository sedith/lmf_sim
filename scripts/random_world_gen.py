from gz.common5 import set_verbosity
from gz.sim8 import TestFixture, World, Model, world_entity
from gz.math7 import Vector3d

import os

set_verbosity(4)

file_path = os.path.dirname(os.path.realpath(__file__))

fixture = TestFixture(os.path.join(file_path, '../resources/worlds/empty.sdf'))

post_iterations = 0
iterations = 0
pre_iterations = 0
first_iteration = True


def on_pre_udpate_cb(_info, _ecm):
    global pre_iterations
    global first_iteration
    pre_iterations += 1
    if first_iteration:
        first_iteration = False
        world_e = world_entity(_ecm)
        print('World entity is ', world_e)
        w = World(world_e)
        rmf = w.model_by_name(_ecm, 'rmf_owl')
        print('Entity for falling model is: ', rmf)


def on_udpate_cb(_info, _ecm):
    global iterations
    iterations += 1


def on_post_udpate_cb(_info, _ecm):
    global post_iterations
    post_iterations += 1
    if _info.sim_time.seconds == 1:
        print('Post update sim time: ', _info.sim_time)


fixture.on_pre_update(on_pre_udpate_cb)
fixture.on_update(on_udpate_cb)
fixture.on_post_update(on_post_udpate_cb)
fixture.finalize()

server = fixture.server()
server.run(True, 1000, False)

print('iterations ', iterations)
print('post_iterations ', post_iterations)
print('pre_iterations ', pre_iterations)
