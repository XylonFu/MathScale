import asyncio

from handlers.data_extractor import extract_question_and_answer, extract_topics_and_knowledge_points
from handlers.data_preparator import construct_math_generation_messages, construct_math_extraction_messages
from network.response_handler import retrieve_responses

if __name__ == "__main__":
    # 构建用于提取主题和知识点的消息列表及元数据
    messages_list, metadata_list = construct_math_extraction_messages(num=100)
    # 运行异步任务，发送请求并处理提取主题和知识点的响应
    asyncio.run(retrieve_responses(messages_list, metadata_list, extract_topics_and_knowledge_points))

    # 构建用于生成数学问题的消息列表及元数据
    messages_list, metadata_list = construct_math_generation_messages(num=100)
    # 运行异步任务，发送请求并处理提取问题和答案的响应
    asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
