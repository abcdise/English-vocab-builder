import jinja2
from Exercise import Exercise
from pathlib import Path

# Set up jinja environment

latex_jinja_env = jinja2.Environment(
    block_start_string = r'\BLOCK{',
    block_end_string = '}',
    variable_start_string = r'\VAR{',
    variable_end_string = '}',
    comment_start_string = r'\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader('../src/resources/Templates')
)

def int_to_roman(num):
        """
        Converts an integer to a Roman numeral.

        Args:
            num (int): The integer to be converted.

        Returns:
            str: The Roman numeral representation of the integer.
        """
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syms = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        roman_numeral = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_numeral += syms[i]
                num -= val[i]
            i += 1
        return roman_numeral

class ExerciseWriter():
    def __init__(self, exercise: Exercise, template_path:str, output_folder:str):
        self.exercise = exercise
        self.template_file = Path(template_path)
        self.output_folder = Path(output_folder)

    
    def render_template(self, set_index:int):
        output_file_path = self.output_folder / f'output_{set_index}.tex'
        output_dict = self.exercise.exercise_dict
        self.__render_template(output_file_path=output_file_path, 
                               part_name = int_to_roman(set_index),
                               **output_dict
                               )
        
    
    def __render_template(self, output_file_path:Path, **kwargs):
        '''
        Create the rendered template and export it.
        '''
        template = latex_jinja_env.get_template(str(self.template_file))
        rendered_template = template.render(**kwargs)
        with open(output_file_path, 'w') as f:
            f.write(rendered_template)
