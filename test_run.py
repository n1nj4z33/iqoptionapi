from iqoption.api.api import IQOptionAPI
from iqoption.enums.actives import Active
from iqoption.enums.strategies import Strategy
from iqoption.enums.periods import Period
import logging

logging.basicConfig(level=logging.DEBUG)


def test_main():
    """Main test method."""
    ssid = "571c72efaf819381a5b445905eecda3c"

    api = IQOptionAPI(ssid)
    api.connect(Active.EURUSD,
                Strategy.candle_martin,
                Period.m1)

if __name__ == '__main__':
    test_main()

