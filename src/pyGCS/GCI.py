from math import pow, log, fabs

class GCI:
    """This class accepts grid parameters as inputs to compute the GCI"""

    # = constructor ====================================================================================================
    def __init__(self, dimension=3, domain_volume=[], cell_count=[], solution=[]):
        self.__dimension = dimension
        self.__volume = domain_volume
        self.__cells = cell_count
        self.__solution = solution

        self.__gci_up_to_date = False
        self.__representative_grid_size = []
        self.__refinement_ratio = []
        self.__relative_error = []
        self.__order = []
        self.__relative_normalised_error = []
        self.__GCI = []
        self.__asymptotic_gci = []
        self.__safety_factor = 1.25
        if len(self.__cells) == 2:
            self.__safety_factor = 3.0

    # = public API =====================================================================================================

    # = private API ====================================================================================================
    def __calculate_gci(self):
        self.__sort_input_based_on_grid_size()
        self.__calculate_representative_grid_size()
        self.__calculate_refinement_ratio()
        self.__calculate_relative_error()
        self.__calculate_order()
        self.__calculate_relative_normalised_error()
        self.__calculate_gci_for_each_grid()
        if len(self.__cells) >= 3:
            self.__calculate_asymptotic_grid_convergence()

    def __sort_input_based_on_grid_size(self):
        self.__cells, self.__volume, self.__solution = zip(*sorted(zip(self.__cells, self.__volume, self.__solution),
                                                                   reverse=True))

    def __calculate_representative_grid_size(self):
        self.__representative_grid_size = []
        for grid in range(0, len(self.__cells)):
            h = pow(self.__volume[grid] / self.__cells[grid], 1.0 / self.__dimension)
            self.__representative_grid_size.append(h)

    def __calculate_refinement_ratio(self):
        self.__refinement_ratio = []
        assert len(self.__representative_grid_size) == len(self.__cells)
        for grid in range(1, len(self.__representative_grid_size)):
            h1 = self.__representative_grid_size[grid - 1]
            h2 = self.__representative_grid_size[grid]
            ratio = h2 / h1
            assert ratio > 1
            self.__refinement_ratio.append(ratio)
        assert len(self.__representative_grid_size) - 1 == len(self.__refinement_ratio)

    def __calculate_relative_error(self):
        self.__relative_error = []
        assert len(self.__solution) == len(self.__cells)
        for grid in range(1, len(self.__solution)):
            phi1 = self.__solution[grid - 1]
            phi2 = self.__solution[grid]
            self.__relative_error.append(phi2 - phi1)
        assert len(self.__relative_error) == len(self.__refinement_ratio)

    def __calculate_order(self):
        self.__order = []
        if len(self.__cells) == 2:
            pass
        elif len(self.__cells) > 2:
            self.__calculate_apparent_order()

    def __calculate_apparent_order(self):
        for grid in range(2, len(self.__cells)):
            e21 = self.__relative_error[grid - 2]
            e32 = self.__relative_error[grid - 1]

            r21 = self.__refinement_ratio[grid - 2]
            r32 = self.__refinement_ratio[grid - 1]

            p = self.__find_apparent_order_iteratively(e21, e32, r21, r32)
            self.__order.append(p)

    def __find_apparent_order_iteratively(self, e21, e32, r21, r32):
        eps = 1
        iteration = 1
        max_iteration = 100
        norm = 1
        p = 2
        while eps > 1e-10:
            p_old = p
            s = self.__sign(e32 / e21)
            q = log((pow(r21, p) - s) / (pow(r32, p) - s))
            p = (1.0 / log(r21)) * fabs(fabs(log(e32 / e21)) + q)

            residual = p - p_old
            if iteration == 1:
                norm = residual
            iteration += 1
            eps = residual / norm
            if iteration == max_iteration:
                print('WARNING: max number of iterations (' + str(max_iteration) +
                      ') reached for calculating apparent order p ...')
                break
        return p

    def __sign(self, value):
        if value == 0:
            return 0
        elif value > 0:
            return 1
        elif value < 0:
            return 0

    def __calculate_relative_normalised_error(self):
        self.__relative_normalised_error = []
        assert len(self.__solution) == len(self.__cells)
        for grid in range(1, len(self.__solution)):
            phi1 = self.__solution[grid - 1]
            phi2 = self.__solution[grid]
            self.__relative_normalised_error.append(fabs((phi1 - phi2) / phi1))
        assert len(self.__relative_normalised_error) == len(self.__refinement_ratio)

    def __calculate_gci_for_each_grid(self):
        self.__GCI = []
        for grid in range(1, len(self.__cells)):
            ea21 = self.__relative_normalised_error[grid - 1]
            r21 = self.__refinement_ratio[grid - 1]
            if len(self.__order) == 1:
                p = self.__order[0]
            else:
                p = self.__order[grid - 1]
            gci = (self.__safety_factor * ea21) / (pow(r21, p) - 1.0)
            self.__GCI.append(gci)
        assert len(self.__GCI) == len(self.__cells) - 1

    def __calculate_asymptotic_grid_convergence(self):
        self.__asymptotic_gci = []
        for grid in range(2, len(self.__cells)):
            if len(self.__order) == 1:
                p = self.__order[0]
            else:
                p = self.__order[grid - 2]
            gci21 = self.__GCI[grid - 2]
            gci32 = self.__GCI[grid - 1]
            r21 = self.__refinement_ratio[grid - 2]
            asymptotic_gci = gci32 / (pow(r21, p) * gci21)
            self.__asymptotic_gci.append(asymptotic_gci)

    def __check_if_gci_is_up_to_date_otherwise_calculate_it(self):
        if self.__gci_up_to_date is False:
            self.__calculate_gci()
            self.__gci_up_to_date = True

    # = getter =========================================================================================================
    def get_gci(self):
        self.__check_if_gci_is_up_to_date_otherwise_calculate_it()
        return self.__GCI

    def get_asymptotic_gci(self):
        self.__check_if_gci_is_up_to_date_otherwise_calculate_it()
        return self.__asymptotic_gci

    def get_order(self):
        self.__check_if_gci_is_up_to_date_otherwise_calculate_it()
        return self.__order

    def get_dimension(self):
        return self.__dimension

    def get_volume(self):
        return self.__volume

    def get_cells(self):
        return self.__cells

    def get_solution(self):
        return self.__solution

    def get_safety_factor(self):
        return self.__safety_factor

    # = setter =========================================================================================================
    def set_dimension(self, dimension):
        assert 1 <= dimension <= 3
        self.__dimension = dimension
        self.__gci_up_to_date = False

    def set_volume(self, volume):
        assert len(volume) > 0
        self.__volume = volume
        self.__gci_up_to_date = False

    def set_cells(self, cell_count):
        assert len(cell_count) > 0
        self.__cells = cell_count
        self.__gci_up_to_date = False
        if len(self.__cells) == 2:
            self.__safety_factor = 3.0
        else:
            self.__safety_factor = 1.25

    def set_solution(self, solution):
        assert len(solution) > 0
        self.__solution = solution
        self.__gci_up_to_date = False

    def set_safety_factor(self, factor):
        assert factor > 0
        self.__safety_factor = factor
        self.__gci_up_to_date = False
