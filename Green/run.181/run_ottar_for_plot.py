# /usr/bin/python3
#! /home/awickert/anaconda3/bin/python

"""
This is meant as a schematic example, using data from the Minnesota River at
Jordan (MN) stream gauge. Parameters are not calibrated to data, and are not
intended to fit real river-width measurements.
"""

import ottar

rw = ottar.RiverWidth.from_yaml('config_for_output.yaml')

rw.initialize()
rw.run()
rw.finalize()

