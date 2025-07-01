import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mkapil/ros2_ws/maze-solver/install/micromouse_sim'
