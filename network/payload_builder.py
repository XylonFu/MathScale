from config import DEFAULT_PAYLOAD


def prepare_payload(messages, payload=None):
    payload = payload.copy() if payload else DEFAULT_PAYLOAD.copy()
    payload["messages"] = messages
    return payload
