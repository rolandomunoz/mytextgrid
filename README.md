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

# Create an empty TextGrid
>>> path = r'C:\Users\rolan\Documents\projects\sentence1.TextGrid'
>>> tg = mytextgrid.read_from_file(path)
```

## Manipulating a TextGrid
```
# Insert tiers
>>> tone_tier = tg.insert_tier("tone", False) # Insert PointTier
>>> segment_tier = tg.insert_tier("segment")
>>> word_tier = tg.insert_tier("word")
>>> phrase_tier = tg.insert_tier("phrase")

# Insert points and intervals
>>> segment_tier.insert_boundaries(0.23, 0.30, 0.42, 0.62, 0.70, 0.82, 0.98)
>>> word_tier.insert_boundaries(0.23, 0.42, 0.98)
>>> phrase_tier.insert_boundaries(0.23, 0.98)

>>> tone_tier.insert_point('tone', 0.66, "H")
>>> tone_tier.insert_point('tone', 0.9, "L")

# Add text to intervals
>>> segment_tier.set_interval_text(1, 'e', 'l', 'p', 'e', 'rr', 'o')
>>> word_tier.set_interval_text(1, 'el')
>>> word_tier.set_interval_text(2, 'perro')
>>> phrase_tier.set_interval_text(1, 'el perro')
```

## Traversing a TextGrid
A TextGrid object is a container that stores one or more Tier objects. Each tier, at the same time, is a container itself and stores two types of objects: Intervals or Points. Depending on that, a tier can be a IntervalTier or PointTier. To iterate through these containers use the `for` loop as in the following example. 

```
>>> # where tg is a variable that contains a TextGrid object.

>>> # TextGrid info
>>> print(tg.xmin)
>>> print(tg.xmax)

>>> # Iterate through a TextGrid
>>> for tier in tg:
>>>     print(tier.name)

>>>    # Iterate through tiers
>>>    if tier.is_interval():
>>>        # For interval tiers
>>>        for interval in tier:
>>>            # Print Interval attributes
>>>            print(interval.xmin)
>>>            print(interval.xmax)
>>>            print(interval.text)
>>>    else:
>>>        # For point tiers
>>>        for point in tier:
>>>            # Print Point attributes
>>>            print(point.time)
>>>            print(point.text)
```

## Writing TextGrid to a file

You can write a `TextGrid` to different types of files.

```
# Write to a TextGrid file
>>> dst_path = r'C:\Users\user\Documents\sentence1.TextGrid'
>>> tg.write(dst_path)
>>> tg.write(dst_path, True) # Write the TextGrid a short format TextGrid

>>> # Write to a CSV file
>>> csv_path = r'C:\Users\user\Documents\sentence1.csv'
>>> tg.to_csv(csv_path)

>>> # Write to a JSON file
>>> csv_path = r'C:\Users\user\Documents\sentence1.json'
>>> tg.write_as_json(csv_path)
```

## Creating a TextGrid from scratch

Creating a TextGrid from the scratch is easy, just take a look to the following lines of code.

```
>>> import mytextgrid

>>> # Create an empty TextGrid
>>> tg = mytextgrid.create_textgrid(xmin = 0, xmax = 1)
```

Becareful, the resulting object does not contain tiers.
