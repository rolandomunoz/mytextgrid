"""Create and manipulate point tiers objects"""
import decimal
from mytextgrid._eval import EvalTimeRange
decimal.getcontext().prec = 16

class PointTier:
    """Represent a tier that contains Point objects."""

    def __init__(self, name = '', xmin = 0, xmax = 1):
        self.name = name
        self.class_ = 'TextTier'
        self.xmin = decimal.Decimal(str(xmin))
        self.xmax = decimal.Decimal(str(xmax))
        self.tier = []
        self.eval_time_range = EvalTimeRange(self.xmin, self.xmax, level = 1)

    def __len__(self):
        return len(self.tier)

    def __iter__(self):
        return iter(self.tier)

    def __getitem__(self, key):
        return self.tier[key]

    def insert_point(self, time, text = ''):
        """Insert a Point object inside PointTier object."""
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))

        if self.is_point_at_time(time):
            raise ValueError(f'Cannot insert a point at {time}')

        point = Point(time, text)
        self.tier.append(point)
        self.tier.sort(key=lambda x:x.time)

    def insert_points(self, *times):
        """Insert various empty Point objects into a PointTier object."""
        for time in times:
            self.insert_point(time)

    def remove_point(self, point_position):
        """Remove a Point object."""
        self.tier.pop[point_position]

    def set_point_text(self, point_position, text):
        """Set the text content of an existing Point object."""
        self.tier[point_position].text = text

    def get_time_of_point(self, point_position):
        """Get the time of an object by its ordinal position."""
        return self.tier[point_position].time

    def get_label_of_point(self, point_position):
        """Get the text content of a Point object."""
        return self.tier[point_position].text

    def is_point_at_time(self, time):
        """Check if a Point exists in the given time."""
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))
        
        # Check if out of range
        self.eval_time_range.check_time(time)
        for point in self:
            if point.time == time:
                return True
        return False


class Point:
    """Represent a Point object which is the minimal unit of a PointTier object"""

    def __init__(self, time, text = ""):
        self.class_ = 'Point'
        self.time = decimal.Decimal(str(time))
        self.text = text
