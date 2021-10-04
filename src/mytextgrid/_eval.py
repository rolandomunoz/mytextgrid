import decimal
class EvalTextGrid:
    pass

class EvalTimeRange:
    """A class for checking point times between a specified range."""

    def __init__(self, tmin, tmax, level = 0):
        if not isinstance(tmin, decimal.Decimal):
            raise TypeError('tmin must be an decimal.Decimal object')
        if not isinstance(tmax, decimal.Decimal):
            raise TypeError('tmax must be an decimal.Decimal object')
        self.tmin = tmin
        self.tmax = tmax
        self.set_level(level)

    def set_level(self, level = 0):
        """Set the level: 0:TextGrid, 1:tier, 2:interval, 3:point"""
        level_dict = {0:'TextGrid', 1:'tier', 2:'interval', 3:'point'}
        self.level = f'of the {level_dict.get(level)}'

    def check_time(self, time):
        """Raise a ValueError if the time is not between the object range."""
        if not isinstance(time, decimal.Decimal):
            raise TypeError('time must be a decimal.Decimal object.')

        if self.tmin > time > self.tmax:
            raise ValueError(f'The time {time} seconds is out of range {self.level}')
        if self.tmin == time:
            raise ValueError(f'The time {time} seconds is at the left edge {self.level}.')
        if self.tmax == time:
            raise ValueError(f'The time {time} seconds is at the right edge {self.level}.')
