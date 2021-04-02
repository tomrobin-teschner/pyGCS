[![PyPI license](https://img.shields.io/pypi/l/pygcs.svg)](https://pypi.python.org/pypi/pygcs/)
[![Generic badge](https://img.shields.io/badge/Version-v0.4.2-red.svg)](https://shields.io/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

# Introduction

pyGCS (Grid Convergence Study) is a python package that calculates the Grid Convergence Index (GCI) for solutions obtained through numerical analysis using computational grids to establish the error-band of the solution with respect to the numerical grid used. This package implements the equations presented in [1] and [2].

# Installation

To install pyCGS, run the following command

```bash
pip3 install pycgs
```

# Usage

The following shows how to calculate the GCI and get additional information that may be useful to establish grid independence. Each GCI calculation requires the number of cells, the solution at each grid level and some information about the domain and its size. You can either specify directly a representative grid spacing (e.g. the square root of the cell area or cubed root of the cell volume in 2D or 3D, respectively) or the area / volume of the 2D / 3D domain. This, together with the number of cells, will then be used to calculate a representative grid size.

Additional information are the dimension of the simulation (1D, 2D, 3D) and the order used in the simulation. All these quantities need to be passed to the constructor of the GCI class but can be altered later if the GCI class is used dynamically while simulations are running through setter functions.

The following shows an example calculation taken from reference [1] and 3 different ways are presented how to calculated the GCI using either a fixed volume domain, a domain with potentially varying domain size and a domain for which we prescribe the representative size directly (and thus do not require any area / volume information about the simulation domain)

```python
import pyGCS

# create grid convergence study (gcs) object either based on volume og grid size
# single volume
gcs_single_volume = pyGCS.GCI(dimension=2, simulation_order=2, volume=76, cells=[18000, 8000, 4500],
                              solution=[6.063, 5.972, 5.863])

# potentially varying domain size
gcs_multiple_volumes = pyGCS.GCI(dimension=2, simulation_order=2, volume=[76, 76, 76], cells=[18000, 8000, 4500],
                                 solution=[6.063, 5.972, 5.863])

# specify representative grid spacing directly
gcs_with_grid_size = pyGCS.GCI(dimension=2, simulation_order=2, grid_size=[0.75, 1.125, 1.5],
                               cells=[18000, 8000, 4500], solution=[6.063, 5.972, 5.863])

# get GCI values (coarse-medium and medium-fine grid configuration)
gci_1 = gcs_single_volume.get('gci')
gci_2 = gcs_multiple_volumes.get('gci')
gci_3 = gcs_with_grid_size.get('gci')

# get the asymptotic GCI (for three grid levels, it is a single value)
asymptotic_gci_1 = gcs_single_volume.get('asymptotic_gci')
asymptotic_gci_2 = gcs_multiple_volumes.get('asymptotic_gci')
asymptotic_gci_3 = gcs_with_grid_size.get('asymptotic_gci')

# apparent (observed) order of the simulation (for three grid levels, it is a single value)
order_1 = gcs_single_volume.get('apparent_order')
order_2 = gcs_multiple_volumes.get('apparent_order')
order_3 = gcs_with_grid_size.get('apparent_order')

# extrapolated value we would achieve for a fine enough grid with no grid induced errors
extrapolated_value_1 = gcs_single_volume.get('extrapolated_value')
extrapolated_value_2 = gcs_multiple_volumes.get('extrapolated_value')
extrapolated_value_3 = gcs_with_grid_size.get('extrapolated_value')

# calculated grid size for a specified GCI value
recommend_grid_size_1 = gcs_single_volume.get_number_of_cells_for_specified_gci_of(0.01)
recommend_grid_size_2 = gcs_multiple_volumes.get_number_of_cells_for_specified_gci_of(0.01)
recommend_grid_size_3 = gcs_with_grid_size.get_number_of_cells_for_specified_gci_of(0.01)

# GCI_32 = 4.11%
print(f'GCI (1st approach) for coarse to medium grid (GCI_32): {gci_1[1] * 100:.2f}%')
print(f'GCI (2nd approach) for coarse to medium grid (GCI_32): {gci_2[1] * 100:.2f}%')
print(f'GCI (3rd approach) for coarse to medium grid (GCI_32): {gci_3[1] * 100:.2f}%\n')

# GCI_21 = 2.17%
print(f'GCI (1st approach) for medium to fine   grid (GCI_21): {gci_1[0] * 100:.2f}%')
print(f'GCI (2nd approach) for medium to fine   grid (GCI_21): {gci_2[0] * 100:.2f}%')
print(f'GCI (3rd approach) for medium to fine   grid (GCI_21): {gci_3[0] * 100:.2f}%\n')

# asymptotic GCI = 1.015
print(f'asymptotic GCI value (1st approach, a value close to 1 indicates grid independence): {asymptotic_gci_1[0]:.3f}')
print(f'asymptotic GCI value (2nd approach, a value close to 1 indicates grid independence): {asymptotic_gci_2[0]:.3f}')
print(f'asymptotic GCI value (3rd approach, a value close to 1 indicates grid independence): {asymptotic_gci_3[0]:.3f}\n')

# extrapolated value = 6.1685
print(f'Extrapolated value (1st approach): {extrapolated_value_1:.4f}')
print(f'Extrapolated value (2nd approach): {extrapolated_value_2:.4f}')
print(f'Extrapolated value (3rd approach): {extrapolated_value_3:.4f}\n')

# order = 1.53
print(f'order achieved in simulation (1st approach): {order_1[0]:.2f}')
print(f'order achieved in simulation (2nd approach): {order_2[0]:.2f}')
print(f'order achieved in simulation (3rd approach): {order_3[0]:.2f}\n')

# recommend_grid_size = 29872
print(f'Number of cells required to achieve a GCI of 1% (1st approach): {recommend_grid_size_1:.0f}')
print(f'Number of cells required to achieve a GCI of 1% (2nd approach): {recommend_grid_size_2:.0f}')
print(f'Number of cells required to achieve a GCI of 1% (3rd approach): {recommend_grid_size_3:.0f}')
```

# References

1. Celik et al. "Procedure of Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications", _Journal of Fluids Engineering_, 130(**7**), 2008  
2. https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html
