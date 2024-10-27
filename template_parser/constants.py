import re 

DATA_TYPES = {
    'STRING': 'str',
    'INTEGER': 'int',
    'FLOAT': 'float',
    'URL': 'url',
    'DATE': 'date',
    'CURRENCY': 'currency'
}

PLACEHOLDER_PATTERN = re.compile(
    r'<(?P<name>\w+)(:(?P<type>\w+))?(?P<options>(\|[^>]+)?)>'
)