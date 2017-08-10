from gzip import GzipFile
from io import BytesIO


def compress_string(uncompressed_string):
    """
    Takes a string object as an argument, compresses it in memory and returns
    a compressed string.
    Any Non UTF-8 characters will be stripped during this process.
    :param uncompressed_string: Regular Sting
    :return: GZipped string
    """
    bytes_buffer = BytesIO()
    with GzipFile(mode='wb', fileobj=bytes_buffer) as f:
        f.write(uncompressed_string.encode('utf-8', errors='ignore'))
    return bytes_buffer.getvalue()


def decompress_string(compressed_string):
    """
    Takes a compressed string object as an argument, decompresses it in memory
    and returns a regular string.
    Any Non UTF-8 characters will be stripped during this process.
    :param compressed_string: GZipped String
    :return: Regular String
    """
    with GzipFile(mode='rb', fileobj=BytesIO(compressed_string)) as f:
        return f.read().decode('utf-8', errors='ignore')
