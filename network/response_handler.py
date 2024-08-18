import inspect
from functools import wraps

from network.payload_builder import prepare_payload
from network.request_manager import orchestrate_requests


# 装饰器函数，用于处理API响应
def process_response(process_function):
    @wraps(process_function)
    async def wrapper(index, response, metadata):
        try:
            # 从响应中提取内容
            content = response['choices'][0]['message']['content']
        except KeyError:
            # 如果响应中没有内容，则打印错误信息并跳过处理
            print(f"Error: No 'content' found in response at index {index}")
            return

        # 检查被装饰函数是否是协程，如果是则使用await，否则直接调用
        if inspect.iscoroutinefunction(process_function):
            await process_function(index, content, metadata)
        else:
            process_function(index, content, metadata)

    return wrapper


# 异步函数，用于批量处理消息并获取响应
async def retrieve_responses(messages_list, metadata_list, process_response):
    # 准备每个消息的有效载荷
    payloads = [prepare_payload(messages) for messages in messages_list]
    # 通过管理器发送请求并处理响应
    await orchestrate_requests(payloads, process_response, metadata_list)
