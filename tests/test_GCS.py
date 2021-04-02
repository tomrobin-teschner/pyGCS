import pytest
import src.pyGCS as pyGCS
from math import fabs


@pytest.fixture
def airfoil_grid_4_grids():
    return pyGCS.GCS(dimension=2, simulation_order=2, volume=456.745, cells=[31719, 41002, 51383, 67209],
                     solution=[0.00919801, 0.00871879, 0.00852288, 0.00842471])


@pytest.fixture
def airfoil_grid_4_grids_reverse_order():
    return pyGCS.GCS(dimension=2, simulation_order=2, volume=456.745, cells=[67209, 51383, 41002, 31719],
                     solution=[0.00842471, 0.00852288, 0.00871879, 0.00919801])


def test_4_grids_gci(airfoil_grid_4_grids):
    # arrange
    sut = airfoil_grid_4_grids

    # act
    gci = sut.get('gci')

    # assert
    assert len(gci) == 2
    assert gci[0][0] < gci[0][1]
    assert gci[1][0] < gci[1][1]


def test_4_grids_asymptotic_gci(airfoil_grid_4_grids):
    # arrange
    sut = airfoil_grid_4_grids

    # act
    asymptotic_gci = sut.get('asymptotic_gci')

    # assert
    assert len(asymptotic_gci) == 2
    assert fabs(1 - asymptotic_gci[0]) > fabs(1 - asymptotic_gci[1])


def test_4_grids_extrapolated_value(airfoil_grid_4_grids):
    # arrange
    sut = airfoil_grid_4_grids

    # act
    extrapolated_value = sut.get('extrapolated_value')

    # assert
    assert len(extrapolated_value) == 2


def test_4_grids_asymptotic_gci(airfoil_grid_4_grids):
    # arrange
    sut = airfoil_grid_4_grids

    # act
    apparent_order = sut.get('apparent_order')

    # assert
    assert len(apparent_order) == 2


def test_4_grids_gci_reverse_order(airfoil_grid_4_grids, airfoil_grid_4_grids_reverse_order):
    # arrange
    sut = airfoil_grid_4_grids
    sut_reverse = airfoil_grid_4_grids_reverse_order

    # act
    gci = sut.get('gci')
    gci_reverse = sut_reverse.get('gci')

    # assert
    assert gci == gci_reverse
