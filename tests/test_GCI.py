import pytest
import src.pyGCS as pyGCS


def test_value_initialising_constructor():
    # arrange
    sut = pyGCS.GCI(dimension=2, volume=[10.45, 11.45, 12.45], cells=[100, 200, 400], solution=[0.8, 0.95, 1.0])

    # act
    volume = sut.get('volume')
    cells = sut.get('cells')
    solution = sut.get('solution')
    sut.set('safety_factor', 3.0)

    # assert
    assert sut.get('dimension') == 2
    assert sut.get('safety_factor') == 3.0

    assert len(volume) == 3
    assert volume[0] == 12.45
    assert volume[1] == 11.45
    assert volume[2] == 10.45

    assert len(cells) == 3
    assert cells[0] == 400
    assert cells[1] == 200
    assert cells[2] == 100

    assert len(solution) == 3
    assert solution[0] == 1.0
    assert solution[1] == 0.95
    assert solution[2] == 0.8


@pytest.fixture
def example_grid_celik():
    return pyGCS.GCI(dimension=2, volume=[76, 76, 76], cells=[18000, 8000, 4500], solution=[6.063, 5.972, 5.863])


@pytest.fixture
def example_grid_celik_single_volume():
    return pyGCS.GCI(dimension=2, volume=76, cells=[18000, 8000, 4500], solution=[6.063, 5.972, 5.863])


@pytest.fixture
def example_grid_celik_reverse_order():
    return pyGCS.GCI(dimension=2, volume=[76, 76, 76], cells=[4500, 8000, 18000], solution=[5.863, 5.972, 6.063])


@pytest.fixture
def example_grid_celik_random_order():
    return pyGCS.GCI(dimension=2, volume=[76, 76, 76], cells=[8000, 18000, 4500], solution=[5.972, 6.063, 5.863])


@pytest.fixture
def example_grid_celik_with_representative_size():
    return pyGCS.GCI(dimension=2, grid_size=[0.75, 1.125, 1.5], cells=[18000, 8000, 4500],
                     solution=[6.063, 5.972, 5.863])


def test_gci_calculation_based_on_volume(example_grid_celik):
    # arrange
    sut = example_grid_celik

    # act
    gci = sut.get('gci')

    # assert
    assert len(gci) == 2
    assert 0.0217 < gci[0] < 0.0218
    assert 0.0411 < gci[1] < 0.0412


def test_gci_calculation_based_on_single_volume(example_grid_celik_single_volume):
    # arrange
    sut = example_grid_celik_single_volume

    # act
    gci = sut.get('gci')

    # assert
    assert len(gci) == 2
    assert 0.0217 < gci[0] < 0.0218
    assert 0.0411 < gci[1] < 0.0412


def test_gci_calculation_based_on_representative_size(example_grid_celik_with_representative_size):
    # arrange
    sut = example_grid_celik_with_representative_size

    # act
    gci = sut.get('gci')

    # assert
    assert len(gci) == 2
    assert 0.0217 < gci[0] < 0.0218
    assert 0.0411 < gci[1] < 0.0412


def test_asymptotic_gci_calculation(example_grid_celik):
    # arrange
    sut = example_grid_celik

    # act
    asymptotic_gci = sut.get('asymptotic_gci')

    # assert
    assert len(asymptotic_gci) == 1
    assert 1.015 < asymptotic_gci[0] < 1.016


def test_extrapolated_value(example_grid_celik):
    # arrange
    sut = example_grid_celik

    # act
    extrapolated_value = sut.get('extrapolated_value')

    # assert
    assert 6.168 < extrapolated_value < 6.169


def test_desired_gci_calculation(example_grid_celik):
    # arrange
    sut = example_grid_celik
    cells = sut.get('cells')

    # act
    cells_for_smaller_gci = sut.get_number_of_cells_for_specified_gci_of(0.01)
    cells_for_larger_gci = sut.get_number_of_cells_for_specified_gci_of(0.03)

    # assert
    assert cells_for_smaller_gci > cells[0]
    assert cells_for_larger_gci < cells[0]


def test_order_calculation(example_grid_celik):
    # arrange
    sut = example_grid_celik

    # act
    order = sut.get('apparent_order')

    # assert
    assert len(order) == 1
    assert 1.53 < order[0] < 1.54


def test_gci_calculation_in_reverse_order(example_grid_celik_reverse_order):
    # arrange
    sut = example_grid_celik_reverse_order

    # act
    gci = sut.get('gci')

    # assert
    assert len(gci) == 2
    assert 0.0217 < gci[0] < 0.0218
    assert 0.0411 < gci[1] < 0.0412


def test_gci_calculation_in_random_order(example_grid_celik_random_order):
    # arrange
    sut = example_grid_celik_random_order

    # act
    gci = sut.get('gci')

    # assert
    assert len(gci) == 2
    assert 0.0217 < gci[0] < 0.0218
    assert 0.0411 < gci[1] < 0.0412
