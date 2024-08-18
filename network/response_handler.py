import inspect
from functools import wraps

from network.payload_builder import prepare_payload
from network.request_manager import orchestrate_requests


def process_response(process_function):
    @wraps(process_function)
    async def wrapper(index, response, metadata):
        try:
            content = response['choices'][0]['message']['content']
        except KeyError:
            print(f"Error: No 'content' found in response at index {index}")
            return

        if inspect.iscoroutinefunction(process_function):
            await process_function(index, content, metadata)
        else:
            process_function(index, content, metadata)

    return wrapper


async def retrieve_responses(messages_list, metadata_list, process_response):
    payloads = [prepare_payload(messages) for messages in messages_list]
    await orchestrate_requests(payloads, process_response, metadata_list)
