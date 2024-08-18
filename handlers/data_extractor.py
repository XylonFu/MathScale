import asyncio
import json
import os

import aiofiles

from network.response_handler import process_response

file_lock = asyncio.Lock()


# 提取主题和知识点的异步函数
@process_response
async def extract_topics_and_knowledge_points(index, content, metadata):
    extraction_file = 'files/math_extraction.json'

    try:
        # 解析API返回的内容，提取topics和knowledge_points
        analysis_data = json.loads(content)
        topics = analysis_data.get("topics", [])
        knowledge_points = analysis_data.get("knowledge_points", [])
    except json.JSONDecodeError:
        # 如果JSON解析失败，打印错误并设置默认值
        print(f"Error: Failed to decode JSON response at index {index}")
        topics = []
        knowledge_points = []

    extraction_data = {
        "id": metadata["id"],  # 使用metadata中的id
        "topics": topics,  # 提取的主题
        "knowledge_points": knowledge_points,  # 提取的知识点
        "question": metadata.get("question", ""),  # 从metadata中获取问题
        "answer": metadata.get("answer", "")  # 从metadata中获取答案
    }

    async with file_lock:
        # 使用文件锁确保文件操作的线程安全
        if os.path.exists(extraction_file):
            async with aiofiles.open(extraction_file, 'r+', encoding='utf-8') as ex_file:
                existing_data = json.loads(await ex_file.read())  # 读取现有数据
                existing_data.append(extraction_data)  # 添加新的提取数据
                await ex_file.seek(0)
                await ex_file.write(json.dumps(existing_data, ensure_ascii=False, indent=2))  # 将更新后的数据写回文件
        else:
            async with aiofiles.open(extraction_file, 'w', encoding='utf-8') as ex_file:
                await ex_file.write(json.dumps([extraction_data], ensure_ascii=False, indent=2))  # 创建新文件并写入数据

    print(f"Processed ID {metadata['id']}")


# 提取问题和答案的异步函数
@process_response
async def extract_question_and_answer(index, content, metadata):
    generation_file = 'files/math_generation.json'

    try:
        # 解析API返回的内容，提取问题和答案
        question = content.split("Question:")[1].split("Answer:")[0].strip()
        answer = content.split("Answer:")[1].strip()
    except IndexError:
        # 如果提取失败，打印错误并设置默认值
        print(f"Error: Failed to decode Text response at index {index}")
        question = ""
        answer = ""

    async with file_lock:
        # 使用文件锁确保文件操作的线程安全
        if os.path.exists(generation_file):
            async with aiofiles.open(generation_file, 'r+', encoding='utf-8') as ex_file:
                existing_data = json.loads(await ex_file.read())  # 读取现有数据
                if existing_data:
                    max_id = max(item['id'] for item in existing_data)  # 获取现有数据中的最大ID
                else:
                    max_id = -1  # 如果没有数据，设置初始ID为-1
        else:
            existing_data = []
            max_id = -1  # 如果文件不存在，设置初始ID为-1

        new_id = max_id + 1  # 计算新数据的ID

        generation_data = {
            "id": new_id,  # 新生成的数据ID
            "question": question,  # 提取的问题
            "answer": answer,  # 提取的答案
            "topics": metadata.get("topics", []),  # 从metadata中获取的主题
            "knowledge_points": metadata.get("knowledge_points", []),  # 从metadata中获取的知识点
            "question_type": metadata.get("question_type", ""),  # 从metadata中获取的问题类型
            "difficulty": metadata.get("difficulty", "")  # 从metadata中获取的难度
        }

        existing_data.append(generation_data)  # 将新数据添加到现有数据中
        async with aiofiles.open(generation_file, 'w', encoding='utf-8') as ex_file:
            await ex_file.write(json.dumps(existing_data, ensure_ascii=False, indent=2))  # 将更新后的数据写回文件

    print(f"Processed ID {new_id}")
