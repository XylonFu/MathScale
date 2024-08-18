import asyncio

import aiohttp

from config import API_URL, HEADERS, MAX_CONCURRENT_REQUESTS


async def dispatch_request(session, payload, index, process_response, metadata):
    async with session.post(API_URL, headers=HEADERS, json=payload) as response:
        result = await response.json()
        await process_response(index, result, metadata)


async def orchestrate_requests(payloads, process_response, metadata_list):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, (payload, metadata) in enumerate(zip(payloads, metadata_list)):
            async with semaphore:
                task = asyncio.create_task(dispatch_request(session, payload, index, process_response, metadata))
                tasks.append(task)
        await asyncio.gather(*tasks)
