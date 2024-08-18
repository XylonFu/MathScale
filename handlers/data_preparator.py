import json
import os
import random

import pandas as pd

from prompt import MATH_EXTRACTION_PROMPT, question_types, difficulty_levels, MATH_GENERATION_PROMPT
from utils.graph_algorithm import build_concept_graph, random_walk_sampling


def construct_math_extraction_messages(num=100):
    parquet_file = 'files/GSM8K.parquet'
    extraction_file = 'files/math_extraction.json'

    df = pd.read_parquet(parquet_file).head(num)

    if os.path.exists(extraction_file):
        with open(extraction_file, 'r', encoding='utf-8') as ex_file:
            processed_data = json.load(ex_file)
            processed_ids = {item['id'] for item in processed_data}
            existing_count = len(processed_data)
    else:
        processed_ids = set()
        existing_count = 0

    num_to_generate = num - existing_count
    if num_to_generate <= 0:
        print(f"Math Extraction: Already have {existing_count} messages, no new messages generated.")
        return [], []

    messages_list = []
    metadata_list = []

    for index, row in df.iterrows():
        row_id = index
        if row_id in processed_ids:
            continue

        question = row['question']
        answer = row['answer']
        prompt = MATH_EXTRACTION_PROMPT.format(question=question)
        messages_list.append([{"role": "user", "content": prompt}])
        metadata_list.append({"question": question, "answer": answer, "id": row_id})

        if len(messages_list) >= num_to_generate:
            break

    return messages_list, metadata_list


def construct_math_generation_messages(num=100):
    extraction_file = 'files/math_extraction.json'
    generation_file = 'files/math_generation.json'

    if os.path.exists(extraction_file):
        with open(extraction_file, 'r', encoding='utf-8') as ex_file:
            extraction_data = json.load(ex_file)
    else:
        print("No extraction data found. Please run math_extraction.py first.")
        exit()

    if os.path.exists(generation_file):
        with open(generation_file, 'r', encoding='utf-8') as gen_file:
            existing_data = json.load(gen_file)
            existing_count = len(existing_data)
    else:
        existing_count = 0

    num_to_generate = num - existing_count
    if num_to_generate <= 0:
        print(f"Math Generation: Already have {existing_count} messages, no new messages generated.")
        return [], []

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
            continue

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

    return messages_list, metadata_list
