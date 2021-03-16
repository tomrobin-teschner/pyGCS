[![PyPI license](https://img.shields.io/pypi/l/pygcs.svg)](https://pypi.python.org/pypi/pygcs/)
[![Generic badge](https://img.shields.io/badge/Version-v0.2.2-red.svg)](https://shields.io/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

# Introduction

pyGCS (Grid Convergence Study) is a python package that calculates the Grid Convergence Index (GCI) for solutions obtained through numerical analysis using computational grids to establish the error-band of the solution with respect to the numerical grid used. This package implements the equations presented in [1] and [2].

# Installation

To install pyCGS, run the following command

```bash
pip3 install pycgs
```

# Usage

The following shows how to calculate the GCI and get additional information that may be useful to establish grid independence.

```python
import pyGCS

# number of cells per grid
grids = [18000, 8000, 4500]

# volume of the simulation domain for each simulation
volume = [76, 76, 76]

# integral quantity for which to calculate the GCI
solution = [6.063, 5.972, 5.863]

# dimension of the simultion (here 2D)
dimension = 2

# create grid convergence study (gcs) object
gcs = pyGCS.GCI(dimension, volume, grids, solution)

# get GCI and supporting information
gci = gcs.get_gci()
asymptotic_gci = gcs.get_asymptotic_gci()
order = gcs.get_order()

# GCI_32 = 4.11%
print('GCI for coarse to medium grid (GCI_32): ' + str(gci[1] * 100) + '%')

# GCI_21 = 2.17%
print('GCI for medium to fine   grid (GCI_21): ' + str(gci[0] * 100) + '%')

# asymptotic GCI = 1.015
print('asymptotic GCI value (a value close to 1 indicates grid independence): ' + str(asymptotic_gci[0]))

# order = 1.53
print('order achieved in simulation: ' + str(order[0]))
```

# References

1. Celik et al. "Procedure of Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications", _Journal of Fluids Engineering_, 130(**7**), 2008  
2. https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html
