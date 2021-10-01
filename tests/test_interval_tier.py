import unittest
import MyTextGrid.interval_tier
import decimal
decimal.getcontext().prec = 16

class TestIntervalTier(unittest.TestCase):

  def test_init_tier(self):
    tier = MyTextGrid.interval_tier.IntervalTier('rolando', 0, 1)
    self.assertEqual(tier.name, 'rolando')
    self.assertEqual(tier.xmin, 0)
    self.assertEqual(tier.xmax, 1)
    self.assertEqual(len(tier), 1)

  def test_add_boundary(self):
    tier = MyTextGrid.interval_tier.IntervalTier('rolando', 0, 1)
    
    times = [decimal.Decimal(str(0.45)), decimal.Decimal(str(0.3)), decimal.Decimal(str(0.5324338183183182)), decimal.Decimal(str(0.931313))]

    # Add boundary
    for time in times:
      tier.add_boundary(time)

    # Test general attributes after adding boundaries
    self.assertEqual(tier.name, 'rolando')
    self.assertEqual(tier.xmin, 0)
    self.assertEqual(tier.xmax, 1)
    self.assertEqual(len(tier), 5) # number of intervals

    # Check if boundaries exist
    times.append(tier.xmax)
    new_times=times.copy()
    new_times.sort()
    for index, interval in enumerate(tier):
      self.assertEqual(interval.xmax, new_times[index])
    
    # Check if NameError on an existing boundary
    with self.assertRaises(NameError):
      for time in times:
        tier.add_boundary(time)
        
      # Add boundary at start and end
      tier.add_boundary(0)
      tier.add_boundary(1)
      
      # Add boundaries outside the range
      tier.add_boundary(-0.0000001)
      tier.add_boundary(2)
    
if __name__ == '__main__':
  unittest.main()

#position = tier.get_interval_at_time(0.5)
#tier.set_interval_text(position, 'Huaiwa')
#position = tier.get_interval_at_time(0.1)
#tier.set_interval_text(position, 'Aarone')
#position = tier.get_interval_at_time(0.95)
#tier.set_interval_text(position, 'Erick')

#tier.move_boundary(0.3, 0.34)
#print(tier)