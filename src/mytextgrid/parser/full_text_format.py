import re
import decimal
import os
import chardet
decimal.getcontext().prec = 16
from ..textgrid import TextGrid as TextGridBuilder

def read_from_file(path):
  """Read a TextGrid file and return a TextGrid object"""
  parser = Parser()
  return parser.parse_full_text(path)

class Parser:
  """
  This class implements methods for parsing TextGrid in full text format.
  """
  def parse_full_text(self, path):
    """Parse a TextGrid file and return a TextGrid object"""

    # Open file
    encoding = self._detect_encoding(path)
    self._file = open(path, 'r', encoding=encoding)    

    ## File header
    file_type = self._get_next_value()
    if not file_type == 'ooTextFile':
      raise OSError()
      
    object_class = self._get_next_value()
    if not object_class == 'TextGrid':
      raise OSError('The file {} is not a TextGrid'.format(path))
    
    ## TextGrid header
    xmin = self._get_next_value()
    xmax = self._get_next_value()
    tier_exists = self._get_next_value()
    size = self._get_next_value()
    basename = os.path.splitext(os.path.basename(path))[0]

    # Create an instance TextGridFormat object
    textgrid = TextGridFormat(basename, xmin, xmax)
    
    # Get tiers and added to the TextGridFormat object
    self.set_TextGrid_tiers(textgrid)
    
    self._file.close()
    return self._build_textgrid(textgrid)
    
  def _build_textgrid(self, textgrid_obj):   
    textgrid_ = TextGridBuilder(textgrid_obj.name, textgrid_obj.xmin, textgrid_obj.xmax)
    
    for tier_position, tier in enumerate(textgrid_obj):
      if isinstance(tier, IntervalTier):
        textgrid_.insert_interval_tier(tier.name, tier_position)
        tier_ = textgrid_[tier_position]
        for interval_position, interval in enumerate(tier):
          try:
            tier_.insert_boundaries(interval.xmax)
            tier_.set_text(interval_position, interval.text)
          except:
            pass
      else:
        textgrid_.insert_point_tier(tier.name, tier_position)
        tier_ = textgrid_[tier_position]
        for point in tier:
          try:
            tier_.insert_point(point.time, point.text)
          except:
            pass
    return textgrid_
   
  def set_TextGrid_tiers(self, textgrid_obj):
    while True:
      tier_class = self._get_next_value()
      if tier_class is None:
        return None
      if tier_class == 'IntervalTier':
        self.set_TextGrid_interval_tier(textgrid_obj)
      elif tier_class == 'TextTier':
        self.set_TextGrid_point_tier(textgrid_obj)
    
  def set_TextGrid_interval_tier(self, textgrid_obj):
    tier_name = self._get_next_value()
    xmin = decimal.Decimal(str(self._get_next_value()))
    xmax = decimal.Decimal(str(self._get_next_value()))
    size = int(self._get_next_value())

    interval_tier = IntervalTier(tier_name, xmin, xmax)
    for index in range(size):
      xmin = self._get_next_value()
      xmax = self._get_next_value()
      text = self._get_next_value()
      interval_item = IntervalItem(xmin, xmax, text)
      interval_tier.append(interval_item)
    textgrid_obj.append(interval_tier)

  def set_TextGrid_point_tier(self, textgrid_obj):
    tier_name = self._get_next_value()
    xmin = decimal.Decimal(str(self._get_next_value()))
    xmax = decimal.Decimal(str(self._get_next_value()))
    size = int(self._get_next_value())
    point_tier = TextTier(tier_name, xmin, xmax)

    for index in range(size):
      time = self._get_next_value()
      text = self._get_next_value()
      point_item = PointItem(time, text)
      point_tier.append(point_item)
    textgrid_obj.append(point_tier)

  def _get_next_value(self):
    while True:
      raw_line = self._file.readline()
      if raw_line == '':
        return None
      if raw_line == '\n':
        continue
      if '[' in raw_line:
        continue
      if raw_line.startswith('tiers?'):
        raw_line = 'tier_status = ' + raw_line
      line = raw_line.rstrip().lstrip()
      line = line.split('= ', 1)[1]
      if line.startswith('"') and line.endswith('"'):
        line = line[1:-1]
      return line

  def _detect_encoding(self, path):
    with open(path, 'rb') as f:
      rawdata = f.read()
      result = chardet.detect(rawdata)
      return result.get('encoding') 

class Container:
  """
  This is a base class for TextGrids and tiers.
  """
  def __init__(self, name, xmin, xmax, items = None):
    self.name = name
    self.xmin = xmin
    self.xmax = xmax
    if items is None:
      items = list()

    self.size = len(items)
    self.items = items

  def __iter__(self):
    return iter(self.items)
    
  def set_header(self, name, xmin, xmax):
    self.name = name
    self.xmin = xmin
    self.xmax = xmax

  def append(self, item_obj):
    self.items.append(item_obj)
    self.size = len(self.items)

class TextGridFormat(Container):
  """
  This is a container for a TextGrid. It contains interval or point tiers.
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.class_ = 'TextGrid'

class IntervalTier(Container):
  """
  This is a container for an Interval tier. It contains intervals.
  """  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.class_ = 'Interval tier'
    
class TextTier(Container):
  """
  This is a container for a Point tier. It contains points.
  """  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.class_ = 'Point tier'
   
class PointItem:
  """
  This is a container for a Point.
  """
  def __init__(self, time, text = ''):
    self.time = time
    self.text = text

class IntervalItem:
  """
  This is a container for an Interval.
  """
  def __init__(self, xmin, xmax, text = ''):
    self.xmin = xmin
    self.xmax = xmax
    self.text = text

