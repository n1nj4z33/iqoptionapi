from base import BaseStrategy
from iqoption.enums.directions import Direction


class SimpleMartinStrategy(BaseStrategy):
    def __call__(self, *args, **kwargs):
        self.name = 'Simple martingale strategy'
        self.won = False
        self.direction = Direction.call
        self.lot = 1

    def martin_rule(self):
        if not won:
            self.lot *= 2.5
