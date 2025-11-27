import decimal
decimal.getcontext().prec = 16

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

def obj_to_decimal(time, message=None):
    """
    Convert a number to :class:`decimal.Decimal`.

    Parameters
    ----------
    time : int, float str or decimal.Decimal
        A number in seconds to be converted.
    message : str
        A message to show if raise an exception.

    Returns
    -------
    :class:`decimal.Decimal`
        A :class:`decimal.Decimal` object representing the time in seconds.
    """
    if isinstance(time, decimal.Decimal):
        return time
    elif isinstance(time, (int, float)):
        return decimal.Decimal(str(time))
    elif isinstance(time, str):
        return decimal.Decimal(time)
    else:
        message = 'time parameter must be int, float, str or decimal.Decimal'
        raise TypeError(message)

def detect_encoding(byte_data):
    """
    Detect the encoding given a binary data.

    Praat encodes text files using UTF-8, UTF-16 with BOM, ISO 8859-1,
    Windows-1252 and Mac OS Roman.
    """
    encodings = [
        'utf-8',
        'utf-16le',
        'utf-16be',
        'windows-1252',
        'mac_roman',
        'iso-8859-1',
    ]
    for encoding in encodings:
        try:
            byte_data.decode(encoding)
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
