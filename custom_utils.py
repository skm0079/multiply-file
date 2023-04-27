import random
import string

from faker import Faker

faker = Faker('en_IN')  # Set the Faker instance to generate data for India

def generate_random_string(target_item, custom_length=7, has_alphabet=False, has_special_characters=False, blank=False):
    """
    Generate a random string based on the given criteria.

    Args:
        target_item (str or int): The target item for which the random string is being generated.
        custom_length (int): The length of the output string. Default is 7.
        has_alphabet (bool): Whether the output string should include alphabets. Default is False.
        has_special_characters (bool): Whether the output string should include special characters. Default is False.
        blank (bool): Whether the output string should be blank. Default is False.
    
    Returns:
        str: The generated random string based on the given criteria.
    """
    try:
        # print(f"target_item: {target_item}")
        # Convert target_item to string if it's not already
        target_item = str(target_item)
        
        if blank:
            return "       "
        
        # Check if the target_item is a number and less than the custom_length
        if target_item.isnumeric() and len(target_item) < custom_length:
            # If the target_item is a number, append or prepend alphabet if has_alphabet is True
            if has_alphabet:
                alphabet = string.ascii_letters
                target_item = target_item.zfill(custom_length - 1)
                target_item += random.choice(alphabet)
            else:
                target_item = target_item.zfill(custom_length)
        elif target_item.isnumeric() and len(target_item) >= custom_length:
                if has_alphabet:
                    target_item = replace_random_chars_with_letters(target_item)
                if has_special_characters:
                    target_item = replace_random_chars_with_punctuations(target_item)
                else:
                    target_item = target_item.zfill(custom_length)
        else:
            # If the target_item is a string, append or prepend both number or string
            characters = string.digits
            if has_alphabet:
                characters += string.ascii_letters
            if has_special_characters:
                characters += string.punctuation
                
            target_length = custom_length - len(target_item)
            if target_length > 0:
                target_item += ''.join(random.choices(characters, k=target_length))
            elif target_length < 0:
                target_item = target_item[:custom_length]
        print(f"Return from Randomizer: {target_item}")
        return target_item
    
    except Exception as e:
        # Handle any exceptions and return None
        print(f"Error generating random string: {str(e)}")
        return None

# Generate a random Indian bank account number of a given length
def generate_account_number(length=12):
    account_number = ''
    while len(account_number) < length:
        account_number += str(faker.random_digit())
    return account_number[:length]


def replace_random_chars_with_letters(input_string):
    # Convert input string to list for in-place modification
    output_list = list(input_string)
    
    # Get indices of characters to replace
    indices = random.sample(range(len(output_list)), random.randint(1, len(output_list)))
    
    # Replace characters at the chosen indices with random letters
    for index in indices:
        output_list[index] = random.choice(string.ascii_uppercase)
    
    # Convert list back to string and return
    return ''.join(output_list)

def replace_random_chars_with_punctuations(input_string):
    # Convert input string to list for in-place modification
    output_list = list(input_string)
    
    # Get indices of characters to replace
    indices = random.sample(range(len(output_list)), random.randint(1, len(output_list)))
    
    # Replace characters at the chosen indices with random punctuation characters
    for index in indices:
        output_list[index] = random.choice(string.punctuation)
    
    # Convert list back to string and return
    return ''.join(output_list)
