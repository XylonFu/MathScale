# Basic API configuration
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"  # API endpoint URL

# HTTP request header configuration
HEADERS = {
    'Content-Type': 'application/json',  # Specify that the request data format is JSON
    'Authorization': 'Bearer sk-xxx'  # Authorization token required for API access
}

# Default payload configuration for requests
DEFAULT_PAYLOAD = {
    "model": "qwen-turbo"  # Specify the model to be used
}

# Maximum number of concurrent requests
MAX_CONCURRENT_REQUESTS = 5  # Maximum number of concurrent requests allowed
