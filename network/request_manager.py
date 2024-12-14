import asyncio

import aiohttp

from config import API_URL, HEADERS, MAX_CONCURRENT_REQUESTS


# Asynchronous function to send a single API request and handle the response
async def dispatch_request(session, payload, index, process_response, metadata):
    # Send a POST request to the specified API and await the response
    async with session.post(API_URL, headers=HEADERS, json=payload) as response:
        result = await response.json()  # Parse the response as JSON
        await process_response(index, result, metadata)  # Process the response data


# Asynchronous function to manage multiple concurrent API requests
async def orchestrate_requests(payloads, process_response, metadata_list):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)  # Limit the number of concurrent requests

    async with aiohttp.ClientSession() as session:
        tasks = []
        # Create a task for each payload and limit the number of concurrent executions
        for index, (payload, metadata) in enumerate(zip(payloads, metadata_list)):
            async with semaphore:
                task = asyncio.create_task(dispatch_request(session, payload, index, process_response, metadata))
                tasks.append(task)
        await asyncio.gather(*tasks)  # Wait for all tasks to complete
