***************
Getting started
***************

``mytextgrid`` is a package written in Python to manipulate TextGrid files. A TextGrid is a type of representation for time-aligned annotations used by `Praat <https://www.fon.hum.uva.nl/praat/>`_, a software for doing phonetics.

With ``mytextgrid`` you can read a TextGrid file or just create it from scratch. Once a TextGrid is loaded in Python, you can modify it or query it. In this tutorial I will walk you through the basics of this package.

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

To read a TextGrid file you can use ``mytextgrid.read_from_file()`` function. This returns a ``mytextgrid.TextGrid`` object.

.. code-block:: python
   :linenos:

   import mytextgrid
   
   path = r'C:\Users\rolan\Documents\projects\sentence1.TextGrid'
   tg = mytextgrid.read_from_file(path)

.. warning::

   TextGrid files come in `three formats`_: long, short and binary. At this moment, only the long format is supported.

.. _three formats: https://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html

Traversing a TextGrid
---------------------

We can use the ``for`` statement to visit all the tiers within a ``TextGrid``.
.. code-block:: python
   :linenos:
   :lineno-start: 5

   # tg is a variable that contains a TextGrid object.

   # TextGrid info
   print(tg.name)
   print(tg.xmin)
   print(tg.xmax)

   # Iterate through a TextGrid
   for tier in tg:
      print(tier.name)

We can also visit elements within a tier in the same way.

.. code-block:: python
   :linenos:
   :lineno-start: 5

   # Iterate through a TextGrid
   for tier in tg:
      # Iterate through tiers
      if tier.is_interval():
         # For interval tiers
         for interval in tier:
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

Creating a TextGrid from scratch
--------------------------------

To create a TextGrid file you can use ``mytextgrid.create_textgrid()`` function. This returns an empty ``mytextgrid.TextGrid`` object.

.. code-block:: python
   :caption: Creating a TextGrid from scratch
   :linenos:

   import mytextgrid

   tg = mytextgrid.create_textgrid(name = 'dog', xmin = 0, xmax = 1)

In the function, we need to specify the name (``name``) of the TextGrid, also its starting (``xmin``) and ending (``xmax``) time. The function returns a empty TextGrid object which is assigned to the variable ``tg``.

.. warning::

   An empty TextGrid `does not` contain any tier. In order we can work with this object, we need to insert at least one tier.

Manipulating a TextGrid
-----------------------

Now that you have created an empty TextGrid, let's insert some tiers and add text.

.. code-block:: python
   :caption: Manipulating a TextGrid
   :lineno-start: 4

   # First, let's insert three tiers
   tg.insert_point_tier("tone")
   tg.insert_interval_tier("segment")
   tg.insert_interval_tier("word")
   tg.insert_interval_tier("phrase")

   # Insert points and intervals
   tg.insert_boundaries('segment', 0.23, 0.30, 0.42, 0.62, 0.70, 0.82, 0.98)
   tg.insert_boundaries('word', 0.23, 0.42, 0.98)
   tg.insert_boundaries('phrase', 0.23, 0.98)

   tg.insert_point('tone', 0.66, "H")
   tg.insert_point('tone', 0.9, "L")

   # Add text to intervals
   tg.set_interval_text('segment', 1, 'e', 'l', 'p', 'e', 'rr', 'o')
   tg.set_interval_text('word', 1, 'el')
   tg.set_interval_text('word', 2, 'perro')
   tg.set_interval_text('phrase', 1, 'el perro')

Writing TextGrid to a file
--------------------------

You can save a ``TextGrid`` object as a text file. For that, you can choose between three types of formats: `TextGrid`, `json` or a `csv` table.

.. code-block:: python
   :caption: Write to a TextGrid file
   :lineno-start: 23

   path = r'C:\Users\user\Documents\sentence1.TextGrid'
   tg.to_textgrid(path)

.. code-block:: python
   :lineno-start: 23
   :caption: Write to a CSV file

   csv_path = r'C:\Users\user\Documents\sentence1.csv'
   tg.to_csv(csv_path)

.. code-block:: python
   :caption: Write to a JSON file
   :lineno-start: 23

   json_path = r'C:\Users\user\Documents\sentence1.json'
   tg.to_json(csv_path)
