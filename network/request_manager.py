import asyncio

import aiohttp

from config import API_URL, HEADERS, MAX_CONCURRENT_REQUESTS


# 发送单个API请求并处理响应的异步函数
async def dispatch_request(session, payload, index, process_response, metadata):
    # 向指定API发送POST请求，并等待响应
    async with session.post(API_URL, headers=HEADERS, json=payload) as response:
        result = await response.json()  # 解析响应为JSON
        await process_response(index, result, metadata)  # 处理响应数据


# 管理多个并发API请求的异步函数
async def orchestrate_requests(payloads, process_response, metadata_list):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)  # 限制并发请求的数量

    async with aiohttp.ClientSession() as session:
        tasks = []
        # 为每个有效载荷创建一个任务，并限制并发执行数量
        for index, (payload, metadata) in enumerate(zip(payloads, metadata_list)):
            async with semaphore:
                task = asyncio.create_task(dispatch_request(session, payload, index, process_response, metadata))
                tasks.append(task)
        await asyncio.gather(*tasks)  # 等待所有任务完成
