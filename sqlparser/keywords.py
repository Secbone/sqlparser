T_COLUMN = 1
T_TABLE = 2

COMMON = {
    'SELECT': T_COLUMN,
    'UPDATE': T_COLUMN,
    'INSERT': T_TABLE,
    'DELETE': T_COLUMN,
    'FROM': T_TABLE,
    'WHERE': T_COLUMN,
    'ON': T_COLUMN,
    'IN': T_COLUMN,
    'AS': T_COLUMN,
    'DISTINCT': T_COLUMN,
}

COMPOSITE = {
    'LEFT': ['JOIN'],
    'RIGHT': ['JOIN'],
    'INNER': ['JOIN'],
    'JOIN': None,
    'ORDER': ['BY'],
    'GROUP': ['BY'],
    'BY': None,
}