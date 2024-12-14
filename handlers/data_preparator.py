import json
import os
import random

import pandas as pd

from prompt import MATH_EXTRACTION_PROMPT, question_types, difficulty_levels, MATH_GENERATION_PROMPT
from utils.graph_algorithm import build_concept_graph, random_walk_sampling


# Function to construct math extraction messages
def construct_math_extraction_messages(file_path, required_fields, num=100):
    """
    General data extraction function that automatically determines the file type
    based on the file extension and generates extraction messages.

    :param file_path: Path to the data file
    :param required_fields: Dictionary specifying required fields, e.g., {'question': 'problem', 'answer': 'solution', 'id': 'id'}
    :param num: Number of data entries to extract, default is 100
    :return: List of messages and metadata
    """

    # Path to save the data file
    save_path = "files/math_extraction.json"

    # Get the file extension to determine the file type
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # Read data based on the file type
    if file_extension == '.json':
        # Read JSON file and convert it to a Python object
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif file_extension == '.csv':
        # Read CSV file and convert it to a list of dictionaries
        data = pd.read_csv(file_path).to_dict(orient='records')
    elif file_extension == '.tsv':
        # Read TSV file and convert it to a list of dictionaries
        data = pd.read_csv(file_path, sep='\t').to_dict(orient='records')
    elif file_extension == '.xlsx':
        # Read Excel file and convert it to a list of dictionaries
        data = pd.read_excel(file_path).to_dict(orient='records')
    elif file_extension == '.parquet':
        # Read Parquet file and convert it to a list of dictionaries
        data = pd.read_parquet(file_path).to_dict(orient='records')
    else:
        # If the provided file type is unsupported, raise an error
        raise ValueError(f"Unsupported file extension: {file_extension}")

    # If the save path exists, read already processed data
    if os.path.exists(save_path):
        # Open and load the already extracted data file
        with open(save_path, 'r', encoding='utf-8') as ex_file:
            processed_data = json.load(ex_file)
            processed_ids = {item['id'] for item in processed_data}  # Get the set of processed IDs
            existing_count = len(processed_data)  # Number of already processed data entries
    else:
        # If the file does not exist, initialize an empty set and set existing count to 0
        processed_ids = set()
        existing_count = 0

    # Calculate the number of new data entries to generate
    num_to_generate = num - existing_count
    if num_to_generate <= 0:
        print(f"Extraction: Already have {existing_count} messages, no new messages generated.")
        return [], []  # If existing data is sufficient, no new data is generated

    messages_list = []
    metadata_list = []

    # Iterate through the data and generate new extraction messages
    for item in data:
        item_id = item[required_fields['id']]
        if item_id in processed_ids:
            continue  # Skip already processed data

        # Extract the question and answer from the data item
        question = item[required_fields['question']]
        answer = item[required_fields['answer']]
        # Generate extraction prompt based on the question
        prompt = MATH_EXTRACTION_PROMPT.format(question=question)
        # Add the message to the message list
        messages_list.append([{"role": "user", "content": prompt}])
        # Add the metadata to the metadata list
        metadata_list.append({"question": question, "answer": answer, "id": item_id})

        if len(messages_list) >= num_to_generate:
            break  # Stop generating if the required number of data entries is reached

    # Return the generated message list and metadata list
    return messages_list, metadata_list


# Function to construct math generation messages
def construct_math_generation_messages(num=100):
    extraction_file = 'files/math_extraction.json'  # Path to the extraction data file
    generation_file = 'files/math_generation.json'  # Path to the generation data file

    # If the extraction file exists, read the extraction data
    if os.path.exists(extraction_file):
        with open(extraction_file, 'r', encoding='utf-8') as ex_file:
            extraction_data = json.load(ex_file)
    else:
        print("No extraction data found. Please run math_extraction.py first.")
        exit()  # If the extraction file does not exist, prompt and exit

    # If the generation file exists, read already generated data
    if os.path.exists(generation_file):
        with open(generation_file, 'r', encoding='utf-8') as gen_file:
            existing_data = json.load(gen_file)
            existing_count = len(existing_data)  # Number of already generated data entries
    else:
        existing_count = 0  # Initialize the count of generated entries to 0

    # Calculate the number of new data entries to generate
    num_to_generate = num - existing_count
    if num_to_generate <= 0:
        print(f"Math Generation: Already have {existing_count} messages, no new messages generated.")
        return [], []  # If existing data is sufficient, no new data is generated

    # Build a concept graph and perform random walk sampling
    graph, node_type_map = build_concept_graph(extraction_data)

    messages_list = []
    metadata_list = []

    while len(messages_list) < num_to_generate:
        start_node = random.choice(list(graph.keys()))
        sampled_nodes = random_walk_sampling(graph, node_type_map, start_node)
        selected_question_type, type_description = random.choice(list(question_types.items()))
        selected_difficulty, difficulty_description = random.choice(list(difficulty_levels.items()))

        topics = [node for node in sampled_nodes if node_type_map.get(node) == "topic"]
        knowledge_points = [node for node in sampled_nodes if node_type_map.get(node) == "knowledge_point"]

        if not topics or not knowledge_points:
            continue  # Skip if the sampling result does not have valid topics or knowledge points

        # Construct the prompt based on the generated content
        prompt = MATH_GENERATION_PROMPT.format(question_type=selected_question_type,
                                               type_description=type_description,
                                               difficulty=selected_difficulty,
                                               difficulty_description=difficulty_description,
                                               topics=', '.join(topics),
                                               knowledge_points=', '.join(knowledge_points))

        messages_list.append([{"role": "user", "content": prompt}])
        metadata_list.append({
            "topics": topics,
            "knowledge_points": knowledge_points,
            "question_type": selected_question_type,
            "difficulty": selected_difficulty
        })

    return messages_list, metadata_list  # Return the generated message list and metadata list
