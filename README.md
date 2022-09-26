# Python package: mytextgrid

This is a python package to work with [Praat](https://www.fon.hum.uva.nl/praat/) annotation files. You can `create`, `read`, `write` and `query` TextGrids.

The following tutorial will walk you through the basics. For more information, visit the [documentation website](https://mytextgrid.readthedocs.io/en/latest/index.html)

## Getting started

### 1. Installation

You can get the lastest release of this package using the `pip` installer:

```
pip install mytextgrid -U
```

After that, you can import the package as in the following line.

```
import mytextgrid
```

### 2. The basics

## Reading a TextGrid from a file
To read an existing TextGrid file use the `read_from_file()` function. TextGrid files come in [three formats](https://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html): long, short and binary. At this moment, only the long format is supported. 

```
import mytextgrid

# Read TextGrid
>>> path = r'C:\Users\rolan\Documents\projects\Mary_John_bell.TextGrid'
>>> tg = mytextgrid.read_from_file(path)
```

## Describe a TextGrid
```
>>> tg.describe()

TextGrid:
    Startig time (sec):    0
    Ending time (sec):     1
    Number of tiers:       3
Tiers summary:
    0   IntervalTier    Mary    (size = 1)
    1   IntervalTier    John    (size = 1)
    2   PointTier       bell    (size = 0)
```

## Manipulating a TextGrid
```
# Insert tier
>>> tone_tier = tg.insert_tier("tone", False)
>>> segment_tier = tg.insert_tier("segment")
>>> word_tier = tg.insert_tier("word")
>>> phrase_tier = tg.insert_tier("phrase")

# Point tier: Inserting points
>>> tone_tier.insert_point(0.66, "H")
>>> tone_tier.insert_point(0.9, "L")

# Interval tier: Inserting boundaries
>>> segment_tier.insert_boundaries(0.23, 0.30, 0.42, 0.62, 0.70, 0.82, 0.98)
>>> word_tier.insert_boundaries(0.23, 0.42, 0.98)
>>> phrase_tier.insert_boundaries(0.23, 0.98)

# Interval tier: Populate intervals with text
>>> segment_tier.set_text_at_index(1, 'e', 'l', 'p', 'e', 'rr', 'o')
>>> word_tier.set_text_at_index(1, 'el')
>>> word_tier.set_text_at_index(2, 'perro')
>>> phrase_tier.set_text_at_index(1, 'el perro')

# Remove a tier
>>> tg.remove_tier(0)
>>> tg.describe()
```

## traversing through a TextGrid
A TextGrid object is a container that stores one or more Tier objects. Each tier, at the same time, is a container itself and stores two types of objects: Intervals or Points. Depending on that, a tier can be a IntervalTier or PointTier. To iterate through these containers use the `for` loop as in the following example. 

```
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
```

## Writing TextGrid to a file

You can write a `TextGrid` to different types of files.

```
tg.write('example1-long.TextGrid')
tg.write('example1-short.TextGrid', True) # Write the TextGrid a short format TextGrid

# Write to a JSON file
tg.write_as_json('example1.json')
```

## Creating a TextGrid from scratch

Creating a TextGrid from the scratch is easy, just take a look to the following lines of code.

```
# Create an empty TextGrid
>>> new_tg = mytextgrid.create_textgrid(xmin = 0, xmax = 1)
```

Becareful, the resulting object does not contain any tier.
