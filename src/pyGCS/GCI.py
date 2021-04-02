from math import pow, log, fabs


class GCI(object):
    """This class accepts grid parameters as inputs to compute the GCI"""

    # = constructor ====================================================================================================
    def __init__(self, **kwargs):
        self.__data = {}
        for key, value in kwargs.items():
            self.__data[key] = value

        self.__data['safety_factor'] = 1.25
        if len(self.__data['cells']) == 2:
            self.__data['safety_factor'] = 3.0

        if 'simulation_order' not in self.__data:
            self.__data['simulation_order'] = 2

        if 'dimension' not in self.__data:
            self.__data['dimension'] = 3

        # limit the order in the GCI calculation based on Oberkampf and Roy
        # See: https://doi.org/10.1017/CBO9780511760396.012, page 326, Table 8.1
        if 'oberkampf_correction' not in kwargs:
            self.__data['oberkampf_correction'] = False


        if 'oberkampf_correction' in key and 'simulation_order' not in key:
            raise Exception('Order of simulation required if Oberkampf and Roy corrections is to be applied!')

        self.__data['gci_up_to_date'] = False

    # = public API =====================================================================================================

    # = private API ====================================================================================================
    def __calculate_gci(self):
        assert len(self.__data['solution']) == 3
        self.__calculate_representative_grid_size()
        self.__sort_input_based_on_grid_size()
        self.__calculate_refinement_ratio()
        self.__calculate_relative_error()
        self.__calculate_order()
        self.__calculate_relative_normalised_error()
        self.__calculate_extrapolated_value()
        self.__apply_oberkamp_correction()
        self.__calculate_gci_for_each_grid()
        self.__calculate_asymptotic_grid_convergence()

    def __sort_input_based_on_grid_size(self):
        if 'volume' in self.__data:
            if type(self.__data['volume']) is list:
                assert len(self.__data['volume']) == len(self.__data['cells'])
                self.__data['cells'], self.__data['grid_size'], self.__data['volume'], self.__data['solution'] = zip(
                    *sorted(zip(self.__data['cells'], self.__data['grid_size'], self.__data['volume'],
                                self.__data['solution']), reverse=True))
            else:
                self.__data['cells'], self.__data['grid_size'], self.__data['solution'] = zip(
                    *sorted(zip(self.__data['cells'], self.__data['grid_size'], self.__data['solution']), reverse=True))
        else:
            self.__data['cells'], self.__data['grid_size'], self.__data['solution'] = zip(
                *sorted(zip(self.__data['cells'], self.__data['grid_size'], self.__data['solution']), reverse=True))

    def __calculate_representative_grid_size(self):
        if ('volume' in self.__data) and ('grid_size' not in self.__data):
            self.__data['grid_size'] = []
            for grid in range(0, len(self.__data['cells'])):
                if type(self.__data['volume']) is list:
                    assert len(self.__data['volume']) == len(self.__data['cells'])
                    volume = self.__data['volume'][grid]
                else:
                    volume = self.__data['volume']
                h = pow(volume / self.__data['cells'][grid], 1.0 / self.__data['dimension'])
                self.__data['grid_size'].append(h)

    def __calculate_refinement_ratio(self):
        self.__data['refinement_ratio'] = []
        assert len(self.__data['grid_size']) == len(self.__data['cells'])
        for grid in range(1, len(self.__data['grid_size'])):
            h1 = self.__data['grid_size'][grid - 1]
            h2 = self.__data['grid_size'][grid]
            ratio = h2 / h1
            assert ratio > 1
            self.__data['refinement_ratio'].append(ratio)
        assert len(self.__data['grid_size']) - 1 == len(self.__data['refinement_ratio'])

    def __calculate_relative_error(self):
        self.__data['relative_error'] = []
        assert len(self.__data['solution']) == len(self.__data['cells'])
        for grid in range(1, len(self.__data['solution'])):
            phi1 = self.__data['solution'][grid - 1]
            phi2 = self.__data['solution'][grid]
            self.__data['relative_error'].append(phi2 - phi1)
        assert len(self.__data['relative_error']) == len(self.__data['refinement_ratio'])

    def __calculate_order(self):
        self.__calculate_apparent_order()

    def __calculate_apparent_order(self):
        for grid in range(2, len(self.__data['cells'])):
            e21 = self.__data['relative_error'][grid - 2]
            e32 = self.__data['relative_error'][grid - 1]

            r21 = self.__data['refinement_ratio'][grid - 2]
            r32 = self.__data['refinement_ratio'][grid - 1]

            self.__data['apparent_order'] = self.__find_apparent_order_iteratively(e21, e32, r21, r32)

    def __find_apparent_order_iteratively(self, e21, e32, r21, r32):
        eps = 1
        iteration = 1
        max_iteration = 100
        norm = 1
        p = self.__data['simulation_order']
        while eps > 1e-6:
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
        assert len(self.__data['solution']) == len(self.__data['cells'])
        for grid in range(1, len(self.__data['solution'])):
            phi1 = self.__data['solution'][grid - 1]
            phi2 = self.__data['solution'][grid]
            self.__relative_normalised_error.append(fabs((phi1 - phi2) / phi1))
        assert len(self.__relative_normalised_error) == len(self.__data['refinement_ratio'])

    def __calculate_extrapolated_value(self):
        r21 = self.__data['refinement_ratio'][0]
        phi_1 = self.__data['solution'][0]
        phi_2 = self.__data['solution'][1]
        p = self.__data['apparent_order']
        self.__data['extrapolated_value'] = (pow(r21, p) * phi_1 - phi_2) / (pow(r21, p) - 1)

    def __apply_oberkamp_correction(self):
        if self.__data['oberkampf_correction']:
            apparent_order = self.__data['apparent_order']
            simulation_order = self.__data['simulation_order']

            order_indicator = fabs((apparent_order - simulation_order) / simulation_order)

            if order_indicator <= 0.1:
                self.__data['safety_factor'] = 1.25
            elif order_indicator > 0.1:
                self.__data['safety_factor'] = 3.0

            oberkampf_order = min(max(0.5, apparent_order), simulation_order)
            self.__data['apparent_order'] = oberkampf_order

    def __calculate_gci_for_each_grid(self):
        self.__data['gci'] = []
        for grid in range(1, len(self.__data['cells'])):
            ea21 = self.__relative_normalised_error[grid - 1]
            r21 = self.__data['refinement_ratio'][grid - 1]
            p = self.__data['apparent_order']
            gci = (self.__data['safety_factor'] * ea21) / (pow(r21, p) - 1.0)
            self.__data['gci'].append(gci)
        assert len(self.__data['gci']) == len(self.__data['cells']) - 1

    def __calculate_asymptotic_grid_convergence(self):
        self.__data['asymptotic_gci'] = []
        for grid in range(2, len(self.__data['cells'])):
            p = self.__data['apparent_order']
            gci21 = self.__data['gci'][grid - 2]
            gci32 = self.__data['gci'][grid - 1]
            r21 = self.__data['refinement_ratio'][grid - 2]
            asymptotic_gci = gci32 / (pow(r21, p) * gci21)
            self.__data['asymptotic_gci'] = asymptotic_gci

    def __check_if_gci_is_up_to_date_otherwise_calculate_it(self):
        if self.__data['gci_up_to_date'] is False:
            self.__calculate_gci()
            self.__data['gci_up_to_date'] = True

    # = getter =========================================================================================================
    def get_number_of_cells_for_specified_gci_of(self, desired_gci):
        self.__check_if_gci_is_up_to_date_otherwise_calculate_it()
        p = self.__data['apparent_order']
        gci = self.__data['gci'][0]
        cells = self.__data['cells'][0]
        r = pow((gci / desired_gci), 1.0 / p)
        return r * cells

    def get(self, key):
        self.__check_if_gci_is_up_to_date_otherwise_calculate_it()
        return self.__data[key]

    # = setter =========================================================================================================
    def set(self, key, value):
        self.__data[key] = value
        self.__data['gci_up_to_date'] = False
