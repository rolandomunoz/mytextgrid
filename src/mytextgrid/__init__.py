"""A tiny python project for creating, reading, writing and querying Praat annotation files
(TextGrid).
"""
from mytextgrid.core.textgrid import create_textgrid
from mytextgrid.io.textgrid_in import read_from_file
from mytextgrid.io.textgrid_in import read_from_stream
from mytextgrid.core.textgrid import TextGrid