import yaml
import socket

'''
Main function is to give the user a choice between using the default config file or provide their own to parse.
Repeats until a valid file is provided.
'''
def main():

    result, isFileValid = process_file("config.yaml")
    if isFileValid:
        return result
    else:
        print("Error: Unable to load default config file. Exiting.")
        return None

def delete_destination(config, destination, config_file):

    for item in config['destinations']:
        if destination == item['destination']:
            config['destinations'].remove(item)
            save_config(config, config_file)
            print(f'Destination {destination} have been deleted.')
            break
    else:
        print(f'Destination {destination} not found.')

def update_interval(config, interval, config_file):

    validated_interval = check_value(interval)

    if validated_interval:
        config['interval'] = validated_interval
        save_config(config, config_file)
        print(f'Time delay interval updated to {validated_interval}.')
    else:
        print(f'Invalid interval: {interval}. Interval not updated.')

def add_destination(config, destination, count, config_file):

    validated_destination = check_destination(destination.strip())
    validated_count = check_value(count)

    if validated_destination and validated_count:
        if 'destinations' not in config:
            config['destinations'] = []
        
        for item in config['destinations']:
            if item['destination'] == validated_destination:
                item['count'] = validated_count
                save_config(config, config_file)
                print(f'Destination {validated_destination} already exists. Updating count to {validated_count}.')
                return 
        
        config['destinations'].append({
            'destination': validated_destination,
            'count': validated_count
        })
        save_config(config, config_file)
        print(f'Added destination {validated_destination} with count {validated_count}.')
    else:
        print("Invalid destination or count. Destination not added.")

def save_config(config, fileName):

    with open(fileName, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    print(f'Configuration saved to {fileName}.')

def load_config(config):

    result, isFileValid = process_file(config)

    if isFileValid:
        return result
    else:
        print("Error: Unable to load default config file. Exiting.")
        return None



'''
Process the given file name to read and parse the YAML content.
Mainly used for exception handling.

Arguments: process_file(str): The name of the file to process.

Returns: (contents, isFileValid): where content is the parsed YAML data or None, and isFileValid is a boolean.
'''
def process_file(fileName):

    # Check if the file name is empty.
    if not fileName:
        print('Error: File name cannot be empty. Please try again.')
        return None, False
    
    try:
        # Call yaml_reader() function to read file name and parse its content. Or throw an exception if error occurs.
        result = yaml_reader(fileName)
        return result, True
    except FileNotFoundError:
        print(f'Error: File not found.\nError translation: The file "{fileName}" was not found. Please ensure the file name and extension are correct and try again.')
    except yaml.parser.ParserError:
        print(f'Error: Parsing error.\nError translation: The file "{fileName}" has syntactical error(s). Please ensure there are no missing "," or "}}" characters and try again.')
    except PermissionError:
        print(f'Error: Permission denied.\nError translation: You do not have permission to read the file "{fileName}". Please check your file\'s permission settings and try again.')
    except yaml.scanner.ScannerError:
        print(f'Error: Scanning error.\nError translation: The file "{fileName}" contains illegal characters or incorrect indentation. Please proof-read the file\'s content and try again.')
    except yaml.YAMLError:
        print(f'Error: YAML error.\nError translation: An error occurred while processing the YAML file "{fileName}".')
    except OSError:
        print(f'Error: Invalid file name.\nError translation: The file name "{fileName}" contains invalid characters or is not allowed. Please use a valid file name and try again.')
    return None, False

def check_value(value):

    try:
        if value <= 0:
            print("Error: The input value must be a positive integer.")
            return None
        else:
            return value
    except ValueError:
        print("Error: Invalid input. Please enter a positive integer.")
        return None
    except Exception:
        print("An unexpected error has occurred")
        return None
    
def check_destination(destination):

    try:
        print("Fetching...")
        if not destination:
            raise ValueError("The destination address cannot be empty. Please enter a valid hostname or IP address.")
        socket.gethostbyname(destination)
        return destination
    except ValueError as e:
        print(f'Error: {e}')
        return None
    except socket.gaierror:
        print(f'Error: Invalid destination. Either {destination} does not exist or is mistyped. Please enter a valid hostname or IP address and try again.')
        return None
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')
        return None

'''
Reads and parses the YAML file content.
Returns parsed YAML content.
'''
def yaml_reader(fileName):

    with open(fileName, 'r') as file:
        return yaml.safe_load(file)

# Execute main directly and not when imported in a different file.  
if __name__ == "__main__":
    
    main()