import click
from ..groups import generate
from datashack.settings import click_pass_settings
from datashack.utils.io import file_write_lines
import inquirer
from datashack.utils.console import console, error_console
from datashack.core.loaders import PyLoader
import yaml
import os

# @generate.command()
# @click.argument('src_folder', default='./my_app/models')
# @click.argument('output_folder', default='./local_docker/yamls')
# @click_pass_settings
# def state(settings, src_folder: str, output_folder: str):
#     """
#     generate state
#     """
#     loader = PyLoader(src_folder)
#     print(loader._state_elements)
#     for element_name, state in loader._state_elements.items():
#         with open(os.path.join(output_folder, f'{element_name}.yaml'), 'w') as fp:
#             yaml.dump(state, fp, allow_unicode=True)