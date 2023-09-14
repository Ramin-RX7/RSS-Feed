import re
import time

from email.utils import mktime_tz, parsedate_tz

__all__ = ("parse_pubdate","parse_time",)



def parse_pubdate(text):
    """
    >>> parse_pubdate('Fri, 21 Nov 1997 09:55:06 -0600')
    880127706
    >>> parse_pubdate('2003-12-13T00:00:00+02:00')
    1071266400
    >>> parse_pubdate('2003-12-13T18:30:02Z')
    1071340202
    >>> parse_pubdate('Mon, 02 May 1960 09:05:01 +0100')
    -305049299
    """
    if not text:
        return 0

    parsed = parsedate_tz(text)
    if parsed is not None:
        try:
            pubtimeseconds = int(mktime_tz(parsed))
            return pubtimeseconds
        except(OverflowError, ValueError):
            print("epoch < t > 2038")
            return 0

    try:
        parsed = time.strptime(text[:19], '%Y-%m-%dT%H:%M:%S')
        if parsed is not None:
            m = re.match(r'^(?:Z|([+-])([0-9]{2})[:]([0-9]{2}))$', text[19:])
            if m:
                parsed = list(iter(parsed))
                if m.group(1):
                    offset = 3600 * int(m.group(2)) + 60 * int(m.group(3))
                    if m.group(1) == '-':
                        offset = 0 - offset
                else:
                    offset = 0
                parsed.append(offset)
                return int(mktime_tz(tuple(parsed)))
            else:
                return int(time.mktime(parsed))
    except Exception:
        pass

    print('Cannot parse date: %s', repr(text))
    return 0
