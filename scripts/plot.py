#!/usr/bin/python

# Script:  plot.py
# Purpose: plots of a file of vectors
# Syntax:  plot.py gnu/matlab file
#          gnu/matlab = style of plots to create
#          file = a file with columns of data
# Example: plot.py gnu file.dat
# Author:  Steve Plimpton (Sandia)

# enable script to run from Python directly w/out Pizza.py

import sys

from gnu import gnu
from matlab import matlab
from plotview import plotview

if "argv" not in globals():
    argv = sys.argv

# main script

if len(argv) != 3:
    raise Exception("Syntax: plot.py gnu/matlab file")

style = argv[1]
file = argv[2]

v = vec(file)
exec("plot = %s()" % style)
p = plotview(v, plot)
