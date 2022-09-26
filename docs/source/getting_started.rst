***************
Getting started
***************

``mytextgrid`` is a package written in Python to manipulate TextGrid files. A TextGrid is a type of representation for time-aligned annotations used by `Praat <https://www.fon.hum.uva.nl/praat/>`_, a software for doing phonetics.

With ``mytextgrid`` you can read a TextGrid file or just create a new one from scratch. Once a TextGrid is loaded in Python,
 you can modify it or make some queries. In this tutorial I will walk you through the basics of this package.

Installation
============

You can get the lastest release of this package using the `pip` installer:

.. code-block:: console

   pip install mytextgrid -U

After that, you can import the package:

.. code-block:: python
   :linenos:

   import mytextgrid

Basic operations
================

A ``TextGrid`` is type of object that represent a time-aligned annotation. They have many uses when working with sound files in Praat. Some people use them in phonetic transcriptions, others make notes of different kind; other people use annotations to run scripts over some specific parts of a sound file.

A TextGrid is hierarchical structured. It contains one or more tiers, which at the same time, contain time-aligned marks. These marks can be of ``Interval`` or ``Point`` type. Marks in intervals have a starting and ending time, while points refer to a specific point in time. Tiers that store ``Interval`` objects are ``IntervalTier``, whereas ``Point`` objects are stored in ``PointTier`` tiers.

Reading a TextGrid file
-----------------------

To read a TextGrid file you can use the function ``mytextgrid.read_from_file()``. This returns a ``TextGrid`` object.

.. code-block:: python

   >>> import mytextgrid

   >>> path = r'C:\Users\rolan\Documents\projects\sentence1.TextGrid'
   >>> tg = mytextgrid.read_from_file(path)

.. warning::

   TextGrid files come in `three formats`_: long, short and binary. At this moment, only the long format is supported.

.. _three formats: https://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html

Creating a TextGrid from scratch
--------------------------------

To create a TextGrid file you can use the function ``mytextgrid.create_textgrid()``. This returns an empty ``TextGrid`` object.

.. code-block:: python
   :caption: Creating a TextGrid from scratch

   >>> import mytextgrid

   >>> tg = mytextgrid.create_textgrid(xmin = 0, xmax = 1)

In the code, we specify the starting (``xmin``) and ending (``xmax``) time of the TextGrid. The returned ``TextGrid`` is assigned to ``tg``.

.. warning::

   An empty TextGrid `does not` contain any tier. In order we can work with this object, we need to insert at least one tier.

Manipulating a TextGrid
-----------------------

Now that you know how to create and read a TextGrid, you probably want to make some changes to it. So Let's do it!

First, create an empty TextGrid as in the previous section. Once this is done, the next step is to insert some empty
tiers on it. Let's start by inserting three interval tiers: `segment`, `word` and `comments`.

.. code-block:: python
   :caption: Inserting tiers

   >>> segment_tier = tg.insert_tier("segment")
   >>> word_tier = tg.insert_tier("word")
   >>> phrase_tier = tg.insert_tier("comments")

Now, insert a point tier named `tone`.

.. code-block:: python
   :caption: Inserting tiers

   >>> tone_tier = tg.insert_tier("tone", False) # point tier

As you can see, the method ``insert_tier()`` creates interval tiers by default. To create a point tier,
we need to provide ``False`` as the second argument (`interval_tier`).

Finally, we can have a quick view of the TextGrid using the ``describe()`` method.

.. code-block:: python

   >>> tg.describe()

       TextGrid:
           Startig time (sec):    0
           Ending time (sec):     1
           Number of tiers:       4
       Tiers summary:
           0	PointTier	tone	(size = 0)
           1	IntervalTier	segment	(size = 1)
           2	IntervalTier	word	(size = 1)
           3	IntervalTier	comments	(size = 1)

For now, we have a TextGrid with four empty tiers. Let's insert two marks in the point tier.

.. code-block:: python
   :caption: Inserting point marks

    >>> # In the point tier, insert two points.
    >>> tone_tier.insert_point(0.66, "H")
    >>> tone_tier.insert_point(0.9, "L")

Note that when we insert a mark, we place the mark at a specific time in a tier
and then, a text can be associated with it. This is done in one step using the method
``insert_point()``.

Working with interval tiers is a bit different since we first create the intervals
and then we set their text contents.

.. code-block:: python
   :caption: Inserting boundaries

   >>> # In the interval tier, insert boundaries
   >>> segment_tier.insert_boundaries(0.23, 0.30, 0.42, 0.62, 0.70, 0.82, 0.98)
   >>> word_tier.insert_boundaries(0.23, 0.42, 0.98)
   >>> phrase_tier.insert_boundaries(0.23, 0.98)

In the previous example, several boundaries were inserted using ``insert_boundaries()``.
To set the text of the intervals, use the ``set_text_at_index()``. Each new interval we
have created has a position starting from 0. So, if want to add text content to the interval
1 and 2 of the tier `word`, we can do it as in the following example:

.. code-block:: python
   :caption: Manipulating a TextGrid

   >>> # We can populate intervals with text
   >>> word_tier.set_text_at_index(1, 'el')
   >>> word_tier.set_text_at_index(2, 'perro')

We can also express the same idea in one line.

.. code-block:: python
   :caption: Manipulating a TextGrid

   >>> word_tier.set_text_at_index(1, 'el', 'perro')
   >>> segment_tier.set_text_at_index(1, 'e', 'l', 'p', 'e', 'rr', 'o')

Use ``describe()`` to check the changes.

.. code-block:: python
   :caption: Describe a TextGrid

    TextGrid:
        Startig time (sec):    0
        Ending time (sec):     1
        Number of tiers:       5
    Tiers summary:
        0	PointTier	tone	(size = 2)
        1	IntervalTier	segment	(size = 8)
        2	IntervalTier	word	(size = 4)
        3	IntervalTier	comments	(size = 1)

Now, let's remove the tier `comments`.

.. code-block:: python
   :caption: Remove a tier

   >>> tg.remove_tier(3)

Check your changes again.

.. code-block:: python
   :caption: Describe a TextGrid

    TextGrid:
        Startig time (sec):    0
        Ending time (sec):     1
        Number of tiers:       5
    Tiers summary:
        0	PointTier	tone	(size = 2)
        1	IntervalTier	segment	(size = 8)
        2	IntervalTier	word	(size = 4)

Traversing a TextGrid
---------------------

We can use the ``for`` statement to visit all the tiers within a ``TextGrid``.

.. code-block:: python

   >>> # Iterate through a TextGrid
   >>> for tier in tg:
           print(tier.name)

We can also visit elements within a tier in the same way.

.. code-block:: python

   >>> # Iterate through a TextGrid
   >>> for tier in tg:
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

Writing TextGrid to a file
--------------------------

You can save a ``TextGrid`` object as a `TextGrid` or `json` file.

.. code-block:: python
   :caption: Write to a TextGrid file

   >>> path = r'C:\Users\user\Documents\sentence1.TextGrid'
   >>> tg.write(path)

.. code-block:: python
   :caption: Write to a JSON file

   >>> json_path = r'C:\Users\user\Documents\sentence1.json'
   >>> tg.write_as_json(csv_path)
