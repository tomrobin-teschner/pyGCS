import pytest
import src.pyGCS as pyGCS


def test_empty_constructor():
    # arrange
    sut = pyGCS.GCI()

    # assert
    assert sut.get_dimension() == 3
    assert sut.get_safety_factor() == 1.25
    assert len(sut.get_volume()) == 0
    assert len(sut.get_cells()) == 0
    assert len(sut.get_solution()) == 0


def test_value_initialising_constructor():
    # arrange
    sut = pyGCS.GCI(2, [10.45, 11.45, 12.45], [100, 200, 400], [0.8, 0.95, 1.0])

    # act
    volume = sut.get_volume()
    cells = sut.get_cells()
    solution = sut.get_solution()
    sut.set_safety_factor(3.0)

    # assert
    assert sut.get_dimension() == 2

    assert sut.get_safety_factor() == 3.0

    assert len(volume) == 3
    assert volume[0] == 10.45
    assert volume[1] == 11.45
    assert volume[2] == 12.45

    assert len(cells) == 3
    assert cells[0] == 100
    assert cells[1] == 200
    assert cells[2] == 400

    assert len(solution) == 3
    assert solution[0] == 0.8
    assert solution[1] == 0.95
    assert solution[2] == 1.0


def test_volume_setter():
    # arrange
    sut = pyGCS.GCI()

    # act
    sut.set_volume([10.45, 15.55])

    # assert
    assert len(sut.get_volume()) == 2
    assert sut.get_volume()[0] == 10.45
    assert sut.get_volume()[1] == 15.55


def test_cell_count_setter():
    # arrange
    sut = pyGCS.GCI()

    # act
    sut.set_cells([1, 2])

    # assert
    assert len(sut.get_cells()) == 2
    assert sut.get_cells()[0] == 1
    assert sut.get_cells()[1] == 2


def test_solution_setter():
    # arrange
    sut = pyGCS.GCI()

    # act
    sut.set_solution([0.99, 1.0])

    # assert
    assert len(sut.get_solution()) == 2
    assert sut.get_solution()[0] == 0.99
    assert sut.get_solution()[1] == 1.0


@pytest.fixture
def grid_parameter():
    return {
        'volume': [76, 76, 76],
        'grids': [18000, 8000, 4500],
        'solution': [6.063, 5.972, 5.863]
    }


@pytest.fixture
def grid_parameter_reverse_order():
    return {
        'volume': [76, 76, 76],
        'grids': [4500, 8000, 18000],
        'solution': [5.863, 5.972, 6.063]
    }


@pytest.fixture
def grid_parameter_random_order():
    return {
        'volume': [76, 76, 76],
        'grids': [8000, 18000, 4500],
        'solution': [5.972, 6.063, 5.863]
    }


def test_gci_calculation_based_on_volume(grid_parameter):
    # arrange
    sut = pyGCS.GCI(2, grid_parameter['volume'], grid_parameter['grids'], grid_parameter['solution'])

    # act
    gci = sut.get_gci()

    # assert
    assert len(gci) == 2
    assert 0.0217 < gci[0] < 0.0218
    assert 0.0411 < gci[1] < 0.0412


def test_asymptotic_gci_calculation(grid_parameter):
    # arrange
    sut = pyGCS.GCI(2, grid_parameter['volume'], grid_parameter['grids'], grid_parameter['solution'])

    # act
    asymptotic_gci = sut.get_asymptotic_gci()

    # assert
    assert len(asymptotic_gci) == 1
    assert 1.015 < asymptotic_gci[0] < 1.016


def test_extrapolated_value(grid_parameter):
    # arrange
    sut = pyGCS.GCI(2, grid_parameter['volume'], grid_parameter['grids'], grid_parameter['solution'])

    # act
    extrapolated_value = sut.get_extrapolated_value()

    # assert
    assert 6.168 < extrapolated_value < 6.169


def test_desired_gci_calculation(grid_parameter):
    # arrange
    sut = pyGCS.GCI(2, grid_parameter['volume'], grid_parameter['grids'], grid_parameter['solution'])

    # act
    cells_for_smaller_gci = sut.get_number_of_cells_for_specified_gci_of(0.01)
    cells_for_larger_gci = sut.get_number_of_cells_for_specified_gci_of(0.03)

    # assert
    assert cells_for_smaller_gci > grid_parameter['grids'][0]
    assert cells_for_larger_gci < grid_parameter['grids'][0]


def test_order_calculation(grid_parameter):
    # arrange
    sut = pyGCS.GCI(2, grid_parameter['volume'], grid_parameter['grids'], grid_parameter['solution'])

    # act
    order = sut.get_order()

    # assert
    assert len(order) == 1
    assert 1.53 < order[0] < 1.54


def test_gci_calculation_in_reverse_order(grid_parameter_reverse_order):
    # arrange
    sut = pyGCS.GCI(2, grid_parameter_reverse_order['volume'], grid_parameter_reverse_order['grids'],
                    grid_parameter_reverse_order['solution'])

    # act
    gci = sut.get_gci()

    # assert
    assert len(gci) == 2
    assert 0.0217 < gci[0] < 0.0218
    assert 0.0411 < gci[1] < 0.0412


def test_gci_calculation_in_random_order(grid_parameter_random_order):
    # arrange
    sut = pyGCS.GCI(2, grid_parameter_random_order['volume'], grid_parameter_random_order['grids'],
                    grid_parameter_random_order['solution'])

    # act
    gci = sut.get_gci()

    # assert
    assert len(gci) == 2
    assert 0.0217 < gci[0] < 0.0218
    assert 0.0411 < gci[1] < 0.0412
