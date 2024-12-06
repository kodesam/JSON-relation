import json
import yaml
import argparse
import os

def parse_json_to_yaml(json_file_path, yaml_file_path):
    """
    Parses a JSON file and converts it into a YAML file.
    
    :param json_file_path: Path to the input JSON file.
    :param yaml_file_path: Path to the output YAML file.
    """
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Write the YAML file
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)
        
        print(f"Successfully converted '{json_file_path}' to '{yaml_file_path}'.")
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' does not exist.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert a JSON file to a YAML file.")
    parser.add_argument("input_json", help="Path to the input JSON file.")
    parser.add_argument("output_yaml", help="Path to the output YAML file.")
    args = parser.parse_args()
    
    # Validate input file path
    if not os.path.isfile(args.input_json):
        print(f"Error: Input file '{args.input_json}' does not exist.")
        return
    
    # Call the conversion function
    parse_json_to_yaml(args.input_json, args.output_yaml)

if __name__ == "__main__":
    main()