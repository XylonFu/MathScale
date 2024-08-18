# API的基本配置
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"  # 请求的API地址

# HTTP请求头配置
HEADERS = {
    'Content-Type': 'application/json',  # 指定请求的数据格式为JSON
    'Authorization': 'Bearer sk-xxxx'  # API访问所需的授权令牌
}

# 默认的请求有效载荷配置
DEFAULT_PAYLOAD = {
    "model": "qwen-turbo"  # 指定使用的模型
}

# 控制并发请求的最大数量
MAX_CONCURRENT_REQUESTS = 5  # 允许同时进行的最大并发请求数
