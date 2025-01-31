#!/usr/bin/python

# Script:  logview.py
# Purpose: plots of LAMMPS log-file thermodynamic data
# Syntax:  logview.py gnu/matlab files ...
#          gnu/matlab = style of plots to create
#          files = one or more log files
# Example: logview.py gnu log.*
# Author:  Steve Plimpton (Sandia)

# enable script to run from Python directly w/out Pizza.py

import sys

from gnu import gnu
from log import log
from matlab import matlab
from plotview import plotview

if "argv" not in globals():
    argv = sys.argv

# main script

if len(argv) < 3:
    raise Exception("Syntax: logview.py gnu/matlab files  ...")

style = argv[1]
files = " ".join(argv[2:])

lg = log(files)
exec("plot = %s()" % style)
p = plotview(lg, plot)
