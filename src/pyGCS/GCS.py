import os
from .GCI import GCI


class GCS(object):
    """This class delegates the GCI computation and formats the output in a user friendly way"""

    def __init__(self, **kwargs):
        # we can only perform a GCI study for 3 grids. If we have more, we need to perform more. For 4 grids, we need
        # 2 gci studies, for 5 grids 3 gci studies, and so on.
        assert 'solution' in kwargs
        self.number_of_gci_studies_required = len(kwargs['solution']) - 2

        # setup data structure
        self.__data = {}
        self.__data['gci'] = list(range(self.number_of_gci_studies_required))
        self.__data['cells'] = list(range(self.number_of_gci_studies_required))
        self.__data['solution'] = list(range(self.number_of_gci_studies_required))
        self.__data['refinement_ratio'] = list(range(self.number_of_gci_studies_required))
        self.__data['asymptotic_gci'] = list(range(self.number_of_gci_studies_required))
        self.__data['apparent_order'] = list(range(self.number_of_gci_studies_required))
        self.__data['extrapolated_value'] = list(range(self.number_of_gci_studies_required))

        self.__gci = []
        kwargs = self.__sort(**kwargs)
        for study in range(0, self.number_of_gci_studies_required):
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
            self.__data['cells'][study] = gci_study.get('cells')
            self.__data['solution'][study] = gci_study.get('solution')
            self.__data['refinement_ratio'][study] = gci_study.get('refinement_ratio')
            self.__data['asymptotic_gci'][study] = gci_study.get('asymptotic_gci')
            self.__data['apparent_order'][study] = gci_study.get('apparent_order')
            self.__data['extrapolated_value'][study] = gci_study.get('extrapolated_value')

    def __sort(self, **kwargs):
        if 'volume' in kwargs:
            if type(kwargs['volume']) is list:
                assert len(kwargs['volume']) == len(kwargs['cells'])
                kwargs['cells'], kwargs['volume'], kwargs['solution'] = zip(*sorted(zip(kwargs['cells'],
                                                                                        kwargs['volume'],
                                                                                        kwargs['solution']),
                                                                                    reverse=True))
            else:
                kwargs['cells'], kwargs['solution'] = zip(*sorted(zip(kwargs['cells'], kwargs['solution']),
                                                                  reverse=True))
        else:
            kwargs['cells'], kwargs['solution'] = zip(*sorted(zip(kwargs['cells'], kwargs['solution']), reverse=True))
        return kwargs

    def get(self, key):
        return self.__data[key]

    def print_table(self, output_type='markdown', output_path=''):
        if output_type == 'markdown':
            self.__markdown_table(output_path)
        elif output_type == 'latex':
            self.__latex_table(output_path)
        elif output_type == 'word':
            self.__word_table(output_path)

    def __markdown_table(self, output_path):
        table = f'''
Generated using pyGCS (Grid Convergence Study)
- https://github.com/tomrobin-teschner/pyGCS
- https://pypi.org/project/pygcs/

Table 1: Grid convergence study over {self.number_of_gci_studies_required + 2} grids. phi represents the {{INSERT MEANING OF PHI HERE}} and phi_extrapolated its extrapolated value. N_cells is the number of grid elements, r the refinement ration between two successive grids. GCI is the grid convergence index in percent and its asymptotic value is provided by GCI_asymptotic, where a value close to unity indicates a grid independent solution. The order achieved in the simulation is given by p.

|        |  phi      |   N_cells   |  r  |  GCI  | GCI_asymptotic |  p   | phi_extrapolated |
|--------|:---------:|:-----------:|:---:|:-----:|:--------------:|:----:|:----------------:|'''
        for study in range(0, self.number_of_gci_studies_required):
            table += f'''
|        |           |             |     |       |                |      |                  |
| Grid {study+1} | {self.__data['solution'][study][0]:.3e} | {self.__data['cells'][study][0]:11d} | {self.__data['refinement_ratio'][study][0]:.1f} | {100 * self.__data['gci'][study][0]:.2f}% |                |      |                  |
| Grid {study+2} | {self.__data['solution'][study][1]:.3e} | {self.__data['cells'][study][1]:11d} | {self.__data['refinement_ratio'][study][1]:.1f} | {100 * self.__data['gci'][study][1]:.2f}% |      {self.__data['asymptotic_gci'][study]:.3f}     | {self.__data['apparent_order'][study]:.2f} |     {self.__data['extrapolated_value'][study]:.2e}     |
| Grid {study+3} | {self.__data['solution'][study][2]:.3e} | {self.__data['cells'][study][2]:11d} | -   | -     |                |      |                  |'''
        table += f'''
|        |           |             |     |       |                |      |                  |'''
        file = open(os.path.join(output_path, 'table.md'), 'w')
        file.write(table)
        file.close()

    def __latex_table(self, output_path):

        table = f'''
% You have to add the following packages to your preamble to make this table work in your document
% \\usepackage{{booktabs}}
% \\usepackage{{multirow}}
\\begin{{table}}[tbp]
\\caption{{Grid convergence study over {self.number_of_gci_studies_required + 2} grids. $ \\phi $ represents the \\textbf{{INSERT MEANING OF PHI HERE}} and $ \\phi_{{extrapolated}} $ its extrapolated value. $ N_{{cells}} $ is the number of grid elements, $ r $ the refinement ration between two successive grids. $ GCI $ is the grid convergence index in percent and its asymptotic value is provided by $ GCI_{{asymptotic}} $, where a value close to unity indicates a grid independent solution. The order achieved in the simulation is given by $ p $.}}
\\label{{tab:gci_study}}
\\begin{{tabular}}{{@{{}}lccccccc@{{}}}}
\\toprule
& $ \\phi $ & $ N_{{cells}} $ & $ r $ & $ GCI $ & $ GCI_{{asymptotic}} $ & $ p $ & $ \\phi_{{extrapolated}} $ \\\\ \\midrule
'''
        for study in range(0, self.number_of_gci_studies_required):

            table += f'''
Grid {study+1} & {self.__data['solution'][study][0]:.3e} & {self.__data['cells'][study][0]} & {self.__data['refinement_ratio'][study][0]:.1f} & {100 * self.__data['gci'][study][0]:.2f}\\%   & \\multirow{{3}}{{*}}{{ {self.__data['asymptotic_gci'][study]:.3f} }} & \\multirow{{3}}{{*}}{{ {self.__data['apparent_order'][study]:.2f} }} & \\multirow{{3}}{{*}}{{ {self.__data['extrapolated_value'][study]:.2e} }} \\\\
Grid {study+2} & {self.__data['solution'][study][1]:.2e} & {self.__data['cells'][study][1]}  & {self.__data['refinement_ratio'][study][1]:.1f} & {100 * self.__data['gci'][study][1]:.2f}\\% &                       &                      &                       \\\\
'''
            if study == self.number_of_gci_studies_required - 1:
                table += f'''Grid {study+3} & {self.__data['solution'][study][2]:.2e} & {self.__data['cells'][study][2]}  & -   & -     &                       &                      &                       \\\\ \\bottomrule
                '''
            else:
                table += f'''Grid {study+3} & {self.__data['solution'][study][2]:.2e} & {self.__data['cells'][study][2]}  & -   & -     &                       &                      &                       \\\\ \\cmidrule(r){{1-8}}
                '''

        table += f'''
\\end{{tabular}}
\\end{{table}}
% Generated using pyGCS (Grid Convergence Study)
% - https://github.com/tomrobin-teschner/pyGCS
% - https://pypi.org/project/pygcs/
'''
        file = open(os.path.join(output_path, 'table.tex'), 'w')
        file.write(table)
        file.close()

    def __word_table(self, output_path):
        table = f'''
Generated using pyGCS (Grid Convergence Study)
- https://github.com/tomrobin-teschner/pyGCS
- https://pypi.org/project/pygcs/

Generate an empty table in word with dimensions 8 (columns) x {1 + 4 * self.number_of_gci_studies_required} (rows), select all cells and copy the content after the caption below into the table

Table 1: Grid convergence study over {self.number_of_gci_studies_required + 2} grids. phi represents the {{INSERT MEANING OF PHI HERE}} and phi_extrapolated its extrapolated value. N_cells is the number of grid elements, r the refinement ration between two successive grids. GCI is the grid convergence index in percent and its asymptotic value is provided by GCI_asymptotic, where a value close to unity indicates a grid independent solution. The order achieved in the simulation is given by p.

\tphi\tN_cells\tr\tGCI\tGCI_asymptotic\tp\tphi_extrapolated'''
        for study in range(0, self.number_of_gci_studies_required):
            table += f'''

Grid {study+1}\t{self.__data['solution'][study][0]:.3e}\t{self.__data['cells'][study][0]:11d}\t{self.__data['refinement_ratio'][study][0]:.1f}\t{100 * self.__data['gci'][study][0]:.2f}%\t\t\t
Grid {study+2}\t{self.__data['solution'][study][1]:.3e}\t{self.__data['cells'][study][1]:11d}\t{self.__data['refinement_ratio'][study][1]:.1f}\t{100 * self.__data['gci'][study][1]:.2f}% \t{self.__data['asymptotic_gci'][study]:.3f}\t{self.__data['apparent_order'][study]:.2f}\t{self.__data['extrapolated_value'][study]:.2e}
Grid {study+3}\t{self.__data['solution'][study][2]:.3e}\t{self.__data['cells'][study][2]:11d}\t\t\t\t\t'''
        file = open(os.path.join(output_path, 'table.txt'), 'w')
        file.write(table)
        file.close()
