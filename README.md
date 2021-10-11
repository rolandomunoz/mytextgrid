# Python package: mytextgrid
A tiny python project for creating, reading, writing and querying Praat annotation files (TextGrid).

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
import MyTextGrid

# Create an empty TextGrid
path = r'C:\Users\rolan\Documents\projects\sentence1.TextGrid'
tg = MyTextGrid.read_from_file(path)
```

## Manipulating a TextGrid
```
# Insert tiers
tg.insert_point_tier("tone")
tg.insert_interval_tier("segment")
tg.insert_interval_tier("word")
tg.insert_interval_tier("phrase")

# Insert points and intervals
tg.insert_boundary('segment', 0.23, 0.30, 0.42, 0.62, 0.70, 0.82, 0.90, 0.98)
tg.insert_boundary('word', 0.23, 0.42, 0.98)
tg.insert_boundary('phrase', 0.23, 0.98)

tg.insert_point('tone', 0.66, "H")
tg.insert_point('tone', 0.94, "L")

# Add text to intervals
tg.set_interval_text('segment', 1, 'e', 'l', 'p', 'e', 'rr', 'o')
tg.set_interval_text('word', 1, 'el')
tg.set_interval_text('word', 2, 'perro')
tg.set_interval_text('phrase', 1, 'el perro')
```

## Traversing a TextGrid
A TextGrid object is a container that stores one or more Tier objects. Each tier, at the same time, is a container itself and stores only two kinds of objects: Intervals or Points. Depending on that, a tier can be a IntervalTier or PointTier. To iterate through these containers use the `for` loop as in the following example. 

```
# where tg is a variable that contains a TextGrid object.

# Iterate through a TextGrid 
for tier in tg:
    print(tier.name)
    print(tier.xmin)
    print(tier.xmax)
    print(tier.class_)
    # Iterate through an interval tier
    if tier.class_ == 'IntervalTier':
        for interval in tier:
            # Print Interval attributes
            print(interval.text)
            print(interval.xmin)
            print(interval.xmax)
    # Iterate through an interval tier
    elif tier.class_ == 'PointTier':
        for point in tier:
            # Print Point attributes
            print(point.time)
            print(point.text)
```

## Writing TextGrid

You can write a `TextGrid` to different types of files.

```
# Write to a TextGrid file
path = r'C:\Users\user\Documents\sentence1.TextGrid'
tg.to_textgrid(path)

# Write to a CSV file
csv_path = r'C:\Users\user\Documents\sentence1.csv'
tg.to_csv(csv_path)

# Write to a JSON file
csv_path = r'C:\Users\user\Documents\sentence1.json'
tg.to_json(csv_path)
```

## Creating a TextGrid from scratch

Creating a TextGrid from the scratch is easy, just take a look to the following lines of code.

```
import mytextgrid

# Create an empty TextGrid
tg = mytextgrid.create_textgrid(name = 'dog', xmin = 0, xmax = 1)
```

In the first line, use `import mytextgrid` to import the package. This package gives you access to the function `create_textgrid()` which is used in the fourth line. Use this function to create an empty `TextGrid`. This function takes three arguments: the name, the starting and the ending time of a TextGrid. The object is created and assigned to the variable `tg`.
