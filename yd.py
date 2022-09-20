import re
import operator

compat_str = str

def lookup_unit_table(unit_table, s):
    units_re = '|'.join(re.escape(u) for u in unit_table)
    m = re.match(
        r'(?P<num>[0-9]+(?:[,.][0-9]*)?)\s*(?P<unit>%s)\b' % units_re, s)
    if not m:
        return None
    num_str = m.group('num').replace(',', '.')
    mult = unit_table[m.group('unit')]
    return int(float(num_str) * mult)

def parse_filesize(s):
    if s is None:
        return None

    # The lower-case forms are of course incorrect and unofficial,
    # but we support those too
    _UNIT_TABLE = {
        'B': 1,
        'b': 1,
        'bytes': 1,
        'KiB': 1024,
        'KB': 1000,
        'kB': 1024,
        'Kb': 1000,
        'kb': 1000,
        'kilobytes': 1000,
        'kibibytes': 1024,
        'MiB': 1024 ** 2,
        'MB': 1000 ** 2,
        'mB': 1024 ** 2,
        'Mb': 1000 ** 2,
        'mb': 1000 ** 2,
        'megabytes': 1000 ** 2,
        'mebibytes': 1024 ** 2,
        'GiB': 1024 ** 3,
        'GB': 1000 ** 3,
        'gB': 1024 ** 3,
        'Gb': 1000 ** 3,
        'gb': 1000 ** 3,
        'gigabytes': 1000 ** 3,
        'gibibytes': 1024 ** 3,
        'TiB': 1024 ** 4,
        'TB': 1000 ** 4,
        'tB': 1024 ** 4,
        'Tb': 1000 ** 4,
        'tb': 1000 ** 4,
        'terabytes': 1000 ** 4,
        'tebibytes': 1024 ** 4,
        'PiB': 1024 ** 5,
        'PB': 1000 ** 5,
        'pB': 1024 ** 5,
        'Pb': 1000 ** 5,
        'pb': 1000 ** 5,
        'petabytes': 1000 ** 5,
        'pebibytes': 1024 ** 5,
        'EiB': 1024 ** 6,
        'EB': 1000 ** 6,
        'eB': 1024 ** 6,
        'Eb': 1000 ** 6,
        'eb': 1000 ** 6,
        'exabytes': 1000 ** 6,
        'exbibytes': 1024 ** 6,
        'ZiB': 1024 ** 7,
        'ZB': 1000 ** 7,
        'zB': 1024 ** 7,
        'Zb': 1000 ** 7,
        'zb': 1000 ** 7,
        'zettabytes': 1000 ** 7,
        'zebibytes': 1024 ** 7,
        'YiB': 1024 ** 8,
        'YB': 1000 ** 8,
        'yB': 1024 ** 8,
        'Yb': 1000 ** 8,
        'yb': 1000 ** 8,
        'yottabytes': 1000 ** 8,
        'yobibytes': 1024 ** 8,
    }

    return lookup_unit_table(_UNIT_TABLE, s)


def _match_one(filter_part, dct):
    COMPARISON_OPERATORS = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '=': operator.eq,
        '!=': operator.ne,
    }
    operator_rex = re.compile(r'''(?x)\s*
        (?P<key>[a-z_]+)
        \s*(?P<op>%s)(?P<none_inclusive>\s*\?)?\s*
        (?:
            (?P<intval>[0-9.]+(?:[kKmMgGtTpPeEzZyY]i?[Bb]?)?)|
            (?P<quote>["\'])(?P<quotedstrval>(?:\\.|(?!(?P=quote)|\\).)+?)(?P=quote)|
            (?P<strval>(?![0-9.])[a-z0-9A-Z]*)
        )
        \s*$
        ''' % '|'.join(map(re.escape, COMPARISON_OPERATORS.keys())))
    m = operator_rex.search(filter_part)
    if m:
        op = COMPARISON_OPERATORS[m.group('op')]
        actual_value = dct.get(m.group('key'))
        if (m.group('quotedstrval') is not None
            or m.group('strval') is not None
            # If the original field is a string and matching comparisonvalue is
            # a number we should respect the origin of the original field
            # and process comparison value as a string (see
            # https://github.com/ytdl-org/youtube-dl/issues/11082).
            or actual_value is not None and m.group('intval') is not None
                and isinstance(actual_value, compat_str)):
            if m.group('op') not in ('=', '!='):
                raise ValueError(
                    'Operator %s does not support string values!' % m.group('op'))
            comparison_value = m.group('quotedstrval') or m.group('strval') or m.group('intval')
            quote = m.group('quote')
            if quote is not None:
                comparison_value = comparison_value.replace(r'\%s' % quote, quote)
        else:
            try:
                comparison_value = int(m.group('intval'))
            except ValueError:
                comparison_value = parse_filesize(m.group('intval'))
                if comparison_value is None:
                    comparison_value = parse_filesize(m.group('intval') + 'B')
                if comparison_value is None:
                    raise ValueError(
                        'Invalid integer value %r in filter part %r' % (
                            m.group('intval'), filter_part))
        if actual_value is None:
            return m.group('none_inclusive')
        return op(actual_value, comparison_value)

    UNARY_OPERATORS = {
        '': lambda v: (v is True) if isinstance(v, bool) else (v is not None),
        '!': lambda v: (v is False) if isinstance(v, bool) else (v is None),
    }
    operator_rex = re.compile(r'''(?x)\s*
        (?P<op>%s)\s*(?P<key>[a-z_]+)
        \s*$
        ''' % '|'.join(map(re.escape, UNARY_OPERATORS.keys())))
    m = operator_rex.search(filter_part)
    if m:
        op = UNARY_OPERATORS[m.group('op')]
        actual_value = dct.get(m.group('key'))
        return op(actual_value)

    raise ValueError('Invalid filter part %r' % filter_part)


def match_str(filter_str, dct):
    """ Filter a dictionary with a simple string syntax. Returns True (=passes filter) or false """

    return all(
        _match_one(filter_part, dct) for filter_part in filter_str.split('&'))

def match_filter_func(filter_str):
    def _match_func(info_dict):
        if match_str(filter_str, info_dict):
            return None
        else:
            video_title = info_dict.get('title', info_dict.get('id', 'video'))
            return '%s does not pass filter %s, skipping ..' % (video_title, filter_str)
    return _match_func

if __name__ == '__main__':
    info_dict = {'title': '吴昊 xxxx'}
    ret = match_filter_func("titile = '吴昊'")(info_dict)
    print(ret)
