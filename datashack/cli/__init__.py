# -*- coding: utf-8 -*-

"""Top-level package for CLI App"""

import click

from . import commands



@click.group()
def cli():
    pass


# Add commands
# cli.add_command(commands.groups.generate)
cli.add_command(commands.apply)