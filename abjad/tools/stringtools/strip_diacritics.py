# -*- encoding: utf-8 -*-
import sys
import unicodedata


def strip_diacritics(binary_string):
    r'''Strip diacritics from `binary_string`:

    ::

        >>> binary_string = 'Dvo\xc5\x99\xc3\xa1k'

    ::

        >>> print(binary_string)
        Dvořák

    ::

        >>> stringtools.strip_diacritics(binary_string)
        'Dvorak'

    Returns ASCII string.
    '''

    if sys.version_info[0] < 3:
        unicode_string = unicode(binary_string, 'utf-8')
    else:
        unicode_string = binary_string
    normalized_unicode_string = unicodedata.normalize('NFKD', unicode_string)
    ascii_string = normalized_unicode_string.encode('ascii', 'ignore')

    if sys.version_info[0] < 3:
        return ascii_string
    else:
        return ascii_string.decode('utf-8')

