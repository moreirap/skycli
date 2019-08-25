from datetime import datetime
from click.types import ParamType

class SkyScannerDateTime(ParamType):
    """The SkyScannerDateTime type converts date strings into tuples (format, `datetime`) objects.

    The format strings which are checked are YYYY-MM-DD, YYYY-MM, HH:MM or the string 'anytime'.

    Parsing is tried using each format, in order, and the first format which
    parses successfully is used.

    :param formats: A list or tuple of date format strings, in the order in
                    which they should be tried. Defaults to
                    ``'%Y-%m-%d'``, ``'%Y-%m'``,``'%H:%M'`` or ``'anytime'``.
    """
    name = 'SkyScannerDateTime'

    def __init__(self, formats=None):
        self.formats = formats or [
            '%Y-%m-%d',
            '%Y-%m',
            '%H:%M'
        ]

    def get_metavar(self, param):
        return '[{} or ''anytime'']'.format('|'.join(self.formats))

    def _try_to_convert_date(self, value, format):
        try:
            return datetime.strptime(value, format)
        except ValueError:
            return None

    def convert(self, value, param, ctx):
        # Matching with 'anytime'
        if value != None and value.strip().lower() == 'anytime':
            return 'anytime'
        
        # Exact match
        for format in self.formats:
            dtime = self._try_to_convert_date(value, format)
            if dtime:
                return value

        self.fail(
            'invalid SkyScannerDateTime format: {}. (choose from {} or \'anytime\')'.format(value, ', '.join(self.formats)))

    def __repr__(self):
        return 'SkyScannerDateTime'
