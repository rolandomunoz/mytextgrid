import decimal
decimal.getcontext().prec = 16

def obj_to_decimal(time, message = None):
    """
    Convert a number to :class:`decimal.Decimal`.

    Parameters
    ----------
    time : int, float str or decimal.Decimal
        A number in seconds to be converted.
    message : str
        A message to show if raise an exception.

    Returns
    -------
    :class:`decimal.Decimal`
        A :class:`decimal.Decimal` object representing the time in seconds.
    """
    if isinstance(time, decimal.Decimal):
        return time
    elif isinstance(time, (int, float)):
        return decimal.Decimal(str(time))
    elif isinstance(time, str):
        return decimal.Decimal(time)
    else:
        if message is None:
            message = 'time parameter must be int, float, str or decimal.Decimal'
        raise TypeError(message)

class EvalTimeRange:
    """
    A class for checking point times between a specified range.
    """

    def __init__(self, tmin, tmax, level_name = ''):
        if not isinstance(tmin, decimal.Decimal):
            raise TypeError('tmin must be an decimal.Decimal object')
        if not isinstance(tmax, decimal.Decimal):
            raise TypeError('tmax must be an decimal.Decimal object')

        self._tmin = tmin
        self._tmax = tmax
        self._level_name = level_name

    @property
    def tmin(self):
        return self._tmix

    @tmin.setter
    def tmin(self, value):
        if not isinstance(value, decimal.Decimal):
            raise TypeError('tmin must be an decimal.Decimal object')
        if value > self._tmax:
            raise ValueError(f'tmix must be a number lesser than tmax')
        self._tmin = value

    @property
    def tmax(self):
        return self._tmax

    @tmax.setter
    def tmax(self, value):
        if not isinstance(value, decimal.Decimal):
            raise TypeError('tmax must be an decimal.Decimal object')
        if value < self._tmin:
            raise ValueError(f'tmax must be a number greater than tmin')
        self._tmax = value

    def update_time_range(self, tmin, tmax):
        """
        Update the time range.
        """
        if not isinstance(tmin, decimal.Decimal):
            raise TypeError('tmin must be an decimal.Decimal object')
        if not isinstance(tmax, decimal.Decimal):
            raise TypeError('tmax must be an decimal.Decimal object')
        self._tmin = tmin
        self._tmax = tmax

    def is_time_between_range(self, time):
        check_time(self, time)

    def check_time(self, time):
        """
        Raise a ValueError if the time is not between the object range.
        """
        if not isinstance(time, decimal.Decimal):
            raise TypeError('time must be a decimal.Decimal object.')

        if self.tmin > time > self.tmax:
            raise ValueError(f'The time {time} seconds is out of range {self.level_name}')
        if self.tmin == time:
            raise ValueError(f'The time {time} seconds is at the left edge {self.level_name}.')
        if self.tmax == time:
            raise ValueError(f'The time {time} seconds is at the right edge {self.level_name}.')
