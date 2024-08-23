import yaml

'''
Main function is to give the user a choice between using the default config file or provide their own to parse.
Repeats until a valid file is provided.
'''
def main():

    choice = input("A config is needed to run this application. You have an option to use either your own custom config file or use the default config file. Type y or yes to use the default config otherwise you will be prompted to enter a valid config file (y/n): ").strip().lower()
    
    if choice in ('y', 'yes'):
        result, isFileValid = process_file("config.yaml")
        if isFileValid:
            return result
        else:
            print("Error: Unable to load default config file. Exiting.")
            return None
        
    else:
        while True:

            # Prompt user for file name, stripping any leading/trailing whitespace.
            file_name = input("Enter file name: ").strip()

            # Call the function to process the file and check if it is valid.
            result, isFileValid = process_file(file_name)

            # If the file is valid, return its contents and exit the loop.
            if isFileValid:
                return result

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