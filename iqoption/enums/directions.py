from enum import Enum


class Direction(Enum):
    call = 'call'
    put = 'put'

    @property
    def flip_direction(self):
        if self.call:
            return self.put
        else:
            return self.call
