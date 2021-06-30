from enum import Enum
from Exception import WSConditionTypeException

class ConditionType(Enum):

    NUMERICAL_EQU = 1
    NUMERICAL_NEQU = 2
    NUMERICAL_LEQ = 3
    NUMERICAL_GEQ = 4
    NUMERICAL_LESS = 5
    NUMERICAL_GREATER = 6

    STRING_INCLUDE = 7
    STRING_FULL_MATCH = 8
    STRING_NOT_INCLUDE = 9
    STRING_REGEXP = 10



CT = ConditionType

OPERATOR = dict()
OPERATOR[CT.NUMERICAL_EQU] = '=='
OPERATOR[CT.NUMERICAL_NEQU] = '!='
OPERATOR[CT.NUMERICAL_LEQ] = '<='
OPERATOR[CT.NUMERICAL_GEQ] = '>='
OPERATOR[CT.NUMERICAL_LESS] = '<'
OPERATOR[CT.NUMERICAL_GREATER] = '>'
OPERATOR[CT.STRING_INCLUDE] = 'in'
OPERATOR[CT.STRING_FULL_MATCH] = '=='
OPERATOR[CT.STRING_NOT_INCLUDE] = 'not in'
OPERATOR[CT.STRING_REGEXP] = '=='

NUMBER_2_CT = dict()
NUMBER_2_CT[1] = CT.NUMERICAL_EQU
NUMBER_2_CT[2] = CT.NUMERICAL_NEQU
NUMBER_2_CT[3] = CT.NUMERICAL_LEQ
NUMBER_2_CT[4] = CT.NUMERICAL_GEQ
NUMBER_2_CT[5] = CT.NUMERICAL_LESS
NUMBER_2_CT[6] = CT.NUMERICAL_GREATER

NUMBER_2_CT[7] = CT.STRING_INCLUDE
NUMBER_2_CT[8] = CT.STRING_FULL_MATCH
NUMBER_2_CT[9] = CT.STRING_NOT_INCLUDE
NUMBER_2_CT[10] = CT.STRING_REGEXP

# request project list
def get_project_list():
    pass

# request server list
def get_server_list():
    pass

# request project info
def get_project_info():
    pass

# request project by condition

# request server by condition
def get_server_by_condition(**kwargs):
    condition_type = kwargs.get('condition_type')
    variable_side = kwargs.get('variable_side')
    condition_name = kwargs.get('condition_name')
    condition_value = kwargs.get('condition_value')
    
    if condition_type > 10 or condition_type < 1:
        raise WSConditionTypeException("Unsupported Condition Type")
    operator = OPERATOR[NUMBER_2_CT[condition_type]]
    half_condition = f'{operator} {condition_value}' if variable_side == 0 else f'{condition_value} {operator}'
    filtered_server = []
    servers = []
    for server in servers:
        condition = f'{getattr(server, condition_name)} {half_condition}' if variable_side == 0 else f'{half_condition} {getattr(server, condition_name)}'
        if eval(condition):
            filtered_server.append(server)
    return filtered_server
            

    

# request training by condition
def get_training_by_condition():
    pass

# request training info
def get_training_info():
    pass
