import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/piyush_hardreset/maze-solver/simulation/install/micromouse_sim'
