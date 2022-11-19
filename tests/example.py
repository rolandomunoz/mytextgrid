import sys
from pathlib import Path
mytextgrid_path = str(Path(__file__).parent.parent.joinpath('src'))
sys.path.insert(0, mytextgrid_path)
import mytextgrid

# Reading a TextGrid
textgrid_path = Path(__file__).parent / 'files/Mary_John_bell-1.TextGrid'

with open(textgrid_path, encoding = 'utf-8') as textfile:
    tg = mytextgrid.read_from_stream(textfile)

with open(textgrid_path, encoding = 'utf-8') as textfile:
    text = textfile.read()
    tg = mytextgrid.read_from_stream(text)

    print(tg.describe())

tg = mytextgrid.read_from_file(textgrid_path)

# Describe a TextGrid
tg.describe()

# Manipulating a TextGrid
tone_tier = tg.insert_tier("tone", False)
segment_tier = tg.insert_tier("segment")
word_tier = tg.insert_tier("word")
phrase_tier = tg.insert_tier("phrase")

# Point tier: Inserting points
tone_tier.insert_point(0.66, "H")
tone_tier.insert_point(0.9, "L")

# Interval tier: Inserting boundaries
segment_tier.insert_boundaries(0.23, 0.30, 0.42, 0.62, 0.70, 0.82, 0.98)
word_tier.insert_boundaries(0.23, 0.42, 0.98)
phrase_tier.insert_boundaries(0.23, 0.98)

# Interval tier: Populate intervals with text
segment_tier.set_text_at_index(1, 'e', 'l', 'p', 'e', 'rr', 'o')
word_tier.set_text_at_index(1, 'el')
word_tier.set_text_at_index(2, 'perro')
phrase_tier.set_text_at_index(1, 'el perro')

# Remove a tier
tg.remove_tier(0)
tg.describe()

# Traversing a TextGrid
# TextGrid info
print(tg.xmin)
print(tg.xmax)

# Iterate through a TextGrid
for tier in tg:
    print(tier.name)
   # Iterate through tiers
    if tier.is_interval():
        for interval in tier:
            # For interval tiers
            # Print Interval attributes
            print(interval.xmin)
            print(interval.xmax)
            print(interval.text)
    else:
        # For point tiers
        for point in tier:
            # Print Point attributes
            print(point.time)
            print(point.text)

# Write TextGrid to a text file
tg.write('example1-long.TextGrid')
tg.write('example1-short.TextGrid', True) # Write the TextGrid a short format TextGrid

# Write to a CSV file
#tg.to_csv(csv_path)

# Write to a JSON file
tg.write_as_json('example1.json')

## Create an empty TextGrid
new_tg = mytextgrid.create_textgrid(xmin = 0, xmax = 1)
