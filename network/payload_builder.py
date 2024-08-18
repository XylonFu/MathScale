from config import DEFAULT_PAYLOAD


# 准备API请求的有效载荷
def prepare_payload(messages, payload=None):
    # 如果提供了自定义payload，复制它；否则使用默认payload
    payload = payload.copy() if payload else DEFAULT_PAYLOAD.copy()

    # 将消息添加到payload中
    payload["messages"] = messages

    # 返回最终的payload
    return payload
