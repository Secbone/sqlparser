COMMON = [
    'SELECT',
    'UPDATE',
    'INSERT',
    'DELETE',
    'FROM',
    'WHERE',
    'ON',
    'IN',
    'AS',
    'DISTINCT',
]

COMPOSITE = {
    'LEFT': ['JOIN'],
    'RIGHT': ['JOIN'],
    'INNER': ['JOIN'],
    'JOIN': None,
    'ORDER': ['BY'],
    'GROUP': ['BY'],
    'BY': None,
}