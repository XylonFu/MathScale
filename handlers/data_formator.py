import json
import os


def merge_json_files(input_dir, output_file):
    merged_data = []
    id_counter = 1  # Initialize a counter for unique IDs

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            item['id'] = id_counter
                            merged_data.append(item)
                            id_counter += 1
                    elif isinstance(data, dict):
                        data['id'] = id_counter
                        merged_data.append(data)
                        id_counter += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)


# Define the input directory and the output file path
input_directory = '../files/MATH/train'
output_file_path = '../files/MATH.json'

# Call the function to merge JSON files
merge_json_files(input_directory, output_file_path)
