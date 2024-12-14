import asyncio
import json
import os
import re

import aiofiles

from network.response_handler import process_response

file_lock = asyncio.Lock()


# Asynchronous function to extract topics and knowledge points
@process_response
async def extract_topics_and_knowledge_points(index, content, metadata):
    extraction_file = 'files/math_extraction.json'
    try:
        # Use regular expressions to extract the JSON code block from Markdown
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', content)
        if json_match:
            json_content = json_match.group(1)
            analysis_data = json.loads(json_content)
        else:
            # If no JSON code block is found, attempt to parse the entire content directly
            analysis_data = json.loads(content)

        topics = analysis_data.get("topics", [])
        knowledge_points = analysis_data.get("knowledge_points", [])
    except json.JSONDecodeError:
        # If JSON parsing fails, print the error and set default values
        print(f"Error: Failed to decode JSON response at index {index}")
        topics = []
        knowledge_points = []

    extraction_data = {
        "id": metadata["id"],  # Use the ID from metadata
        "topics": topics,  # Extracted topics
        "knowledge_points": knowledge_points,  # Extracted knowledge points
        "question": metadata.get("question", ""),  # Get the question from metadata
        "answer": metadata.get("answer", "")  # Get the answer from metadata
    }

    async with file_lock:
        # Use a file lock to ensure thread safety for file operations
        if os.path.exists(extraction_file):
            async with aiofiles.open(extraction_file, 'r+', encoding='utf-8') as ex_file:
                existing_data = json.loads(await ex_file.read())  # Read existing data
                existing_data.append(extraction_data)  # Add new extracted data
                await ex_file.seek(0)
                await ex_file.write(
                    json.dumps(existing_data, ensure_ascii=False, indent=2))  # Write updated data back to file
        else:
            async with aiofiles.open(extraction_file, 'w', encoding='utf-8') as ex_file:
                await ex_file.write(
                    json.dumps([extraction_data], ensure_ascii=False, indent=2))  # Create a new file and write data

    print(f"Processed ID {metadata['id']}")


# Asynchronous function to extract questions and answers
@process_response
async def extract_question_and_answer(index, content, metadata):
    generation_file = 'files/math_generation.json'

    try:
        # Parse the API response content to extract questions and answers
        question = content.split("Question:")[1].split("Answer:")[0].strip()
        answer = content.split("Answer:")[1].strip()
    except IndexError:
        # If extraction fails, print the error and set default values
        print(f"Error: Failed to decode Text response at index {index}")
        question = ""
        answer = ""

    async with file_lock:
        # Use a file lock to ensure thread safety for file operations
        if os.path.exists(generation_file):
            async with aiofiles.open(generation_file, 'r+', encoding='utf-8') as ex_file:
                existing_data = json.loads(await ex_file.read())  # Read existing data
                if existing_data:
                    max_id = max(item['id'] for item in existing_data)  # Get the maximum ID from existing data
                else:
                    max_id = -1  # If no data exists, set the initial ID to -1
        else:
            existing_data = []
            max_id = -1  # If the file doesn't exist, set the initial ID to -1

        new_id = max_id + 1  # Calculate the ID for new data

        generation_data = {
            "id": new_id,  # ID for the new data
            "question": question,  # Extracted question
            "answer": answer,  # Extracted answer
            "topics": metadata.get("topics", []),  # Topics from metadata
            "knowledge_points": metadata.get("knowledge_points", []),  # Knowledge points from metadata
            "question_type": metadata.get("question_type", ""),  # Question type from metadata
            "difficulty": metadata.get("difficulty", "")  # Difficulty level from metadata
        }

        existing_data.append(generation_data)  # Add the new data to existing data
        async with aiofiles.open(generation_file, 'w', encoding='utf-8') as ex_file:
            await ex_file.write(
                json.dumps(existing_data, ensure_ascii=False, indent=2))  # Write updated data back to file

    print(f"Processed ID {new_id}")
