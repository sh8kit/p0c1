from . import groups

from .subcommands import generate # we need to load this code for click register commands
from .stubs import apply

__all__ = ['groups', 'generate', 'apply']