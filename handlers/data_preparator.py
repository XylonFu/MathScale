import json
import os
import random

import pandas as pd

from prompt import MATH_EXTRACTION_PROMPT, question_types, difficulty_levels, MATH_GENERATION_PROMPT
from utils.graph_algorithm import build_concept_graph, random_walk_sampling


# 构建数学提取消息的函数
def construct_math_extraction_messages(num=100):
    parquet_file = 'files/GSM8K.parquet'  # Parquet文件的路径
    extraction_file = 'files/math_extraction.json'  # 已提取数据存储文件的路径

    # 读取Parquet文件的前num条数据
    df = pd.read_parquet(parquet_file).head(num)

    # 如果提取文件存在，则读取已经处理过的数据
    if os.path.exists(extraction_file):
        with open(extraction_file, 'r', encoding='utf-8') as ex_file:
            processed_data = json.load(ex_file)
            processed_ids = {item['id'] for item in processed_data}  # 获取已处理的ID集合
            existing_count = len(processed_data)  # 已处理的数据条数
    else:
        processed_ids = set()  # 如果文件不存在，初始化为空集合
        existing_count = 0  # 初始化已处理条数为0

    # 计算需要生成的新数据条数
    num_to_generate = num - existing_count
    if num_to_generate <= 0:
        print(f"Math Extraction: Already have {existing_count} messages, no new messages generated.")
        return [], []  # 如果已有数据足够，则不生成新数据

    messages_list = []
    metadata_list = []

    # 遍历Parquet文件中的数据，生成新的提取消息
    for index, row in df.iterrows():
        row_id = index
        if row_id in processed_ids:
            continue  # 跳过已经处理过的数据

        question = row['question']
        answer = row['answer']
        prompt = MATH_EXTRACTION_PROMPT.format(question=question)  # 根据问题生成提取提示
        messages_list.append([{"role": "user", "content": prompt}])
        metadata_list.append({"question": question, "answer": answer, "id": row_id})

        if len(messages_list) >= num_to_generate:
            break  # 如果生成的数据条数达到了需要生成的数量，则停止生成

    return messages_list, metadata_list  # 返回生成的消息列表和元数据列表


# 构建数学生成消息的函数
def construct_math_generation_messages(num=100):
    extraction_file = 'files/math_extraction.json'  # 提取数据文件的路径
    generation_file = 'files/math_generation.json'  # 生成数据文件的路径

    # 如果提取文件存在，则读取提取数据
    if os.path.exists(extraction_file):
        with open(extraction_file, 'r', encoding='utf-8') as ex_file:
            extraction_data = json.load(ex_file)
    else:
        print("No extraction data found. Please run math_extraction.py first.")
        exit()  # 如果提取文件不存在，提示并退出

    # 如果生成文件存在，则读取已生成的数据
    if os.path.exists(generation_file):
        with open(generation_file, 'r', encoding='utf-8') as gen_file:
            existing_data = json.load(gen_file)
            existing_count = len(existing_data)  # 已生成的数据条数
    else:
        existing_count = 0  # 初始化已生成条数为0

    # 计算需要生成的新数据条数
    num_to_generate = num - existing_count
    if num_to_generate <= 0:
        print(f"Math Generation: Already have {existing_count} messages, no new messages generated.")
        return [], []  # 如果已有数据足够，则不生成新数据

    # 构建概念图谱并进行随机游走采样
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
            continue  # 如果采样结果没有有效的主题或知识点，则跳过

        # 根据生成的内容构建提示
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

    return messages_list, metadata_list  # 返回生成的消息列表和元数据列表
