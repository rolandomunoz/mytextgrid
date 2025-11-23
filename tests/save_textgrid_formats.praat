# -----------------------------------------------------------------------------
# Script Name: save_textgrid_formats
# Description: Create a TextGrid object and save multiple versions of it with
#              different encodings and formats (short long and binary)
# -----------------------------------------------------------------------------
#
# MIT License
#
# Copyright (c) 2025 Rolando Muñoz Aramburú
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# -----------------------------------------------------------------------------
textgrid_id = Create TextGrid: 0, 1, "Mary John bell", "bell"

boundaries# = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}
tier_mary$# = splitByWhitespace$#("ro lan do mu ñoz a ram bu rú")
tier_john$# = splitByWhitespace$#("cá qué quí có cú güe bu rú")
tier_bell$# = {"r", "o", "l", "a", "n", "d", "o", "ñ", ""}
for i to size(boundaries#)
    Insert boundary: 1, boundaries#[i]
    Insert boundary: 2, boundaries#[i]
    Insert point: 3, boundaries#[i], tier_bell$#[i]
endfor

for i to size(tier_mary$#)
    Set interval text: 1, i, tier_mary$#[i]
endfor

for i to size(tier_john$#)
    Set interval text: 2, i, tier_john$#[i]
endfor

# Save in multiple formats

writing_settings$# = {"UTF-8", "UTF-16", "try ISO Latin-1, then UTF-16"}
encoding_alias$# = {"UTF8", "UTF16", "ISO_Latin_1"}

createFolder("tmp")
basename$ = "tmp/text"
for i to size(writing_settings$#)
    Text writing settings: writing_settings$#[i]
    Save as text file: basename$ + "-" + encoding_alias$#[i] + "-LONG" + ".TextGrid"
    Save as short text file: basename$ + "-" + encoding_alias$#[i] + "-SHORT" + ".TextGrid"
    Save as binary file: basename$ + "-" + encoding_alias$#[i] + "-BIN" + ".TextGrid"
endfor

removeObject: textgrid_id
