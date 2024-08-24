import json
import os
import random

import pandas as pd

from prompt import MATH_EXTRACTION_PROMPT, question_types, difficulty_levels, MATH_GENERATION_PROMPT
from utils.graph_algorithm import build_concept_graph, random_walk_sampling


# 构建数学提取消息的函数
def construct_math_extraction_messages(file_path, required_fields, num=100):
    """
    通用的数据提取函数，根据文件后缀自动判断文件类型，并生成提取消息。

    :param file_path: 数据文件的路径
    :param required_fields: 字典形式，指定所需字段，如 {'question': 'problem', 'answer': 'solution', 'id': 'id'}
    :param num: 要提取的数据条数，默认为100
    :return: 消息列表和元数据列表
    """

    # 保存数据的文件路径
    save_path = "files/math_extraction.json"

    # 获取文件的后缀名以确定文件类型
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # 根据文件类型读取数据
    if file_extension == '.json':
        # 读取JSON文件并将其转换为Python对象
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif file_extension == '.csv':
        # 读取CSV文件并将其转换为字典列表
        data = pd.read_csv(file_path).to_dict(orient='records')
    elif file_extension == '.tsv':
        # 读取TSV文件并将其转换为字典列表
        data = pd.read_csv(file_path, sep='\t').to_dict(orient='records')
    elif file_extension == '.xlsx':
        # 读取Excel文件并将其转换为字典列表
        data = pd.read_excel(file_path).to_dict(orient='records')
    elif file_extension == '.parquet':
        # 读取Parquet文件并将其转换为字典列表
        data = pd.read_parquet(file_path).to_dict(orient='records')
    else:
        # 如果提供的文件类型不受支持，则抛出错误
        raise ValueError(f"Unsupported file extension: {file_extension}")

    # 如果保存的文件路径存在，则读取已经处理过的数据
    if os.path.exists(save_path):
        # 打开并加载已提取的数据文件
        with open(save_path, 'r', encoding='utf-8') as ex_file:
            processed_data = json.load(ex_file)
            processed_ids = {item['id'] for item in processed_data}  # 获取已处理的ID集合
            existing_count = len(processed_data)  # 已处理的数据条数
    else:
        # 如果文件不存在，初始化为一个空集合和已处理条数为0
        processed_ids = set()
        existing_count = 0

    # 计算需要生成的新数据条数
    num_to_generate = num - existing_count
    if num_to_generate <= 0:
        print(f"Extraction: Already have {existing_count} messages, no new messages generated.")
        return [], []  # 如果已有数据足够，则不生成新数据

    messages_list = []
    metadata_list = []

    # 遍历数据并生成新的提取消息
    for item in data:
        item_id = item[required_fields['id']]
        if item_id in processed_ids:
            continue  # 跳过已经处理过的数据

        # 从数据项中提取问题和答案
        question = item[required_fields['question']]
        answer = item[required_fields['answer']]
        # 根据问题生成提取提示
        prompt = MATH_EXTRACTION_PROMPT.format(question=question)
        # 将消息添加到消息列表中
        messages_list.append([{"role": "user", "content": prompt}])
        # 将元数据添加到元数据列表中
        metadata_list.append({"question": question, "answer": answer, "id": item_id})

        if len(messages_list) >= num_to_generate:
            break  # 如果生成的数据条数达到了需要生成的数量，则停止生成

    # 返回生成的消息列表和元数据列表
    return messages_list, metadata_list


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
