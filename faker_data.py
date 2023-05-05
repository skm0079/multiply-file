import random
import yaml
import ruamel.yaml
import csv
import re
from faker import Faker
from custom_utils import execute_query, generate_account_number, generate_ifsc, generate_random_string

# 'en_IN'for Indian Names
fake = Faker('en_IN')

# Load the data from default.yaml and input.yaml
with open('config/default.yaml', 'r') as file:
    default_data = ruamel.yaml.safe_load(file)

# Open and read the YAML file
with open('config/input.yaml') as yaml_file:
    input_data = yaml.safe_load(yaml_file)




# Function to generate random bank detail and set the Values

def get_random_bank():
    response = execute_query('SELECT ID, BANK, IFSC, MICR, BRANCH, CITY FROM banks ORDER BY RAND() LIMIT 1;')
    # Working Bank Values
    query_data = {
        "BANK_ID" : response[0][0],
        "BANK_NAME" :response[0][1],
        "BANK_IFSC" :response[0][2],
        "BANK_MICR" :response[0][3],
        "BANK_BRANCH" :response[0][4],
        "BANK_CITY" :response[0][5]
    }
    return query_data

# Function to validate account holder name field
def validate_account_holder_name(case, length, gap, dot, title):
    # Validation rules go here
    if case == 'small':
        name = fake.name().lower()
    elif case == 'capital':
        name = fake.name().upper()
    else:
        name = fake.name().capitalize()
    
    if length == 'short':
        name = name[:3]
    elif length == 'long':
        name = name[:25]
    
    if gap:
        name = name.replace(' ', '')
    
    if dot:
        name = name.replace(' ', '.')
    
    if title:
        name_parts = name.split(' ')
        if len(name_parts) > 1:
            name = ' '.join(name_parts[1:])
    
    if not case and not length and not gap and not dot and not title:
        return fake.name()

    return name

# TODO: Function to validate address field
def validate_address(address_line='single', wrong_state=False, pincode_length=5, has_pincode=True, no_gap_address=False):
     # Generate the address line based on the input parameter
     # This Logic is Only valid for default Locale
    if address_line == 'single':
        address = fake.street_address().replace('\n', ', ')
    elif address_line == 'double':
        address = f"{fake.secondary_address()} {fake.street_address()}"
    elif address_line == 'three':
        address = f"{fake.building_number()} {fake.street_name()}{fake.secondary_address()}"
    elif address_line == 'four':
        address = f"{fake.building_number()} {fake.street_name()}{fake.secondary_address()}{fake.street_suffix()}"
    else:
        address = fake.address()

    # Generate the state name, potentially with a wrong name if the input parameter is True
    if wrong_state:
        state = fake.state()
    else:
        state = fake.state()

    # Generate a pincode of length 5
    pincode = fake.postcode()[:pincode_length]

    # Format the address data as a string and return it
    # Adjust for Pincode True or False
    if has_pincode:
        address_data = f"{address}{state}, {pincode}"
    else:
        address_data = f"{address}{state}"
    
    # print(re.sub(r"[\n\t\s]*", "", address_data))

    if no_gap_address:
        address = re.sub(r"[\n\t\s]*", "", address_data)
    else:
        address = address_data

    return address


# Function to validate IFSC code field
def validate_ifsc_code(target_value, case="default"):
    # input_data['ifsc_code']['ifsc_code_length'][0]
    # Validation rules go here

    ifsc_code_length = input_data['ifsc_code']['ifsc_code_length'][0]
    has_alphabet = input_data['ifsc_code']['has_alphabet'][0]
    has_special_characters = input_data['ifsc_code']['has_special_characters'][0]
    blank = input_data['ifsc_code']['blank'][0]

    validated_ifsc_code = target_value

    if case == 'default':
        return validated_ifsc_code
    elif case == 'ifsc_code_length':
        validated_ifsc_code = generate_random_string(target_item=target_value,custom_length=ifsc_code_length,has_alphabet=False,has_special_characters=False,blank=False)
    elif case == 'has_alphabet':
        validated_ifsc_code = generate_random_string(target_item=target_value,custom_length=ifsc_code_length,has_alphabet=True,has_special_characters=False,blank=False)
    elif case == 'has_special_characters':
        validated_ifsc_code = generate_random_string(target_item=target_value,custom_length=ifsc_code_length,has_alphabet=False,has_special_characters=True,blank=False)
    elif case == 'blank':
        validated_ifsc_code = generate_random_string(target_item=target_value,custom_length=ifsc_code_length,has_alphabet=False,has_special_characters=False,blank=True)
    elif case == 'faulty':
        validated_ifsc_code = fake.swift(length=ifsc_code_length)
    return validated_ifsc_code

# Function to validate MICR code field
def validate_micr_code():
    # Validation rules go here
    return fake.msisdn()

# Function to validate branch name field
def validate_branch_name():
    # Validation rules go here
    return fake.company()

# Function to validate branch name field
def validate_account_number(target_value, case="default"):
    # Default input values in yaml
    account_number_length = input_data['account_number']['account_number_length'][0]
    has_alphabet = input_data['account_number']['has_alphabet'][0]
    has_special_characters = input_data['account_number']['has_special_characters'][0]
    blank = input_data['account_number']['blank'][0]

    # Validated Return Value
    validated_account_number = target_value
    # print(f"validated_account_number: {validated_account_number}")
    # Validation rules go here
    if case == 'default':
        return validated_account_number
    elif case == 'account_number_length':
        validated_account_number = generate_random_string(target_item=target_value,custom_length=account_number_length,has_alphabet=False,has_special_characters=False,blank=False)
    elif case == 'has_alphabet':
        validated_account_number = generate_random_string(target_item=target_value,custom_length=account_number_length,has_alphabet=True,has_special_characters=False,blank=False)
    elif case == 'has_special_characters':
        validated_account_number = generate_random_string(target_item=target_value,custom_length=account_number_length,has_alphabet=False,has_special_characters=True,blank=False)
    elif case == 'blank':
        validated_account_number = generate_random_string(target_item=target_value,custom_length=account_number_length,has_alphabet=False,has_special_characters=False,blank=True)
    return validated_account_number

# Function to validate account type field
def validate_account_type():
    # Validation rules go here
    return fake.word(ext_word_list=['Savings', 'Regular', 'Current','Joint','Salary','RD','Company'])

# Function to generate random opening balance
def generate_opening_balance(target_value, case="default",start=1000, end=10000):

    vaidated_opening_balance = random.randint(start, end)

    start_range = input_data['opening_balance']['start_range']
    end_range = input_data['opening_balance']['end_range']
    has_alphabet = input_data['opening_balance']['has_alphabet'][0]
    has_special_characters = input_data['opening_balance']['has_special_characters'][0]
    blank = input_data['opening_balance']['blank'][0]

    if case == 'default':
        return vaidated_opening_balance
    elif case == 'account_number_length':
        vaidated_opening_balance = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=False,blank=False)
    elif case == 'has_alphabet':
        vaidated_opening_balance = generate_random_string(target_item=target_value,has_alphabet=True,has_special_characters=False,blank=False)
    elif case == 'has_special_characters':
        vaidated_opening_balance = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=True,blank=False)
    elif case == 'blank':
        vaidated_opening_balance = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=False,blank=True)
    return random.randint(start_range, end_range)

# Function to generate random closing balance
def generate_closing_balance(target_value, case="default",start=1000, end=10000):

    vaidated_closing_balance = random.randint(start, end)

    start_range = input_data['closing_balance']['start_range']
    end_range = input_data['closing_balance']['end_range']
    has_alphabet = input_data['closing_balance']['has_alphabet'][0]
    has_special_characters = input_data['closing_balance']['has_special_characters'][0]
    blank = input_data['closing_balance']['blank'][0]

    if case == 'default':
        return vaidated_closing_balance
    elif case == 'account_number_length':
        vaidated_closing_balance = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=False,blank=False)
    elif case == 'has_alphabet':
        vaidated_closing_balance = generate_random_string(target_item=target_value,has_alphabet=True,has_special_characters=False,blank=False)
    elif case == 'has_special_characters':
        vaidated_closing_balance = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=True,blank=False)
    elif case == 'blank':
        vaidated_closing_balance = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=False,blank=True)
    return random.randint(start_range, end_range)


# Function to generate random debit amount
def generate_debit(target_value, case="default",start=1000, end=10000):

    vaidated_debit = random.randint(start, end)

    start_range = input_data['debit']['start_range']
    end_range = input_data['debit']['end_range']
    has_alphabet = input_data['debit']['has_alphabet'][0]
    has_special_characters = input_data['debit']['has_special_characters'][0]
    blank = input_data['debit']['blank'][0]
    if case == 'default':
        return vaidated_debit
    elif case == 'account_number_length':
        vaidated_debit = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=False,blank=False)
    elif case == 'has_alphabet':
        vaidated_debit = generate_random_string(target_item=target_value,has_alphabet=True,has_special_characters=False,blank=False)
    elif case == 'has_special_characters':
        vaidated_debit = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=True,blank=False)
    elif case == 'blank':
        vaidated_debit = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=False,blank=True)

    return vaidated_debit

# Function to generate random credit amount
def generate_credit(target_value, case="default",start=1000, end=10000):

    vaidated_credit = random.randint(start, end)   

    start_range = input_data['credit']['start_range']
    end_range = input_data['credit']['end_range']
    has_alphabet = input_data['credit']['has_alphabet'][0]
    has_special_characters = input_data['credit']['has_special_characters'][0]
    blank = input_data['credit']['blank'][0]
    if case == 'default':
        return vaidated_credit
    elif case == 'account_number_length':
        vaidated_credit = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=False,blank=False)
    elif case == 'has_alphabet':
        vaidated_credit = generate_random_string(target_item=target_value,has_alphabet=True,has_special_characters=False,blank=False)
    elif case == 'has_special_characters':
        vaidated_credit = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=True,blank=False)
    elif case == 'blank':
        vaidated_credit = generate_random_string(target_item=target_value,has_alphabet=False,has_special_characters=False,blank=True)

    return vaidated_credit

# Function to generate random date
def generate_date():
    return fake.date_between(start_date='-1y', end_date='today')

# Function to generate total balance
def calculate_total_balance(opening_balance, closing_balance, debit, credit):
    if all(isinstance(n, (int, float)) for n in [opening_balance, closing_balance, debit, credit]):
        return opening_balance + credit - debit + closing_balance
    else:
        return random.uniform(0, 100)

# Ask user for number of rows to generate
num_rows = input_data['number_of_rows']

# ACCOUNT HOLDER NAME MODIFICATION SETTINGS
# How many account holder names should be in small letters?
num_small_names = input_data['account_holder_name']['small_names']
# How many account holder names should be in capital letters?
num_capital_names = input_data['account_holder_name']['capital_names']
# How many account holder names should have only 3 letters?
num_short_names = input_data['account_holder_name']['short_names']
# How many account holder names should have 25 letters?
num_long_names = input_data['account_holder_name']['long_names']
# How many account holder names should not have gaps?
num_no_gap_names = input_data['account_holder_name']['no_gap_names']
# How many account holder names should have dots between the names?
num_dot_names = input_data['account_holder_name']['dot_names']
# How many account holder names should not have a title?
num_no_title_names = input_data['account_holder_name']['no_title_names']

BANK_DETAILS = get_random_bank()

# Generate CSV file with random data
with open(f"excel_sheets/{input_data['file_name']}_accounts.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['account_holder_name', 'address', 'ifsc_code', 'micr_code', 'branch_name', 'account_type', 'account_number', 'opening_balance', 'closing_balance', 'debit', 'credit', 'date', 'total_balance'])

    for i in range(num_rows):
        if 'account_holder_name' in input_data['target_field']:
                    if num_small_names > 0:
                        account_holder_name = validate_account_holder_name('small', '', '', '', '')
                        num_small_names -= 1
                    elif num_capital_names > 0:
                        account_holder_name = validate_account_holder_name('capital', '', '', '', '')
                        num_capital_names -= 1
                    elif num_short_names > 0:
                        account_holder_name = validate_account_holder_name('', 'short', '', '', '')
                        num_short_names -= 1
                    elif num_long_names > 0:
                        account_holder_name = validate_account_holder_name('', 'long', '', '', '')
                        num_long_names -= 1
                    elif num_no_gap_names > 0:
                        account_holder_name = validate_account_holder_name('', '', True, '', '')
                        num_no_gap_names -= 1
                    elif num_dot_names > 0:
                        account_holder_name = validate_account_holder_name('', '', '', True, '')
                        num_dot_names -= 1
                    elif num_no_title_names > 0:
                        account_holder_name = validate_account_holder_name('', '', '', '', True)
                        num_no_title_names -= 1
                    else:
                        account_holder_name = validate_account_holder_name('', '', '', '', '')
        else:
            account_holder_name = input_data['default']['account_holder_name']

        if 'address' in input_data['target_field']:
            address = validate_address(address_line=input_data['address']['address_line'], wrong_state=input_data['address']['wrong_state'],pincode_length=input_data['address']['pincode_length'],has_pincode=input_data['address']['has_pincode'])
        else:
            address = input_data['default']['address']

        if 'ifsc_code' in input_data['target_field']:
            # ifsc_code = validate_ifsc_code()
            base_ifsc_code= BANK_DETAILS['BANK_IFSC']
            if input_data['ifsc_code']['ifsc_code_length'][2] > 0 and input_data['ifsc_code']['ifsc_code_length'][0]:
                ifsc_code= validate_ifsc_code(base_ifsc_code, 'ifsc_code_length')
                input_data['ifsc_code']['ifsc_code_length'][1] -= 1
            elif input_data['ifsc_code']['has_alphabet'][1] > 0 and input_data['ifsc_code']['has_alphabet'][0]:
                ifsc_code= validate_ifsc_code(base_ifsc_code, 'has_alphabet')
                input_data['ifsc_code']['has_alphabet'][1] -= 1
            elif input_data['ifsc_code']['has_special_characters'][1] > 0 and input_data['ifsc_code']['has_special_characters'][0]:
                ifsc_code= validate_ifsc_code(base_ifsc_code, 'has_special_characters')
                input_data['ifsc_code']['has_special_characters'][1] -= 1
            elif input_data['ifsc_code']['blank'][1] > 0 and input_data['ifsc_code']['blank'][0]:
                ifsc_code= validate_ifsc_code(base_ifsc_code, 'blank')
                input_data['ifsc_code']['blank'][1] -= 1
            elif input_data['ifsc_code']['normal'][1] > 0 and input_data['ifsc_code']['normal'][0]:
                ifsc_code= validate_ifsc_code(base_ifsc_code, 'default')
                input_data['ifsc_code']['normal'][1] -= 1
            elif input_data['ifsc_code']['faulty'][1] > 0 and input_data['ifsc_code']['faulty'][0]:
                ifsc_code= validate_ifsc_code(base_ifsc_code, 'faulty')
                input_data['ifsc_code']['faulty'][1] -= 1
            else:
                ifsc_code= validate_ifsc_code(base_ifsc_code, 'other')
        else:
            ifsc_code = input_data['default']['ifsc_code']
        
        if 'micr_code' in input_data['target_field']:
            micr_code = BANK_DETAILS['BANK_MICR']
        else:
            micr_code = input_data['default']['micr_code']
        
        if 'branch_name' in input_data['target_field']:
            branch_name = BANK_DETAILS['BANK_BRANCH']
        else:
            branch_name = input_data['default']['branch_name']
        
        if 'account_type' in input_data['target_field']:
            account_type = validate_account_type()
        else:
            account_type = input_data['default']['account_type']

        # Logic for Account Number
        if 'account_number' in input_data['target_field']:
            # Generate base account number
            base_account_number = generate_account_number(BANK_DETAILS['BANK_IFSC'],BANK_DETAILS['BANK_MICR'],BANK_DETAILS['BANK_NAME'],BANK_DETAILS['BANK_BRANCH'],input_data['account_number']['account_number_length'][0])
            # print(f"base_account_number {base_account_number}")
            if input_data['account_number']['account_number_length'][1] > 0 and input_data['account_number']['account_number_length'][1]:
                account_number = validate_account_number(base_account_number, 'account_number_length')
                input_data['account_number']['account_number_length'][1] -= 1
            elif input_data['account_number']['has_alphabet'][1] > 0 and input_data['account_number']['has_alphabet'][1]:
                account_number = validate_account_number(base_account_number, 'has_alphabet')
                input_data['account_number']['has_alphabet'][1] -= 1
            elif input_data['account_number']['has_special_characters'][1] > 0 and input_data['account_number']['has_special_characters'][1]:
                account_number = validate_account_number(base_account_number, 'has_special_characters')
                input_data['account_number']['has_special_characters'][1] -= 1
            elif input_data['account_number']['blank'][1] > 0 and input_data['account_number']['blank'][1]:
                account_number = validate_account_number(base_account_number, 'blank')
                input_data['account_number']['blank'][1] -= 1
            elif input_data['account_number']['normal'][1] > 0 and input_data['account_number']['normal'][1]:
                account_number = validate_account_number(base_account_number, 'default')
                input_data['account_number']['normal'][1] -= 1
            else:
                account_number = validate_account_number(base_account_number, 'other')
        else:
            account_number = input_data['default']['account_number']
        
        if 'opening_balance' in input_data['target_field']:
            start_range = input_data['opening_balance']['start_range']
            end_range = input_data['opening_balance']['end_range']
            base_opening_balance = random.randint(start_range,end_range)
            if input_data['opening_balance']['has_alphabet'][1] > 0 and input_data['opening_balance']['has_alphabet'][1]:
                opening_balance = generate_opening_balance(base_opening_balance, 'has_alphabet',start_range,end_range)
                input_data['opening_balance']['has_alphabet'][1] -= 1
            elif input_data['opening_balance']['has_special_characters'][1] > 0 and input_data['opening_balance']['has_special_characters'][1]:
                opening_balance = generate_opening_balance(base_opening_balance, 'has_special_characters',start_range,end_range)
                input_data['opening_balance']['has_special_characters'][1] -= 1
            elif input_data['opening_balance']['blank'][1] > 0 and input_data['opening_balance']['blank'][1]:
                opening_balance = generate_opening_balance(base_opening_balance, 'blank',start_range,end_range)
                input_data['opening_balance']['blank'][1] -= 1
        else:
            opening_balance = input_data['default']['opening_balance']
        
        if 'closing_balance' in input_data['target_field']:
            start_range = input_data['closing_balance']['start_range']
            end_range = input_data['closing_balance']['end_range']
            base_closing_balance = random.randint(start_range,end_range)

            if input_data['closing_balance']['has_alphabet'][1] > 0 and input_data['closing_balance']['has_alphabet'][1]:
                closing_balance = generate_closing_balance(base_closing_balance, 'has_alphabet',start_range,end_range)
                input_data['closing_balance']['has_alphabet'][1] -= 1
            elif input_data['closing_balance']['has_special_characters'][1] > 0 and input_data['closing_balance']['has_special_characters'][1]:
                closing_balance = generate_closing_balance(base_closing_balance, 'has_special_characters',start_range,end_range)
                input_data['closing_balance']['has_special_characters'][1] -= 1
            elif input_data['closing_balance']['blank'][1] > 0 and input_data['closing_balance']['blank'][1]:
                closing_balance = generate_closing_balance(base_closing_balance, 'blank',start_range,end_range)
                input_data['closing_balance']['blank'][1] -= 1
        else:
            closing_balance = input_data['default']['closing_balance']
        
        if 'debit' in input_data['target_field']:
            start_range = input_data['debit']['start_range']
            end_range = input_data['debit']['end_range']
            base_debit = random.randint(start_range,end_range)

            if input_data['debit']['has_alphabet'][1] > 0 and input_data['debit']['has_alphabet'][1]:
                debit = generate_debit(base_debit, 'has_alphabet',start_range,end_range)
                input_data['debit']['has_alphabet'][1] -= 1
            elif input_data['debit']['has_special_characters'][1] > 0 and input_data['debit']['has_special_characters'][1]:
                debit = generate_debit(base_debit, 'has_special_characters',start_range,end_range)
                input_data['debit']['has_special_characters'][1] -= 1
            elif input_data['debit']['blank'][1] > 0 and input_data['debit']['blank'][1]:
                debit = generate_debit(base_debit, 'blank',start_range,end_range)
                input_data['debit']['blank'][1] -= 1
        else:
            debit = input_data['default']['debit']
        
        if 'credit' in input_data['target_field']:
            start_range = input_data['credit']['start_range']
            end_range = input_data['credit']['end_range']
            base_credit = random.randint(start_range,end_range)

            if input_data['credit']['has_alphabet'][1] > 0 and input_data['credit']['has_alphabet'][1]:
                credit = generate_credit(base_credit, 'has_alphabet',start_range,end_range)
                input_data['credit']['has_alphabet'][1] -= 1
            elif input_data['credit']['has_special_characters'][1] > 0 and input_data['credit']['has_special_characters'][1]:
                credit = generate_credit(base_credit, 'has_special_characters',start_range,end_range)
                input_data['credit']['has_special_characters'][1] -= 1
            elif input_data['credit']['blank'][1] > 0 and input_data['credit']['blank'][1]:
                credit = generate_credit(base_credit, 'blank',start_range,end_range)
                input_data['credit']['blank'][1] -= 1
        else:
            credit = input_data['default']['credit']
        
        if 'date' in input_data['target_field']:
            date = generate_date()
        else:
            date = input_data['default']['date']
        
        if 'total_balance' in input_data['target_field']:
            total_balance = calculate_total_balance(opening_balance, closing_balance, debit, credit)
        else:
            total_balance = input_data['default']['total_balance']
        
        writer.writerow([account_holder_name, address, ifsc_code, micr_code, branch_name, account_type, account_number, opening_balance, closing_balance, debit, credit, date, total_balance])
