"""Create and manipulate `Interval` and `IntervalTier` objects."""
import decimal
from mytextgrid._eval import EvalTimeRange
decimal.getcontext().prec = 16

class IntervalTier:
    """A class representation for a tier."""

    def __init__(self, name = '', xmin = 0, xmax = 1):
        self.name = name
        self.class_ = 'IntervalTier'
        self.xmin = decimal.Decimal(str(xmin))
        self.xmax = decimal.Decimal(str(xmax))
        self.tier = [Interval(self.xmin, self.xmax)]
        self.eval_time_range = EvalTimeRange(self.xmin, self.xmax, level = 1)

    def __iter__(self):
        return iter(self.tier)

    def __len__(self):
        return len(self.tier)

    def __getitem__(self, key):
        return self.tier[key]

    def insert_boundaries(self, *times):
        """Insert one or more tier boundaries."""
        for time in times:
            self.insert_boundary(time)

    def insert_boundary(self, time):
        """Insert a tier boundary and split intervals."""
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))

        # Check if out of range
        self.eval_time_range.check_time(time)

        interval_position = self.get_interval_at_time(time)
        interval_left = self.tier[interval_position]
        if time == interval_left.xmin:
            error_msg = (f'Cannot add a boundary at {time} seconds,'
            'because there is already a boundary there. Boundary not inserted.')
            raise ValueError(error_msg)

        # Split interval
        interval_right = Interval(time, interval_left.xmax)
        interval_left.xmax= time

        # Insert interval
        self.tier.insert(interval_position+1, interval_right)

    def remove_boundary(self, time):
        """Remove a boundary given a time value."""
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))

        self.eval_time_range.check_time(time)

        interval_position = self.get_interval_at_time(time)
        interval_left = self.tier[interval_position]
        if not time == interval_left.xmin:
            error_msg = f'There is no boundary at {time} seconds'
            raise ValueError(error_msg)

        interval_left = self.tier[interval_position-1]
        interval_right = self.tier[interval_position]

        interval_left.xmax = interval_right.xmax
        interval_left.text += interval_right.text

        # Remove right interval
        self.tier.pop(interval_position)

    def move_boundary(self, src_time, dst_time):
        """Move boundary with src_time to dst_time."""
        # Normalize numbers
        if not isinstance(src_time, decimal.Decimal):
            src_time = decimal.Decimal(str(src_time))

        if not isinstance(dst_time, decimal.Decimal):
            dst_time = decimal.Decimal(str(dst_time))

        # Check
        self.eval_time_range.check_time(src_time)
        self.eval_time_range.check_time(dst_time)

        position = self.get_interval_at_time(src_time)

        interval_left = self.tier[position-1]
        interval_right = self.tier[position]

        if not interval_right.xmin == src_time:
            raise ValueError(f'There is no boundary at {src_time} seconds')

        if not dst_time > interval_left.xmin or not dst_time < interval_right.xmax:
            raise ValueError(f'Cannot move boundary to {dst_time}')

        # Do
        interval_left.xmax = dst_time
        interval_right.xmin = dst_time

    def set_text(self, interval_position, *text_items):
        """Set the text of a given interval. When more than one text
         item is specified, each item is placed next to each other."""
        for position, text in enumerate(text_items, start = interval_position):
            self.tier[position].text = text

    def get_interval_at_time(self, time):
        """Return the interval position given a time value."""
        self.eval_time_range.check_time(time)
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))
        for index_, interval in enumerate(self):
            if interval.is_in_range(time):
                return index_
        return None

class Interval:
    """A class representation for an interval object."""

    def __init__(self, xmin, xmax, text = ""):
        self.class_ = 'Interval'
        self.xmin = decimal.Decimal(str(xmin))
        self.xmax = decimal.Decimal(str(xmax))
        self.text = text

    def is_in_range(self, time):
        """"Return True if the given time is between the interval boundaries.
         That is: xmin >= x < xmax."""
        time = decimal.Decimal(str(time))
        if self.xmin <= time < self.xmax:
            return True
        return False

    def is_left_boundary(self, time):
        """Return True if the time value is equal to the left boundary time"""
        time = decimal.Decimal(str(time))
        if self.xmin == time:
            return True
        return False

    def is_right_boundary(self, time):
        """Return True if the time value is equal to the right boundary time"""
        time = decimal.Decimal(str(time))
        if self.xmax == time:
            return True
        return False
