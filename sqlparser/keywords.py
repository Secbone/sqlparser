T_COLUMN = 1
T_TABLE = 2

COMMON = {
    'SELECT': T_COLUMN,
    'UPDATE': T_TABLE,
    'INSERT INTO': T_TABLE,
    'DELETE': T_COLUMN,
    'FROM': T_TABLE,
    'WHERE': T_COLUMN,
    'ON': T_COLUMN,
    'AS': T_COLUMN,
    'DISTINCT': T_COLUMN,
    'SET': T_COLUMN,
    'VALUES': T_COLUMN,
    'ASC': None,
    'DESC': None,
}

COMPOSITE = {
    'LEFT': ['JOIN'],
    'RIGHT': ['JOIN'],
    'INNER': ['JOIN'],
    'JOIN': None,
    'ORDER': ['BY'],
    'GROUP': ['BY'],
    'BY': None,
    'INSERT': ['INTO'],
    'INTO': None,
}

OPERATOR = {
    'AND': T_COLUMN,
    'OR': T_COLUMN,
    'IN': T_COLUMN,
    'LIKE': T_COLUMN,
    'NOT': T_COLUMN,
}