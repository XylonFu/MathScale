API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-xxxx'
}

DEFAULT_PAYLOAD = {
    "model": "qwen-turbo"
}

MAX_CONCURRENT_REQUESTS = 5
