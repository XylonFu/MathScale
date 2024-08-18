import asyncio
import json
import os

import aiofiles

from network.response_handler import process_response

file_lock = asyncio.Lock()


@process_response
async def extract_topics_and_knowledge_points(index, content, metadata):
    extraction_file = 'files/math_extraction.json'

    try:
        analysis_data = json.loads(content)
        topics = analysis_data.get("topics", [])
        knowledge_points = analysis_data.get("knowledge_points", [])
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON response at index {index}")
        topics = []
        knowledge_points = []

    extraction_data = {
        "id": metadata["id"],
        "topics": topics,
        "knowledge_points": knowledge_points,
        "question": metadata.get("question", ""),
        "answer": metadata.get("answer", "")
    }

    async with file_lock:
        if os.path.exists(extraction_file):
            async with aiofiles.open(extraction_file, 'r+', encoding='utf-8') as ex_file:
                existing_data = json.loads(await ex_file.read())
                existing_data.append(extraction_data)
                await ex_file.seek(0)
                await ex_file.write(json.dumps(existing_data, ensure_ascii=False, indent=2))
        else:
            async with aiofiles.open(extraction_file, 'w', encoding='utf-8') as ex_file:
                await ex_file.write(json.dumps([extraction_data], ensure_ascii=False, indent=2))

    print(f"Processed ID {metadata['id']}")


@process_response
async def extract_question_and_answer(index, content, metadata):
    generation_file = 'files/math_generation.json'

    try:
        question = content.split("Question:")[1].split("Answer:")[0].strip()
        answer = content.split("Answer:")[1].strip()
    except IndexError:
        print(f"Error: Failed to decode Text response at index {index}")
        question = ""
        answer = ""

    async with file_lock:
        if os.path.exists(generation_file):
            async with aiofiles.open(generation_file, 'r+', encoding='utf-8') as ex_file:
                existing_data = json.loads(await ex_file.read())
                if existing_data:
                    max_id = max(item['id'] for item in existing_data)
                else:
                    max_id = -1
        else:
            existing_data = []
            max_id = -1

        new_id = max_id + 1

        generation_data = {
            "id": new_id,
            "question": question,
            "answer": answer,
            "topics": metadata.get("topics", []),
            "knowledge_points": metadata.get("knowledge_points", []),
            "question_type": metadata.get("question_type", ""),
            "difficulty": metadata.get("difficulty", "")
        }

        existing_data.append(generation_data)
        async with aiofiles.open(generation_file, 'w', encoding='utf-8') as ex_file:
            await ex_file.write(json.dumps(existing_data, ensure_ascii=False, indent=2))

    print(f"Processed ID {new_id}")
