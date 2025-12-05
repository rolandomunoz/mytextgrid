_BINARY_MARK = b'ooBinaryFile\x08TextGrid'

_UTF8_LF_MARK = b'File type = "ooTextFile"\nObject class = "TextGrid"\n'
_UTF8_CR_MARK = b'File type = "ooTextFile"\rObject class = "TextGrid"\r'
_UTF8_CRLF_MARK = b'File type = "ooTextFile"\r\nObject class = "TextGrid"\r\n'

_UTF16BE_CR_MARK = (b'\xfe\xff\x00F\x00i\x00l\x00e\x00 \x00t'
                    b'\x00y\x00p\x00e\x00 \x00=\x00 \x00"\x00o'
                    b'\x00o\x00T\x00e\x00x\x00t\x00F\x00i\x00l'
                    b'\x00e\x00"\x00\r\x00O\x00b\x00j\x00e\x00c'
                    b'\x00t\x00 \x00c\x00l\x00a\x00s\x00s\x00 '
                    b'\x00=\x00 \x00"\x00T\x00e\x00x\x00t\x00G'
                    b'\x00r\x00i\x00d\x00"\x00\r\x00\r')

_UTF16BE_LF_MARK = (b'\xfe\xff\x00F\x00i\x00l\x00e\x00 \x00t\x00y\x00p'
                    b'\x00e\x00 \x00=\x00 \x00"\x00o\x00o\x00T\x00e\x00'
                    b'x\x00t\x00F\x00i\x00l\x00e\x00"\x00\n\x00O\x00b'
                    b'\x00j\x00e\x00c\x00t\x00 \x00c\x00l\x00a\x00s'
                    b'\x00s\x00 \x00=\x00 \x00"\x00T\x00e\x00x\x00t'
                    b'\x00G\x00r\x00i\x00d\x00"\x00\n\x00\n')

_UTF16BE_CRLF_MARK = (b'\xfe\xff\x00F\x00i\x00l\x00e\x00 \x00t'
                      b'\x00y\x00p\x00e\x00 \x00=\x00 \x00"'
                      b'\x00o\x00o\x00T\x00e\x00x\x00t\x00F'
                      b'\x00i\x00l\x00e\x00"\x00\r\x00\n\x00O'
                      b'\x00b\x00j\x00e\x00c\x00t\x00 \x00c'
                      b'\x00l\x00a\x00s\x00s\x00 \x00=\x00 \x00"'
                      b'\x00T\x00e\x00x\x00t\x00G\x00r\x00i\x00d'
                      b'\x00"\x00\r\x00\n\x00\r\x00\n')

_UTF16LE_LF_MARK = (b'\xff\xfeF\x00i\x00l\x00e\x00 \x00t\x00y\x00p'
                    b'\x00e\x00 \x00=\x00 \x00"\x00o\x00o\x00T\x00'
                    b'e\x00x\x00t\x00F\x00i\x00l\x00e\x00"\x00\n'
                    b'\x00O\x00b\x00j\x00e\x00c\x00t\x00 \x00c\x00l'
                    b'\x00a\x00s\x00s\x00 \x00=\x00 \x00"\x00T\x00e'
                    b'\x00x\x00t\x00G\x00r\x00i\x00d\x00"\x00\n\x00'
                    b'\n\x00')

_UTF16LE_CR_MARK = (b'\xff\xfeF\x00i\x00l\x00e\x00 \x00t\x00y\x00p'
                    b'\x00e\x00 \x00=\x00 \x00"\x00o\x00o\x00T\x00'
                    b'e\x00x\x00t\x00F\x00i\x00l\x00e\x00"\x00\r'
                    b'\x00O\x00b\x00j\x00e\x00c\x00t\x00 \x00c'
                    b'\x00l\x00a\x00s\x00s\x00 \x00=\x00 \x00"\x00T'
                    b'\x00e\x00x\x00t\x00G\x00r\x00i\x00d\x00"\x00'
                    b'\r\x00\r\x00')

_UTF16LE_CRLF_MARK = (b'\xff\xfeF\x00i\x00l\x00e\x00 \x00t\x00y\x00'
                      b'p\x00e\x00 \x00=\x00 \x00"\x00o\x00o\x00T\x00'
                      b'e\x00x\x00t\x00F\x00i\x00l\x00e\x00"\x00\r\x00'
                      b'\n\x00O\x00b\x00j\x00e\x00c\x00t\x00 \x00c\x00l'
                      b'\x00a\x00s\x00s\x00 \x00=\x00 \x00"\x00T\x00e'
                      b'\x00x\x00t\x00G\x00r\x00i\x00d\x00"\x00\r\x00'
                      b'\n\x00\r\x00\n\x00')

_TEXTGRID_HEADERS = [
    _UTF8_CRLF_MARK, _UTF8_CR_MARK, _UTF8_LF_MARK,
    _UTF16BE_LF_MARK, _UTF16BE_CR_MARK, _UTF16BE_CRLF_MARK,
    _UTF16LE_LF_MARK, _UTF16LE_CR_MARK, _UTF16LE_CRLF_MARK
]

_ALL_TEXTGRID_HEADERS = _TEXTGRID_HEADERS + [_BINARY_MARK]

_BOOM_MARK_DICT = {
    b'\xfe\xff': 'utf-16be', # Big endian
    b'\xff\xfe': 'utf-16le', # Little endian
}

_TEXTGRID_ENCODINGS = [
    'utf-8',
    'windows-1252',
    'mac_roman',
    'iso-8859-1',
]


def detect_textgrid_encoding(fpath):
    """
    Detects the encoding of a Praat TextGrid file.

    This function determines the file's text encoding. The decoding
    attempts are performed in the following strict order:

        - UTF-16 with BOM
        - UTF-8 without BOM
        - Windows-1252
        - Mac OS Roman
        - ISO 8859-1 (used as a final fallback)

    Parameters
    ----------
    fpath : str
        The file path to the TextGrid file to be evaluated.

    Returns
    -------
    str
        The detected encoding string: one of {'utf-16be', 'utf-16le',
        'utf-8', 'windows-1252', 'mac_roman', 'iso-8859-1'}. Returns an
         empty string ('') if a valid encoding cannot be detected.
    """
    if not is_textgrid_file(fpath, include_binary=False):
        return ''

    with open(fpath, 'rb') as f:
        byte_stream = f.read()

    boom_mark = byte_stream[0:2]
    if boom_mark in _BOOM_MARK_DICT:
        return _BOOM_MARK_DICT[boom_mark]

    for encoding in _TEXTGRID_ENCODINGS:
        try:
            byte_stream.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return ''


def is_textgrid_file(filepath, include_binary=True):
    """
    Validates if a file is a recognized Praat TextGrid file format.

    The function checks the initial bytes of the file for the required
    header signature, supporting both binary and text formats, and handling
    various encodings and end-of-line (EOL) conventions.

    Parameters
    ----------
    filepath : str
        The path to the file to be validated.
    include_binary : bool
        Check the header in binary files.

    Returns
    -------
    bool
        Returns `True` if the file contains the expected TextGrid header
        signature (binary or text). Returns `False` otherwise.

    Notes
    -----
    The function accounts for:

    * **Encodings Supported:** UTF-16LE, UTF-16BE (detected via BOM), and UTF-8
        (default, relying on ASCII compatibility for the header).
    * **EOL Conventions Handled:** LF, CRLF, and CR.
    * **Formats Checked:** Binary (ooBinaryFile) and Text (ooTextFile, Long/Short).
    """
    if include_binary:
        headers_to_check = _ALL_TEXTGRID_HEADERS
    else:
        headers_to_check = _TEXTGRID_HEADERS

    with open(filepath, 'rb') as f:
        chunk = f.read(4096)

    for header in headers_to_check:
        if chunk.startswith(header):
            return True
    return False
