from abc import ABC, abstractmethod
from datashack.utils.io import exists

class Loader(ABC):

    def __init__(self, src: str):
        self._state_elements = None

        if exists(src):
            self.from_folder(src)
        else:
            raise RuntimeError(f"unable to identify loader source {src}")
        
        if not self._state_elements:
            raise RuntimeError("empty state")



    @abstractmethod
    def from_folder(self, src: str):
        raise NotImplementedError()