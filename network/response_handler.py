import inspect
from functools import wraps

from network.payload_builder import prepare_payload
from network.request_manager import orchestrate_requests


# Decorator function for handling API responses
def process_response(process_function):
    @wraps(process_function)
    async def wrapper(index, response, metadata):
        try:
            # Extract content from the response
            content = response['choices'][0]['message']['content']
        except KeyError:
            # If no content is found in the response, print an error message and skip processing
            print(f"Error: No 'content' found in response at index {index}")
            return

        # Check if the decorated function is a coroutine; if so, use await, otherwise call directly
        if inspect.iscoroutinefunction(process_function):
            await process_function(index, content, metadata)
        else:
            process_function(index, content, metadata)

    return wrapper


# Asynchronous function for batch processing messages and retrieving responses
async def retrieve_responses(messages_list, metadata_list, process_response):
    # Prepare the payload for each message
    payloads = [prepare_payload(messages) for messages in messages_list]
    # Use the manager to send requests and handle responses
    await orchestrate_requests(payloads, process_response, metadata_list)
