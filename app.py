import asyncio

from handlers.data_extractor import extract_question_and_answer, extract_topics_and_knowledge_points
from handlers.data_preparator import construct_math_generation_messages, construct_math_extraction_messages
from network.response_handler import retrieve_responses

if __name__ == "__main__":
    messages_list, metadata_list = construct_math_extraction_messages(num=100)
    asyncio.run(retrieve_responses(messages_list, metadata_list, extract_topics_and_knowledge_points))

    messages_list, metadata_list = construct_math_generation_messages(num=100)
    asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
