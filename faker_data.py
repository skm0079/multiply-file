import random
import yaml
import ruamel.yaml
import csv
import re
from faker import Faker

# 'en_IN'for Indian Names
fake = Faker('en_IN')

# Load the data from default.yaml and input.yaml
with open('config/default.yaml', 'r') as file:
    default_data = ruamel.yaml.safe_load(file)

# Open and read the YAML file
with open('config/input.yaml') as yaml_file:
    input_data = yaml.safe_load(yaml_file)

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

# Function to validate address field
def validate_address(address_line='single', wrong_state=False, pincode_length=5, has_pincode=True, no_gap_address=False):
     # Generate the address line based on the input parameter
     # This Logic is Only valid for default Locale
    if address_line == 'single':
        address = fake.street_address()
    elif address_line == 'double':
        address = f"{fake.secondary_address()} {fake.street_address()}"
    elif address_line == 'three':
        address = f"{fake.building_number()} {fake.street_name()}\n{fake.secondary_address()}"
    elif address_line == 'four':
        address = f"{fake.building_number()} {fake.street_name()}\n{fake.secondary_address()}\n{fake.street_suffix()}"
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
        address_data = f"{address}\n{state}, {pincode}"
    else:
        address_data = f"{address}\n{state}"
    
    # print(re.sub(r"[\n\t\s]*", "", address_data))

    if no_gap_address:
        address = re.sub(r"[\n\t\s]*", "", address_data)
    else:
        address = address_data

    return address


# Function to validate IFSC code field
def validate_ifsc_code():
    # Validation rules go here
    return fake.swift()

# Function to validate MICR code field
def validate_micr_code():
    # Validation rules go here
    return fake.msisdn()

# Function to validate branch name field
def validate_branch_name():
    # Validation rules go here
    return fake.company()

# Function to validate branch name field
def validate_account_number():
    # Validation rules go here
    account_number = fake.swift(length=8)
    return account_number

# Function to validate account type field
def validate_account_type():
    # Validation rules go here
    return fake.word(ext_word_list=['Savings', 'Regular', 'Current','Joint','Salary','RD','Company'])

# Function to generate random opening balance
def generate_opening_balance():
    return random.randint(1000, 10000)

# Function to generate random closing balance
def generate_closing_balance():
    return random.randint(1000, 10000)

# Function to generate random debit amount
def generate_debit():
    return random.randint(100, 1000)

# Function to generate random credit amount
def generate_credit():
    return random.randint(100, 1000)

# Function to generate random date
def generate_date():
    return fake.date_between(start_date='-1y', end_date='today')

# Function to generate total balance
def calculate_total_balance(opening_balance, closing_balance, debit, credit):
    return opening_balance + credit - debit + closing_balance

# Ask user for number of rows to generate
num_rows = input_data['number_of_rows']

# Get user modifications to account holder name

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
            ifsc_code = validate_ifsc_code()
        else:
            ifsc_code = input_data['default']['ifsc_code']
        
        if 'micr_code' in input_data['target_field']:
            micr_code = validate_micr_code()
        else:
            micr_code = input_data['default']['micr_code']
        
        if 'branch_name' in input_data['target_field']:
            branch_name = validate_branch_name()
        else:
            branch_name = input_data['default']['branch_name']
        
        if 'account_type' in input_data['target_field']:
            account_type = validate_account_type()
        else:
            account_type = input_data['default']['account_type']

        if 'account_number' in input_data['target_field']:
            account_number = validate_account_number()
        else:
            account_number = input_data['default']['account_number']
        
        if 'opening_balance' in input_data['target_field']:
            opening_balance = generate_opening_balance()
        else:
            opening_balance = input_data['default']['opening_balance']
        
        if 'closing_balance' in input_data['target_field']:
            closing_balance = generate_closing_balance()
        else:
            closing_balance = input_data['default']['closing_balance']
        
        if 'debit' in input_data['target_field']:
            debit = generate_debit()
        else:
            debit = input_data['default']['debit']
        
        if 'credit' in input_data['target_field']:
            credit = generate_credit()
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
