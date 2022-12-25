from .base import Loader

from datashack.utils.py import dynamic_load_classes
from ...entities.tables import StateElement


class PyLoader(Loader):
    
    def from_folder(self, src: str):
        members = dynamic_load_classes(src)
        self._state_elements = {
            obj.state_elemt_name: obj.generate_state()
            for obj in members
            if isinstance(obj, StateElement)
        }
