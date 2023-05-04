from pprint import pprint
from custom_utils import execute_query


def get_random_bank():
    response = execute_query('SELECT ID, BANK, IFSC, MICR, BRANCH, CITY FROM banks ORDER BY RAND() LIMIT 1;')
    pprint(response[0])
    return response

get_random_bank()