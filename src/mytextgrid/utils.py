import decimal
decimal.getcontext().prec = 16

def obj_to_decimal(time, message = None):
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

def is_textgrid_file(filepath):
    """
    Validates if a file is a recognized Praat TextGrid file format.

    The function checks the initial bytes of the file for the required
    header signature, supporting both binary and text formats, and handling
    various encodings and end-of-line (EOL) conventions. It performs a minimal
    read operation to verify the header, ensuring efficiency.

    Parameters
    ----------
    filepath : str
        The path to the file to be validated.

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
    BOM_LE = b'\xff\xfe' # LE
    BOM_BE = b'\xfe\xff' # BE
    CR = b'\x0d'
    LF = b'\x0a'
    LF_UTF16_LE = b'\x0a\x00'
    CR_UTF16_LE = b'\x0d\x00'
    LF_UTF16_BE = b'\x00\x0a'
    CR_UTF16_BE = b'\x00\x0d'
    TEXTGRID_BINARY_MARK = b'ooBinaryFile\x08TextGrid'
    TEXTGRID_UTF8_MARK = 'File type = "ooTextFile"\nObject class = "TextGrid"\n'

    byte_stream = b''
    line_counter = 0
    byte_window = 1
    encoding = 'utf-8'
    max_header_size = 51

    # Read the first two lines of a TextGrid file
    with open(filepath, 'rb') as f:
        current_position = f.tell()
        boom_mark = f.read(2)
        if boom_mark == BOM_LE:
            current_position = 2
            byte_window = 2
            LF, CR = LF_UTF16_LE, CR_UTF16_LE
            encoding = 'utf-16le'
            max_header_size = 102
        elif boom_mark == BOM_BE:
            current_position = 2
            byte_window = 2
            LF, CR = LF_UTF16_BE, CR_UTF16_BE
            encoding = 'utf-16be'
            max_header_size = 102
        else:
            # Read the first 21 bytes to look for the TEXTGRID_BYTE_MARK
            textgrid_binary_mark = boom_mark + f.read(19)
            if textgrid_binary_mark == TEXTGRID_BINARY_MARK:
                return True

        f.seek(current_position)
        while len(byte_stream) < max_header_size:
            byte = f.read(byte_window)
            if not byte:
                break

            if byte == LF: # Mordern MAC and LINUX
                line_counter += 1
            elif byte == CR: #CR
                next_byte = f.read(byte_window)
                if next_byte == LF: # CRLF (Windows)
                    byte = LF
                else: # CR (Classic MAC)
                    byte = LF
                    f.seek(f.tell() - byte_window)
                line_counter += 1

            if line_counter > 2:
                break

            byte_stream = byte_stream + byte

    textgrid_utf8_mark = byte_stream.decode(encoding)
    if textgrid_utf8_mark == TEXTGRID_UTF8_MARK:
        return True
    return False
