[![PyPI license](https://img.shields.io/pypi/l/pygcs.svg)](https://pypi.python.org/pypi/pygcs/)
[![Generic badge](https://img.shields.io/badge/Version-v0.3.0-red.svg)](https://shields.io/)
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

# get GCI values (coarse-medium and medium-fine grid configuration)
gci = gcs.get_gci()

# get the asymptotic GCI (for three grid levels, it is a single value)
asymptotic_gci = gcs.get_asymptotic_gci()

# apparent (observed) order of the simulation (for three grid levels, it is a single value)
order = gcs.get_order()

# extrapolated value we would achieve for a fine enough grid with no grid induced errors
extrapolated_value = gcs.get_extrapolated_value()

# calculated grid size for a specified GCI value
recommend_grid_size = gcs.get_number_of_cells_for_specified_gci_of(0.01)
    
# GCI_32 = 4.11%
print(f'GCI for coarse to medium grid (GCI_32): {gci[1] * 100:.2f}%')

# GCI_21 = 2.17%
print(f'GCI for medium to fine   grid (GCI_21): {gci[0] * 100:.2f}%')

# asymptotic GCI = 1.015
print(f'asymptotic GCI value (a value close to 1 indicates grid independence): {asymptotic_gci[0]:.3f}')

# extrapolated value = 6.1685
print(f'Extrapolated value: {extrapolated_value:.4f}')

# order = 1.53
print(f'order achieved in simulation: {order[0]:.2f}')

# recommend_grid_size = 29872
print(f'Number of cells required to achieve a GCI of 1%: {recommend_grid_size:.0f}')
```

# References

1. Celik et al. "Procedure of Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications", _Journal of Fluids Engineering_, 130(**7**), 2008  
2. https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html
