"""Implementation of JSONEncoder

Simplified verion from Python3.5 that understands GeneratorType
"""
import re
from types import GeneratorType

ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]')
ESCAPE_ASCII = re.compile(r'([\\"]|[^\ -~])')
HAS_UTF8 = re.compile(b'[\x80-\xff]')
ESCAPE_DCT = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}
for i in range(0x20):
    ESCAPE_DCT.setdefault(chr(i), '\\u{0:04x}'.format(i))

INFINITY = float('inf')


def _make_iterencode(
                     # HACK: hand-optimized bytecode; turn globals into locals
                     ValueError=ValueError,
                     dict=dict,
                     float=float,
                     int=int,
                     isinstance=isinstance,
                     list=list,
                     str=str,
                     tuple=tuple,
                     ):

    def _encoder(s):
        """Return a JSON representation of a Python string """
        def replace(match):
            return ESCAPE_DCT[match.group(0)]
        return '"' + ESCAPE.sub(replace, s) + '"'

    def _floatstr(o):
        # Check for specials.  Note that this type of test is processor
        # and/or platform-specific, so do tests which don't depend on the
        # internals.

        if o != o:
            text = 'NaN'
        elif o == float('inf'):
            text = 'Infinity'
        elif o == -float('inf'):
            text = '-Infinity'
        else:
            return repr(o)

        return text

    def _iterencode_list(lst):
        if not lst:
            yield '[]'
            return
        buf = '['
        first = True
        for value in lst:
            if first:
                first = False
            else:
                buf = ','
            if isinstance(value, str):
                yield buf + _encoder(value)
            elif value is None:
                yield buf + 'null'
            elif value is True:
                yield buf + 'true'
            elif value is False:
                yield buf + 'false'
            elif isinstance(value, int):
                # Subclasses of int/float may override __str__, but we still
                # want to encode them as integers/floats in JSON. One example
                # within the standard library is IntEnum.
                yield buf + str(int(value))
            elif isinstance(value, float):
                # see comment above for int
                yield buf + _floatstr(float(value))
            else:
                yield buf
                if isinstance(value, (list, tuple, GeneratorType)):
                    chunks = _iterencode_list(value)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value)
                else:
                    chunks = _iterencode(value)
                yield from chunks
        yield ']'

    def _iterencode_dict(dct):
        if not dct:
            yield '{}'
            return
        yield '{'
        first = True
        for key, value in dct.items():
            if isinstance(key, str):
                pass
            # JavaScript is weakly typed for these, so it makes sense to
            # also allow them.  Many encoders seem to do something like this.
            elif isinstance(key, float):
                # see comment for int/float in _make_iterencode
                key = _floatstr(float(key))
            elif key is True:
                key = 'true'
            elif key is False:
                key = 'false'
            elif key is None:
                key = 'null'
            elif isinstance(key, int):
                # see comment for int/float in _make_iterencode
                key = str(int(key))
            else:
                raise TypeError("key " + repr(key) + " is not a string")
            if first:
                first = False
            else:
                yield ','
            yield _encoder(key)
            yield ':'
            if isinstance(value, str):
                yield _encoder(value)
            elif value is None:
                yield 'null'
            elif value is True:
                yield 'true'
            elif value is False:
                yield 'false'
            elif isinstance(value, int):
                # see comment for int/float in _make_iterencode
                yield str(int(value))
            elif isinstance(value, float):
                # see comment for int/float in _make_iterencode
                yield _floatstr(float(value))
            else:
                if isinstance(value, (list, tuple, GeneratorType)):
                    chunks = _iterencode_list(value)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value)
                else:
                    chunks = _iterencode(value)
                yield from chunks
        yield '}'

    def _iterencode(o):
        if isinstance(o, str):
            yield _encoder(o)
        elif o is None:
            yield 'null'
        elif o is True:
            yield 'true'
        elif o is False:
            yield 'false'
        elif isinstance(o, int):
            # see comment for int/float in _make_iterencode
            yield str(int(o))
        elif isinstance(o, float):
            # see comment for int/float in _make_iterencode
            yield _floatstr(float(o))
        elif isinstance(o, (list, tuple, GeneratorType)):
            yield from _iterencode_list(o)
        elif isinstance(o, dict):
            yield from _iterencode_dict(o)
        else:
            raise ValueError("'%r' is not JSON encodable." % o)
    return _iterencode

dumps = _make_iterencode()
