import click
from datashack.settings import click_pass_settings
from datashack.utils.io import file_write_lines, mkdir
import inquirer
from datashack.utils.console import console, error_console
from datashack.core.loaders import PyLoader
import yaml
import os
import requests

@click.command()
@click.argument('src_folder', default='./my_app/models')
@click.argument('output_folder', default='./local_docker/yamls')
@click_pass_settings
def apply(settings, src_folder: str, output_folder: str):
    """
    apply
    """
    console.log(f'Reading models from {src_folder}')
    loader = PyLoader(src_folder)

    mkdir(output_folder)

    for element_name, state in loader._state_elements.items():
        console.log(f'generating state for {element_name}')
        with open(os.path.join(output_folder, f'{element_name}.yaml'), 'w') as fp:
            yaml.dump(state, fp, allow_unicode=True)

    
    try:
        res = requests.get('http://localhost:5000')
    except:
        res = None

    if res:
        res_json = res.json()
        if res_json['code'] == 0:
            console.log('Datashack server updated, check Dashboard in http://localhost:8501')
        else:
            console.log('Datashack server had some problem')
            console.log('Stdout:')
            console.log(res_json['stdout'])
            console.log('Stderr:')
            error_console.log(res_json['stderr'])
    else:
        error_console.log('failed to update server')