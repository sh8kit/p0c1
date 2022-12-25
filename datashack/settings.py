import os
import click
from datashack.consts import Consts
from datashack.utils.io import YamlIO, mkdir, touch
from datashack.utils.sys import get_os
from datashack.utils.console import console, error_console

class Settings:
    def __init__(self, home=None, terminal=None):
        self.home = os.path.abspath(home or Consts.HOME)
        self.terminal = terminal or Consts.DEFAULT_TERMINAL
        mkdir(self.home)

        self.os = get_os()
        
# from https://click.palletsprojects.com/en/8.1.x/complex/
click_pass_settings = click.make_pass_decorator(Settings, ensure=True)
