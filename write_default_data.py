import ruamel.yaml

# Load the data from default.yaml and input.yaml
with open('config/default.yaml', 'r') as file:
    default_yaml_data = ruamel.yaml.safe_load(file)

with open('config/input.yaml', 'r') as file:
    input_yaml_data = ruamel.yaml.round_trip_load(file)

# Get the values from sbi-1 in default.yaml
default_data = default_yaml_data.get(input_yaml_data['file_name'])
# Update the default key in input.yaml with the values from sbi-1
input_yaml_data['default'].update(default_data)

# Write the updated data to input.yaml while preserving comments
with open('config/input.yaml', 'w') as file:
    ruamel.yaml.round_trip_dump(input_yaml_data, file)
