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
        message = 'time parameter must be int, float, str or decimal.Decimal'
        raise TypeError(message)
