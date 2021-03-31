from .GCI import GCI


class GCS(object):
    """This class delegates the GCI computation and formats the output in a user friendly way"""
    def __init__(self, **kwargs):
        # we can only perform a GCI study for 3 grids. If we have more, we need to perform more. For 4 grids, we need
        # 2 gci studies, for 5 grids 3 gci studies, and so on.
        assert 'solution' in kwargs
        number_of_gci_studies_required = len(kwargs['solution']) - 2

        # setup data structure
        self.__data = {}
        self.__data['gci'] = list(range(number_of_gci_studies_required))
        self.__data['asymptotic_gci'] = list(range(number_of_gci_studies_required))
        self.__data['apparent_order'] = list(range(number_of_gci_studies_required))
        self.__data['extrapolated_value'] = list(range(number_of_gci_studies_required))

        self.__gci = []
        for study in range(0, number_of_gci_studies_required):
            # create new input arguments
            new_input = {}
            for key, value in kwargs.items():
                if (key == 'solution') or (key == 'cells'):
                    new_input[key] = value[study:study+3]
                elif key == 'volume':
                    if type(key) is list:
                        new_input[key] = value[study:study+3]
                    else:
                        new_input[key] = value
                else:
                    new_input[key] = value

            gci_study = GCI(**new_input)

            # gather data
            self.__data['gci'][study] = gci_study.get('gci')
            self.__data['asymptotic_gci'][study] = gci_study.get('asymptotic_gci')
            self.__data['apparent_order'][study] = gci_study.get('apparent_order')
            self.__data['extrapolated_value'][study] = gci_study.get('extrapolated_value')

    def get(self, key):
        return self.__data[key]

