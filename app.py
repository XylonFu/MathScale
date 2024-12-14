import asyncio

from handlers.data_extractor import extract_question_and_answer, extract_topics_and_knowledge_points
from handlers.data_preparator import construct_math_generation_messages, construct_math_extraction_messages
from network.response_handler import retrieve_responses

if __name__ == "__main__":
    # Construct the message list and metadata for extracting topics and knowledge points
    messages_list, metadata_list = construct_math_extraction_messages(file_path="files/MATH.json",
                                                                      required_fields={
                                                                          'question': 'problem',
                                                                          'answer': 'solution',
                                                                          'id': 'id'
                                                                      },
                                                                      num=100)
    # Run asynchronous tasks to send requests and process the responses for extracting topics and knowledge points
    asyncio.run(retrieve_responses(messages_list, metadata_list, extract_topics_and_knowledge_points))

    # Construct the message list and metadata for generating math problems
    messages_list, metadata_list = construct_math_generation_messages(num=100)
    # Run asynchronous tasks to send requests and process the responses for extracting questions and answers
    asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
